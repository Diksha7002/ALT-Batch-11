import re

# Common contractions for expansion
CONTRACTIONS = {
    "can't": "cannot",
    "won't": "will not",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "aren't": "are not",
    "isn't": "is not",
    "couldn't": "could not",
    "shouldn't": "should not",
    "wouldn't": "would not",
    "i'm": "I am",
    "you're": "you are",
    "they're": "they are",
    "we're": "we are",
    "he's": "he is",
    "she's": "she is",
    "it's": "it is",
    "that's": "that is",
    "what's": "what is",
    "there's": "there is",
    "cant": "cannot",
    "wont": "will not",
    "dont": "do not",
    "doesnt": "does not",
    "didnt": "did not",
    "wasnt": "was not",
    "werent": "were not",
    "havent": "have not",
    "hasnt": "has not",
    "hadnt": "had not",
    "arent": "are not",
    "isnt": "is not",
    "couldnt": "could not",
    "shouldnt": "should not",
    "wouldnt": "would not",
    "im": "I am",
    "youre": "you are",
    "theyre": "they are",
    "weare": "we are",
    "hes": "he is",
    "shes": "she is",
    "its": "it is",
    "whats": "what is",
    "theres": "there is",
}

# Slang abbreviations mapping to standard words
SLANG_MAP = {
    "u": "you",
    "r": "are",
    "ur": "your",
    "y": "why",
    "omg": "oh my god",
    "idk": "I do not know",
    "tbh": "to be honest",
    "imo": "in my opinion",
    "imho": "in my humble opinion",
    "pls": "please",
    "plz": "please",
    "thx": "thanks",
    "ty": "thank you",
    "lol": "laugh out loud",
    "wtf": "what the fuck",
    "ppl": "people",
    "rn": "right now",
    "sry": "sorry",
    "gr8": "great",
    "b4": "before",
    "soo": "so",
    "loove": "love",
    "aree": "are",
    "haate": "hate",
}

# English letters that commonly appear doubled in spelling (e.g. good, feel, happy)
ALLOWED_DOUBLES = {'e', 'o', 'l', 's', 't', 'p', 'f', 'd', 'g', 'm', 'n', 'r', 'c', 'b'}

