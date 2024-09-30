from flask import Flask, render_template, request

app = Flask(__name__)

# Simple synonym dictionary
synonyms = {
    "happy": ["joyful", "content", "pleased"],
    "play": ["participate", "engage", "perform"],
    "good": ["great", "excellent", "superb"],
    "game": ["match", "competition", "event"]
}

def paraphrase_sentence(sentence):
    words = sentence.split()
    paraphrased = []

    for word in words:
        if word in synonyms:
            paraphrased.append(synonyms[word][0])  # Just use the first synonym for simplicity
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
            variations = [paraphrase_sentence(sentence) for _ in range(3)]

    return render_template('index.html', sentence=sentence, variations=variations, error=error)

if __name__ == '__main__':
    app.run(debug=True)

