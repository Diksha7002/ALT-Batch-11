import os
import json
import torch
import numpy as np
from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from preprocess import normalize_text, analyze_pragmatics

app = Flask(__name__)

# ============================================================
# LOAD MODEL & CONFIGURATION
# ============================================================

MODEL_FOLDER = "./emotion_model"
NUM_CLASSES = 28

print("\nLoading emotion detection model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_FOLDER)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_FOLDER)
model.eval()
print("Model loaded successfully!")

# Retrieve the model's own id2label mapping
id2label = model.config.id2label
emotion_names = [id2label.get(c, id2label.get(str(c), f"Class_{c}")) for c in range(NUM_CLASSES)]
name2id = {name: i for i, name in enumerate(emotion_names)}
print(f"Mapped {len(emotion_names)} classes from model config.")

# Load per-class optimal thresholds
threshold_path = os.path.join(MODEL_FOLDER, "thresholds.json")
if os.path.exists(threshold_path):
    with open(threshold_path, "r") as f:
        thresholds = json.load(f)
    print("Tuned class thresholds loaded successfully.")
else:
    thresholds = [0.30] * NUM_CLASSES

# Polarity clustering for visual analytics
EMOTION_POLARITIES = {
    "positive": ["admiration", "amusement", "approval", "caring", "desire", "excitement", "gratitude", "joy", "love", "optimism", "pride", "relief"],
    "negative": ["anger", "annoyance", "disapproval", "disgust"],
    "melancholy": ["disappointment", "fear", "grief", "nervousness", "sadness", "remorse", "embarrassment"],
    "surprise": ["confusion", "curiosity", "realization", "surprise"],
    "neutral": ["neutral"]
}

def get_polarity(emotion):
    for pol, list_e in EMOTION_POLARITIES.items():
        if emotion in list_e:
            return pol
    return "neutral"

# ============================================================
# ROUTING
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received."}), 400

        original_text = data.get("text", "").strip()
        if not original_text:
            return jsonify({"error": "Please enter some text."}), 400

        # 1. Normalize text using preprocess pipeline
        normalized_text = normalize_text(original_text)

        # 2. Extract linguistic and pragmatic nuances (indirect speech, sarcasm, idioms)
        pragmatics = analyze_pragmatics(original_text, normalized_text)

        # 3. Model Tokenization & Forward Pass
        inputs = tokenizer(
            normalized_text,
            return_tensors="pt",
            truncation=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = model(**inputs)
        
        # Base probabilities via Sigmoid
        probs = torch.sigmoid(outputs.logits)[0].cpu().numpy().copy()

        # 4. Apply Pragmatic Calibration for indirect expressions
        if pragmatics["is_indirect"]:
            # Damp neutral for all indirect / figurative expressions
            if "neutral" in name2id:
                probs[name2id["neutral"]] *= 0.05
                
            # Heavily suppress misleading superficial emotions
            for supp_emo in pragmatics["suppress_emotions"]:
                if supp_emo in name2id:
                    c_idx = name2id[supp_emo]
                    probs[c_idx] = probs[c_idx] * 0.02  # remove superficial sentiment
                    
            # Boost figurative / contextually implied emotions
            for boost_emo, boost_val in pragmatics["boost_emotions"].items():
                if boost_emo in name2id:
                    c_idx = name2id[boost_emo]
                    probs[c_idx] = max(probs[c_idx], float(boost_val))

        # 5. Extract multi-label detections based on thresholds
        detected_emotions = []
        for index, prob in enumerate(probs):
            score = float(prob)
            thresh = float(thresholds[index])
            if score >= thresh:
                detected_emotions.append({
                    "emotion": emotion_names[index],
                    "confidence": round(score * 100, 2),
                    "polarity": get_polarity(emotion_names[index])
                })

        # Fallback to single highest-confidence emotion if none exceeded threshold
        if not detected_emotions:
            best_index = int(np.argmax(probs))
            best_score = float(probs[best_index])
            detected_emotions.append({
                "emotion": emotion_names[best_index],
                "confidence": round(best_score * 100, 2),
                "polarity": get_polarity(emotion_names[best_index])
            })

        # Sort detected emotions by confidence descending
        detected_emotions.sort(key=lambda x: x["confidence"], reverse=True)

        primary_emotion = detected_emotions[0]["emotion"]
        primary_confidence = detected_emotions[0]["confidence"]
        primary_polarity = get_polarity(primary_emotion)

        # Complete top scores breakdown for charts
        top_indices = np.argsort(probs)[::-1][:6]
        top_spectrum = [
            {
                "emotion": emotion_names[idx],
                "confidence": round(float(probs[idx]) * 100, 2),
                "polarity": get_polarity(emotion_names[idx])
            }
            for idx in top_indices
        ]

        # Formulate API response payload
        return jsonify({
            "emotion": primary_emotion,
            "confidence": primary_confidence,
            "polarity": primary_polarity,
            "emotions": detected_emotions,
            "spectrum": top_spectrum,
            "original_text": original_text,
            "normalized_text": normalized_text,
            "signals": pragmatics["signals"],
            "is_indirect": pragmatics["is_indirect"],
            "pragmatic_notes": pragmatics["pragmatic_notes"],
            "idiom_matched": pragmatics["idiom_matched"],
            "sarcasm_detected": pragmatics["sarcasm_detected"]
        })

    except Exception as e:
        print("Prediction server error:", str(e))
        return jsonify({"error": "An error occurred during text analysis. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True)