# ============================================================
# COMPREHENSIVE IDIOMS & FIGURATIVE SPEECH TAXONOMY (50+ ENTRIES)
# ============================================================
# ============================================================
# COMPREHENSIVE IDIOMS & FIGURATIVE SPEECH TAXONOMY (80+ ENTRIES)
# ============================================================
IDIOM_MAPPINGS = [
    # 1. Contempt, Betrayal & Severe Disapproval
    {
        "pattern": r"\b(good for nothing|useless piece of|waste of space|worthless|dead weight|waste of time)\b",
        "description": "Idiomatic contempt / worthlessness",
        "boost": {"disapproval": 0.90, "annoyance": 0.65, "disgust": 0.50},
        "suppress": ["admiration", "approval", "joy", "gratitude"]
    },
    {
        "pattern": r"\b(dead to me|done with (you|this)|had enough of|cut ties with|burned bridges?)\b",
        "description": "Severe estrangement / relational finality",
        "boost": {"anger": 0.85, "disapproval": 0.80, "annoyance": 0.70},
        "suppress": ["love", "caring", "joy", "approval"]
    },
    {
        "pattern": r"\b((threw|throw(n|ing|s)?)\s+(me|us|him|her|them|someone)?\s*under the bus|stabbed\s+(me|us|him|her|them)?\s*in the back|backstabb(ing|er|ed))\b",
        "description": "Idiomatic betrayal / grievance",
        "boost": {"anger": 0.88, "disapproval": 0.82, "disappointment": 0.70},
        "suppress": ["admiration", "joy", "gratitude", "love", "neutral"]
    },
    {
        "pattern": r"\b(cold shoulder|turned? (their|his|her|your) back on)\b",
        "description": "Idiomatic rejection / ostracization",
        "boost": {"disapproval": 0.85, "sadness": 0.75, "annoyance": 0.65},
        "suppress": ["caring", "love", "approval"]
    },
    {
        "pattern": r"\b(makes? my skin crawl|turns? my stomach|sick to my stomach|leaves? a bad taste in my mouth|makes? me sick|gag me)\b",
        "description": "Idiomatic visceral disgust",
        "boost": {"disgust": 0.90, "disapproval": 0.70, "annoyance": 0.60},
        "suppress": ["joy", "admiration", "approval", "love"]
    },

    # 2. Outrage, Fury & Extreme Frustration
    {
        "pattern": r"\b(makes? my blood boil|see(ing)? red|blew a fuse|blow a fuse|hit the roof|lost my cool|lost my temper|fly off the handle|crossed? the line|add(ing)? fuel to the fire|slap in the face)\b",
        "description": "Idiomatic boiling fury / indignation",
        "boost": {"anger": 0.96, "annoyance": 0.85, "disapproval": 0.75},
        "suppress": ["joy", "relief", "optimism", "caring", "fear", "sadness", "neutral"]
    },
    {
        "pattern": r"\b(at the end of my rope|pulling my hair out|driv(e|ing) me (up the wall|crazy|nuts|insane)|last straw|on my last nerve|sick and tired of|fed up with)\b",
        "description": "Idiomatic peak exasperation / frustration",
        "boost": {"annoyance": 0.92, "anger": 0.75, "disapproval": 0.65},
        "suppress": ["joy", "approval", "relief", "optimism"]
    },
    {
        "pattern": r"\b(give (me|us) a break|cry me a river|over my dead body|give it a rest|save it|take a hike|get lost)\b",
        "description": "Exasperated dismissal / rejection",
        "boost": {"annoyance": 0.88, "disapproval": 0.75, "anger": 0.70},
        "suppress": ["approval", "joy", "caring"]
    },
    {
        "pattern": r"\b(cost an arm and a leg|daylight robbery|robbery in broad daylight|rip[- ]?off)\b",
        "description": "Idiomatic outrage at price / gouging",
        "boost": {"annoyance": 0.85, "disapproval": 0.75, "surprise": 0.65},
        "suppress": ["joy", "approval"]
    },

    # 3. Supreme Admiration, Achievement & Humor
    {
        "pattern": r"\b(kill(ing|ed)? it|nail(ing|ed)? it|crush(ing|ed)? it|on fire|slay(ing|ed)?|knock(ed|ing)? it out of the park|outdid yourself|take my hat off to|cream of the crop|gold standard|class act)\b",
        "description": "Figurative compliment / supreme achievement",
        "boost": {"admiration": 0.88, "excitement": 0.80, "joy": 0.75, "approval": 0.70},
        "suppress": ["fear", "sadness", "anger", "disapproval"]
    },
    {
        "pattern": r"\b(dying of laughter|dying laughing|cracking up|burst out laughing|rolling on the floor|in stitches|cracked me up|had me in tears)\b",
        "description": "Figurative extreme hilarity / amusement",
        "boost": {"amusement": 0.95, "joy": 0.80},
        "suppress": ["fear", "sadness", "grief", "disappointment"]
    },
    {
        "pattern": r"\b(on cloud nine|over the moon|top of the world|walking on air|thrilled to bits|in seventh heaven|having a blast|time of my life|jump(ed)? for joy|paint the town red|tickled pink)\b",
        "description": "Idiomatic supreme joy / ecstasy",
        "boost": {"joy": 0.95, "excitement": 0.85, "optimism": 0.70},
        "suppress": ["sadness", "fear", "neutral", "anger"]
    },
    {
        "pattern": r"\b(breathe a sigh of relief|weight off my shoulders|bullet dodged|dodged a bullet|out of the woods|off the hook|breath of fresh air|smooth sailing|light at the end of the tunnel)\b",
        "description": "Idiomatic tension release / relief",
        "boost": {"relief": 0.92, "joy": 0.65, "optimism": 0.60},
        "suppress": ["fear", "nervousness", "anger"]
    },
    {
        "pattern": r"\b(break a leg|silver lining|hang in there|keep your chin up|brighter days ahead|fingers crossed)\b",
        "description": "Theatrical blessing / encouraging optimism",
        "boost": {"optimism": 0.88, "caring": 0.70, "admiration": 0.60},
        "suppress": ["fear", "sadness"]
    },
    {
        "pattern": r"\b(proud as a peacock|have (my|your) back|hold your head high|feather in (my|your|his|her) cap)\b",
        "description": "Idiomatic pride / solidarity",
        "boost": {"pride": 0.88, "admiration": 0.75, "caring": 0.70},
        "suppress": ["shame", "sadness"]
    },
    {
        "pattern": r"\b(head over heels|apple of my eye|stole my heart|love (you|him|her|them) to the moon and back|soft spot for|means? the world to me)\b",
        "description": "Idiomatic deep love / affection",
        "boost": {"love": 0.95, "caring": 0.85, "joy": 0.75},
        "suppress": ["disapproval", "anger", "disgust"]
    },

    # 4. Melancholy, Grief, Despair & Heartbreak
    {
        "pattern": r"\b(under the weather|feeling blue|down in the dumps|broken heart(ed)?|heavy heart|lump in my throat|crying my eyes out|world crashed down|heart sank|hit rock bottom|down in the doldrums|drowning in sorrow|eat(ing)? my heart out|torn apart)\b",
        "description": "Idiomatic sadness / dejection",
        "boost": {"sadness": 0.92, "disappointment": 0.75, "grief": 0.70},
        "suppress": ["joy", "amusement", "admiration", "approval"]
    },
    {
        "pattern": r"\b(face the music|hard pill to swallow|swallow the bitter pill|wake[- ]?up call|back to reality|cry over spill?ed milk|burst my bubble)\b",
        "description": "Idiomatic painful realization / disappointment",
        "boost": {"disappointment": 0.85, "realization": 0.75, "sadness": 0.65},
        "suppress": ["joy", "optimism"]
    },

    # 5. Anxiety, Dread, Panic & Fear
    {
        "pattern": r"\b(on pins and needles|butterflies in (my|the) stomach|scared out of my mind|scared to death|shaking in (my|our) boots|edge of (my|our) seat|walking on eggshells|cold feet|bite my nails|heart in my throat|sweating bullets|freaking out|in a cold sweat|jump(ed)? out of (my|our) skin)\b",
        "description": "Idiomatic intense apprehension / fear",
        "boost": {"nervousness": 0.92, "fear": 0.88},
        "suppress": ["relief", "joy", "calm"]
    }
]

