from flask import Flask, render_template, request

app = Flask(__name__)

# Simple synonym dictionary
synonyms = {
    
    "happy": ["joyful", "content", "pleased", "cheerful", "delighted", "blissful"],
    "sad": ["unhappy", "downcast", "miserable", "sorrowful", "depressed", "melancholy"],
    "play": ["participate", "engage", "perform", "compete", "act", "entertain"],
    "good": ["great", "excellent", "superb", "wonderful", "favorable", "admirable"],
    "bad": ["awful", "terrible", "poor", "inferior", "unpleasant", "dreadful"],
    "game": ["match", "competition", "event", "tournament", "contest", "challenge"],
    "run": ["sprint", "jog", "dash", "race", "hasten", "move quickly"],
    "eat": ["consume", "devour", "ingest", "dine", "feast", "partake"],
    "fast": ["quick", "rapid", "swift", "speedy", "brisk", "hurried"],
    "slow": ["lethargic", "sluggish", "unhurried", "delayed", "lazy", "tardy"],
    "smart": ["intelligent", "clever", "bright", "brilliant", "wise", "knowledgeable"],
    "strong": ["powerful", "sturdy", "robust", "mighty", "tough", "resilient"],
    "weak": ["fragile", "feeble", "delicate", "frail", "vulnerable", "infirm"],
    "speak": ["talk", "converse", "communicate", "chat", "utter", "address"],
    "think": ["ponder", "reflect", "consider", "contemplate", "believe", "assume"],
    "beautiful": ["gorgeous", "stunning", "lovely", "attractive", "charming", "radiant"],
    "ugly": ["unattractive", "hideous", "unsightly", "displeasing", "gross", "repulsive"],
    "start": ["begin", "commence", "initiate", "launch", "embark", "undertake"],
    "end": ["finish", "complete", "conclude", "terminate", "wrap up", "close"],
    "small": ["tiny", "petite", "miniature", "little", "compact", "diminutive"],
    "big": ["large", "huge", "massive", "gigantic", "colossal", "immense"],
    "hot": ["warm", "scorching", "blazing", "boiling", "sweltering", "heated"],
    "cold": ["chilly", "freezing", "frigid", "cool", "icy", "frosty"],
    "angry": ["furious", "irritated", "mad", "enraged", "livid", "infuriated"],
    "calm": ["serene", "peaceful", "composed", "tranquil", "relaxed", "collected"],
    "walk": ["stroll", "saunter", "wander", "amble", "stride", "trek"],
    "jump": ["leap", "bound", "spring", "hop", "vault", "bounce"],
    "love": ["adore", "cherish", "admire", "appreciate", "care for", "treasure"],
    "hate": ["detest", "loathe", "despise", "dislike", "abhor", "resent"],
    "talk": ["speak", "converse", "discuss", "communicate", "chat", "articulate"],
    "listen": ["hear", "attend", "harken", "heed", "take in", "pay attention"],
    "work": ["labor", "toil", "operate", "function", "perform", "endeavor"],
    "sleep": ["rest", "slumber", "doze", "nap", "snooze", "hibernate"],
    "friend": ["companion", "buddy", "pal", "mate", "ally", "acquaintance"],
    "enemy": ["foe", "opponent", "rival", "adversary", "antagonist", "challenger"],
    "win": ["triumph", "succeed", "prevail", "conquer", "dominate", "achieve victory"],
    "lose": ["fail", "fall short", "be defeated", "be bested", "succumb", "surrender"]

}
def paraphrase_sentence(sentence):
    words = sentence.split()
    paraphrased = []

    for word in words:
        if word in synonyms:
            paraphrased.append(synonyms[word][1])   # Just use the first synonym for simplicity
        else:
            paraphrased.append(word)

    return ' '.join(paraphrased)

@app.route('/', methods=['GET', 'POST'])
def paraphrase():
    sentence = ''
    variations = []
    error = None

    if request.method == 'POST':
        sentence = request.form.get('sentence')

        if not sentence:
            error = 'Please enter a sentence.'
        else:
            # Generate paraphrased versions using basic synonym replacement
            variations = [paraphrase_sentence(sentence) for _ in range(2)]

    return render_template('index.html', sentence=sentence, variations=variations, error=error)

if __name__ == '__main__':
    app.run(debug=True)