ALL_POSITIVE_EMOTIONS = ["admiration", "joy", "approval", "gratitude", "optimism", "caring", "love", "relief", "pride", "amusement"]
ALL_NEGATIVE_EMOTIONS = ["anger", "annoyance", "disapproval", "disgust", "fear", "sadness", "grief", "disappointment", "embarrassment", "remorse"]

# Lexicons for Semantic Incongruity / Sarcasm Detection
POSITIVE_SENTIMENT_TOKENS = {
    "great", "fantastic", "brilliant", "wonderful", "perfect", "lovely", "amazing",
    "superb", "glad", "happy", "thrilled", "genius", "masterpiece", "delightful",
    "sweet", "kind", "thoughtful", "helpful", "pure joy", "perfection", "love",
    "adore", "appreciate", "cherish", "5-star", "5 star", "best", "blessed", "miracle",
    "hero", "thanks", "thank you", "nice", "favorite", "favourite", "enjoy"
}

NEGATIVE_SITUATION_TOKENS = {
    "delay", "delayed", "late", "later", "weeks later", "days later", "months later",
    "hours later", "too late", "aftermath", "broke", "broken", "breaking", "mistake",
    "disaster", "mess", "headache", "ruined", "ruining", "traffic", "error", "crash",
    "crashed", "nightmare", "fail", "failed", "failing", "died", "flat tire", "tire",
    "rain", "standing in the rain", "forgot", "forgotten", "ignored", "ghosted",
    "bills", "cancel", "cancelled", "canceling", "dropped", "dropping", "screwed",
    "destroy", "destroyed", "wreck", "wrecked", "problem", "issue", "trouble", "alone",
    "hospital", "ticket", "fine", "loss", "nothing", "useless", "dead", "worst",
    "cuts out", "cut out", "mid-game", "down", "freezes", "frozen", "garbage", "trash",
    "spilled", "spilt", "stolen", "lost"
}

SARCASTIC_PHRASES = [
    # --- Classic sarcasm tropes ---
    r"\b(yeah\s*,?\s*right)\b",
    r"\b(as\s+if)\b",
    r"\b(like\s+that(\s+is|\'s|\s+will)?\s+(ever\s+)?(gonna|going\s+to|will)?\s*happen)\b",
    r"\b(just\s+great|just\s+perfect|just\s+wonderful|just\s+lovely|just\s+fantastic|just\s+brilliant)\s*[.!]?",
    r"\b(what\s+a\s+surprise|who\s+could\s+have\s+guessed|no\s+kidding|what\s+a\s+shock|what\s+a\s+shocker|big\s+surprise|no\s+surprise\s+there|color\s+me\s+surprised|shocker)\b",
    r"\b(sure\s*,?\s*(whatever|if)\s+you\s+say\s+so)\b",
    r"\b(oh\s+sure\s*,?\s*totally)\b",

    # --- Ironic Agreement: "Oh yes/sure/right, because ..." ---
    r"\b(oh\s+(yes|yeah|sure|right)\s*,?\s*because)\b",
    r"\b(yes\s*,?\s*because\s+(i|we|that)\s+(clearly|obviously|totally|definitely|absolutely))\b",
    r"\b(sure\s*,?\s*because\s+(i|we|that|this|it))\b",
    r"\b(right\s*,?\s*because\s+(i|we|everyone|that|this|it))\b",

    # --- Exaggerated certainty / false sincerity markers ---
    r"\b(because\s+i\s+(clearly|obviously|totally|definitely|absolutely)\s+(have|had|do|did|am|was|need|want|love|enjoy|came))\b",
    r"\b(because\s+(that\s+is|this\s+is|it\s+is)\s+(exactly|totally|clearly|obviously)\s+(what|how))\b",
    r"\b(clearly\s*,?\s*(i|we|that|this)\s+(have|had|do|did|was|were|need|deserve))\b",
    r"\b(obviously\s*,?\s*(i|we|that|this)\s+(have|had|do|did|was|were|need|deserve))\b",

    # --- Self-deprecating / rhetorical sarcasm ---
    r"\b(nothing\s+better\s+to\s+do)\b",
    r"\b(all\s+the\s+time\s+in\s+the\s+world)\b",
    r"\b(because\s+that\s+is\s+(exactly|just|precisely)\s+what\s+i\s+(needed|wanted|asked\s+for))\b",
    r"\b(exactly\s+what\s+i\s+(needed|wanted|asked\s+for|was\s+hoping\s+for))\b",
    r"\b(just\s+what\s+i\s+(needed|wanted|asked\s+for|was\s+hoping\s+for))\b",

    # --- Dismissive sarcasm ---
    r"\b(thanks\s+for\s+nothing|thank\s+you\s+for\s+nothing)\b",
    r"\b(must\s+be\s+nice(\s+to)?)\b",
    r"\b(used\s+to\s+being\s+(ignored|forgotten|left\s+out|alone))\b",
    r"\b(do\s+not\s+worry\s+about\s+me|dont\s+worry\s+about\s+me)\b",
    r"\b(take\s+your\s+time\b.*?\b(not\s+like|deadline|matter))\b",
    r"\b(i\s+am\s+sure\s+you\s+tried\s+your\s+best)\b",
    r"\b(oh\s+wow\s*,?\s*what\s+an\s+achievement)\b",
    r"\b(good\s+luck\s+with\s+that)\b",
    r"\b(real\s+smooth\b|smooth\s+move)\b",

    # --- Praise + Destructive action (ironic compliment) ---
    r"\b(nice\s+job\s+(breaking|ruining|messing|dropping|losing|forgetting)\b)",
    r"\b(great\s+job\s+(breaking|ruining|crashing|messing|losing|forgetting)\b)",
    r"\b(good\s+job\s+(breaking|ruining|crashing|messing|losing|forgetting)\b)",
    r"\b(well\s+done\s+(breaking|ruining|crashing|messing|losing|forgetting)\b)",
    r"\b(brilliant\s+(move|idea|plan|thinking)\b)",
    r"\b(genius\s+(move|idea|plan|thinking)\b)",

    # --- "Oh how [positive]" ironic exclamations ---
    r"\b(oh\s+how\s+(lovely|wonderful|great|nice|fun|exciting|charming|delightful|sweet|pleasant))\b",
    r"\b(how\s+(lovely|wonderful|great|nice|fun|exciting|charming|delightful|sweet|pleasant)\s+of\s+(you|them|him|her))\b",
    r"\b(oh\s+(lovely|wonderful|great|nice|fantastic|brilliant|perfect)\s*[,.])",

    # --- Fake enthusiasm about bad things ---
    r"\b(i\s+just\s+love\s+(waiting|standing|getting|being|paying|sitting\s+in|having|dealing|watching|hearing|listening))\b",
    r"\b(i\s+love\s+how\s+(you|they|he|she|we|everyone|nobody|no\s+one)\b.*?\b(never|always|forgot|ignore|do\s+not|does\s+not|did\s+not|can\s+not))\b",
    r"\b(my\s+favorite\s+(part|thing)\s+(is|was)\s+(when|how|that)\b)",
    r"\b(so\s+glad\s+(i|we)\s+(got\s+to|had\s+to|have\s+to|get\s+to)\s+(wait|stand|sit|deal|pay|spend|waste))\b",

    # --- Belittling with "nice" / "great" + negative context ---
    r"\b(nice\s+of\s+you\s+to\s+(finally\s+)?(show\s+up|reply|remember|come|join|bother|notice|care))\b",
    r"\b(thanks\s+a\s+lot\s+for\s+(breaking|ruining|forgetting|ignoring|leaving|dumping|wasting))\b",

    # --- Incredulous / mocking sarcasm ---
    r"\b(tell\s+me\s+something\s+i\s+do\s+not\s+know)\b",
    r"\b(as\s+if\s+i\s+(care|do\s+not\s+have\s+enough))\b",
    r"\b(wow\s*,?\s*i\s+(never|did\s+not)\s+(would\s+have\s+)?(guess(ed)?|know(n)?|think|expect(ed)?|imagine(d)?))\b",
    r"\b(who\s+would\s+have\s+(thought|guessed|known|imagined))\b",
    r"\b(well\s*,?\s*that\s+(went|turned\s+out|worked\s+out)\s+(well|great|perfectly|beautifully|wonderfully))\b",

    # --- Understated "totally fine" / "no problem" sarcasm ---
    r"\b(no\s*,?\s*that\s+is\s+(totally|absolutely|completely|perfectly)\s+(fine|okay|normal|acceptable|great|wonderful))\b",
    r"\b(because\s+my\s+(time|feelings?|opinion|effort|work)\s+(do\s+not|does\s+not|did\s+not)\s+(matter|count))\b",
    r"\b(not\s+like\s+(i|we|anyone|my|it)\b.*?\b(matters?|cares?|counts?|important|means?\s+anything))\b",
    r"\b(it\s+is\s+not\s+like\s+i\s+(have|had|need|wanted|care|was))\b",
    r"\b(not\s+like\s+(my|our)\s+(opinion|input|feelings?|effort|time|work)\s+(matters?|counts?))\b"
]

PASSIVE_AGGRESSIVE_PATTERNS = [
    r"\b(i\s+guess\s+that\s+is\s+fine|i\s+guess\s+that\'?s\s+fine|do\s+whatever\s+you\s+want|whatever\s+you\s+say|if\s+you\s+say\s+so|fine\s*,\s*be\s+that\s+way)\b",
    r"\b(no\s*,\s*it\s+is\s+totally\s+fine|i\s+am\s+not\s+mad|not\s+like\s+anyone\s+cares)\b",
    r"\b(do\s+not\s+worry\s+about\s+(helping|it|me)\b.*?\b(i\s+will|myself|alone|on\s+my\s+own))\b",
    r"\b(whatever\s+you\s+think\s+is\s+best\s*,?\s*since\s+my\s+opinion\s+does\s+not\s+matter)\b",
    r"\b(i\s+guess\s+my\s+input\s+did\s+not\s+matter)\b"
]

LITOTES_PATTERNS = [
    {
        "pattern": r"\b(not\s+(too|that)\s+shabby|not\s+bad\s+at\s+all|cannot\s+complain|could\s+not\s+be\s+(happier|better))\b",
        "description": "Litotes / Modest high praise",
        "boost": {"approval": 0.88, "joy": 0.80, "optimism": 0.70},
        "suppress": ["disapproval", "sadness", "anger"]
    },
    {
        "pattern": r"\b(not\s+(the\s+sharpest|the\s+brightest|a\s+genius))\b",
        "description": "Litotes / Mocking understatement",
        "boost": {"disapproval": 0.85, "amusement": 0.65},
        "suppress": ["admiration", "approval"]
    },
    {
        "pattern": r"\b(no\s+walk\s+in\s+the\s+park|no\s+piece\s+of\s+cake|no\s+picnic)\b",
        "description": "Litotes / Hardship understatement",
        "boost": {"nervousness": 0.75, "annoyance": 0.65, "fear": 0.60},
        "suppress": ["joy", "relief"]
    }
]

BACKHANDED_PATTERNS = [
    {
        "pattern": r"\b(surprisingly\s+(good|smart|capable|competent)|not\s+as\s+(bad|terrible|awful)\s+as\s+i\s+(thought|expected)|pretty\s+(smart|good)\s+for\s+someone|i\s+love\s+how\s+you\s+can\s+just\s+wear\s+anything)\b",
        "description": "Backhanded compliment / subtle insult",
        "boost": {"disapproval": 0.78, "surprise": 0.65, "annoyance": 0.60},
        "suppress": ["love", "gratitude"]
    }
]

RHETORICAL_PATTERNS = [
    r"\b(why\s+would\s+you\s+do\s+this|how\s+could\s+you\s+do\s+this|why\s+me|what\s+did\s+i\s+do\s+to\s+deserve\s+this)\b",
    r"\b(are\s+you\s+kidding\s+me|are\s+you\s+serious|you\s+cannot\s+be\s+serious|you\s+have\s+got\s+to\s+be\s+kidding|are\s+you\s+out\s+of\s+your\s+mind|what\s+were\s+you\s+thinking|who\s+does\s+that|could\s+this\s+day\s+get\s+any\s+worse|is\s+this\s+(some\s+kind\s+of\s+)?a\s+joke)\b"
]

VIOLENT_INTENT_PATTERNS = [
    # Desire/intent verbs + violent/aggressive actions
    r"\b(wanna|want\s+to|feel\s+like|feeling\s+like|dying\s+to|itching\s+to|would\s+love\s+to|wish\s+i\s+could|cant\s+wait\s+to|can\'t\s+wait\s+to|going\s+to|gonna)\s+(hit|punch|smash|slap|beat|kick|kill|choke|strangle|stab|throw|break|destroy|hurt|harm|slaughter|tackle|curb\s+stomp|wring|shoot|bash|clobber|bitch\s+slap|headbutt|dropkick)\b",
    # Violent actions targeting a person or object with an instrument/location
    r"\b(hit|punch|smash|slap|beat|kick|kill|choke|strangle|stab|throw|break|destroy|hurt|harm|slaughter|bash|clobber|bitch\s+slap|headbutt|dropkick)\s+([\w\s]+)?\s*(with\s+a|using\s+a|into\s+a|to\s+death|in\s+the\s+face|on\s+the\s+head)\b",
    # Hostile threats
    r"\b(i\s+will\s+(make\s+you\s+pay|destroy\s+you|end\s+you)|watch\s+your\s+back|you\s+will\s+regret|you\s+are\s+dead\s+to\s+me)\b"
]

SELF_HARM_PATTERNS = [
    r"\b(wanna|want\s+to|feel\s+like|wishing\s+to|going\s+to|gonna)\s+(die|end\s+it(\s+all)?|disappear|sleep\s+forever|jump\s+off|kill\s+myself|harm\s+myself)\b"
]



def clean_repeated_chars(text: str) -> str:
    if not text:
        return text
    
    result = []
    i = 0
    n = len(text)
    while i < n:
        char = text[i]
        run_len = 1
        while i + run_len < n and text[i + run_len] == char:
            run_len += 1
        
        if run_len >= 3:
            char_lower = char.lower()
            if char_lower in ALLOWED_DOUBLES:
                result.append(char * 2)
            else:
                result.append(char)
        else:
            result.append(char * run_len)
            
        i += run_len
    return "".join(result)


def clean_repeated_punctuation(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'!{3,}', '!!', text)
    text = re.sub(r'\?{3,}', '??', text)
    text = re.sub(r'\.{4,}', '...', text)
    return text


def case_preserved_replace(text: str, dictionary: dict) -> str:
    for key, value in dictionary.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        
        def replace_match(match):
            matched_text = match.group(0)
            if matched_text.isupper():
                return value.upper()
            if matched_text[0].isupper():
                return value.capitalize()
            return value
        
        text = re.sub(pattern, replace_match, text, flags=re.IGNORECASE)
    return text


def normalize_text(text: str) -> str:
    """
    Standard preprocessing and text normalization pipeline.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Normalize unicode curly quotes, apostrophes, accents, and dashes
    text = text.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    text = text.replace('`', "'").replace('´', "'").replace('—', ' - ').replace('–', ' - ')
    
    # 2. Basic space collapsing
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    
    # 3. Repeated punctuation & character collapse
    text = clean_repeated_punctuation(text)
    text = clean_repeated_chars(text)
    
    # 4. Expansion of contractions & slang
    text = case_preserved_replace(text, CONTRACTIONS)
    text = case_preserved_replace(text, SLANG_MAP)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def check_semantic_incongruity(text_lower: str) -> bool:
    """
    Detects generalized semantic incongruity (sarcasm) by checking if strong positive sentiment
    words co-occur with negative situation/late/failure indicators without a genuine contrastive
    conjunction ('but', 'however', 'although', 'except').
    """
    has_positive = any(re.search(r'\b' + re.escape(pos) + r'\b', text_lower) for pos in POSITIVE_SENTIMENT_TOKENS)
    has_negative = any(re.search(r'\b' + re.escape(neg) + r'\b', text_lower) for neg in NEGATIVE_SITUATION_TOKENS)
    
    # Also check time delays / afterthought phrases like "X weeks/days/hours later", "after everything"
    has_delay = bool(re.search(r'\b(\d+|two|three|four|five|six|several|a few)?\s*(hours?|days?|weeks?|months?|years?)\s+later\b', text_lower))
    has_too_late = bool(re.search(r'\b(too late|after (the fact|it was over|everything|i (already|finished)))\b', text_lower))
    
    if (has_positive and (has_negative or has_delay or has_too_late)):
        # If it's a genuine contrast like "I am sad but glad you came", check conjunction
        if re.search(r'\b(but|however|although)\s+(i|we)\b', text_lower):
            return False
        return True
    return False


def analyze_pragmatics(original_text: str, normalized_text: str) -> dict:
    """
    Deep pragmatic analyzer that extracts indirect language traits:
    - Sarcasm & Irony (via Semantic Incongruity & Trope Matching)
    - Idiomatic & Metaphorical nuances (50+ catalogued expressions)
    - Passive-aggressive & subdued compliance
    - Rhetorical questioning & disbelief
    - Linguistic intensity signals (capitalization, punctuation, intensifiers)
    """
    findings = {
        "is_indirect": False,
        "sarcasm_detected": False,
        "idiom_matched": None,
        "passive_aggressive": False,
        "rhetorical_detected": False,
        "signals": [],
        "boost_emotions": {},
        "suppress_emotions": [],
        "pragmatic_notes": []
    }
    
    combined_lower = (original_text + " " + normalized_text).lower()
    
    # 1. Surface syntactic signals
    if re.search(r'(?i)(.)\1{2,}', original_text):
        findings["signals"].append("Repeated Characters")
        
    words = re.findall(r'\b\w+\b', original_text)
    if any(w.isupper() and len(w) >= 2 for w in words):
        findings["signals"].append("Capitalization (Shouting)")
        
    if re.search(r'[!?]{2,}', original_text):
        findings["signals"].append("Strong Punctuation")
        
    intensifiers = {"so", "very", "extremely", "really", "incredibly", "totally", "absolutely", "too", "sooo", "soooo"}
    original_words_lower = set(w.lower() for w in re.findall(r"\b[\w']+\b", original_text))
    if any(i in original_words_lower for i in intensifiers):
        findings["signals"].append("Intensifier")
        
    # 2. Check Sarcastic Tropes
    for spat in SARCASTIC_PHRASES:
        if re.search(spat, combined_lower, re.IGNORECASE):
            findings["is_indirect"] = True
            findings["sarcasm_detected"] = True
            findings["signals"].append("Sarcasm / Irony")
            findings["pragmatic_notes"].append("Sarcastic trope / ironical phrasing detected.")
            findings["boost_emotions"].update({"annoyance": 0.88, "disapproval": 0.80, "disappointment": 0.65})
            findings["suppress_emotions"].extend(ALL_POSITIVE_EMOTIONS)
            break
            
    # 3. Check Generalized Semantic Incongruity (Positive praise + Adverse/Late condition)
    if not findings["sarcasm_detected"] and check_semantic_incongruity(combined_lower):
        findings["is_indirect"] = True
        findings["sarcasm_detected"] = True
        findings["signals"].append("Sarcasm / Irony (Incongruity)")
        findings["pragmatic_notes"].append("Positive surface wording inverted due to adverse or delayed situational context.")
        findings["boost_emotions"].update({"annoyance": 0.88, "disapproval": 0.80, "disappointment": 0.65})
        findings["suppress_emotions"].extend(ALL_POSITIVE_EMOTIONS)
        
    # 4. Check Idiomatic Patterns (50+ Expressions)
    for idiom in IDIOM_MAPPINGS:
        if re.search(idiom["pattern"], combined_lower, re.IGNORECASE):
            findings["is_indirect"] = True
            findings["idiom_matched"] = idiom["description"]
            findings["signals"].append("Idiomatic Expression")
            findings["pragmatic_notes"].append(f"Figurative expression: {idiom['description']}.")
            for emo, boost_val in idiom["boost"].items():
                findings["boost_emotions"][emo] = max(findings["boost_emotions"].get(emo, 0.0), boost_val)
            findings["suppress_emotions"].extend(idiom.get("suppress", []))
            break
            
    # 5. Check Passive-Aggressive Patterns
    for papat in PASSIVE_AGGRESSIVE_PATTERNS:
        if re.search(papat, combined_lower, re.IGNORECASE):
            findings["is_indirect"] = True
            findings["passive_aggressive"] = True
            findings["signals"].append("Passive-Aggressive Tone")
            findings["pragmatic_notes"].append("Subdued compliance with underlying grievance.")
            findings["boost_emotions"].update({"annoyance": 0.75, "disappointment": 0.65, "disapproval": 0.60})
            findings["suppress_emotions"].extend(ALL_POSITIVE_EMOTIONS)
            break
            
    # 6. Check Rhetorical Patterns
    for rpat in RHETORICAL_PATTERNS:
        if re.search(rpat, combined_lower, re.IGNORECASE):
            findings["is_indirect"] = True
            findings["rhetorical_detected"] = True
            findings["signals"].append("Rhetorical Question")
            findings["pragmatic_notes"].append("Rhetorical expression signaling shock, disbelief, or distress.")
            findings["boost_emotions"].update({"surprise": 0.75, "sadness": 0.65, "annoyance": 0.60, "confusion": 0.55})
            break

    # 7. Check Litotes / Understatements
    for lit in LITOTES_PATTERNS:
        if re.search(lit["pattern"], combined_lower, re.IGNORECASE):
            findings["is_indirect"] = True
            findings["signals"].append("Litotes / Understatement")
            findings["pragmatic_notes"].append(f"{lit['description']}.")
            for emo, boost_val in lit["boost"].items():
                findings["boost_emotions"][emo] = max(findings["boost_emotions"].get(emo, 0.0), boost_val)
            findings["suppress_emotions"].extend(lit.get("suppress", []))
            break

    # 8. Check Backhanded Compliments / Subtle Disparagement
    for bh in BACKHANDED_PATTERNS:
        if re.search(bh["pattern"], combined_lower, re.IGNORECASE):
            findings["is_indirect"] = True
            findings["signals"].append("Backhanded Remark")
            findings["pragmatic_notes"].append(f"{bh['description']}.")
            for emo, boost_val in bh["boost"].items():
                findings["boost_emotions"][emo] = max(findings["boost_emotions"].get(emo, 0.0), boost_val)
            findings["suppress_emotions"].extend(bh.get("suppress", []))
            break

    # 9. Check Violent / Hostile Intent (overrides false "desire" classification)
    for vpat in VIOLENT_INTENT_PATTERNS:
        if re.search(vpat, combined_lower, re.IGNORECASE):
            findings["is_indirect"] = True
            findings["signals"].append("Hostile / Violent Intent")
            findings["pragmatic_notes"].append("Violent action/hostile expression detected (overriding desire bias).")
            findings["boost_emotions"].update({"anger": 0.92, "annoyance": 0.75, "disapproval": 0.70})
            findings["suppress_emotions"].extend(["desire", "love", "caring", "optimism", "joy", "approval", "admiration"])
            break

    # 10. Check Self-Harm / Despair Intent (overrides false "desire" classification)
    for shpat in SELF_HARM_PATTERNS:
        if re.search(shpat, combined_lower, re.IGNORECASE):
            findings["is_indirect"] = True
            findings["signals"].append("Despair / Self-Harm Sentiment")
            findings["pragmatic_notes"].append("Despair or self-harm expression detected (overriding desire bias).")
            findings["boost_emotions"].update({"sadness": 0.90, "grief": 0.85, "disappointment": 0.70})
            findings["suppress_emotions"].extend(["desire", "optimism", "joy", "approval", "pride"])
            break

    return findings



