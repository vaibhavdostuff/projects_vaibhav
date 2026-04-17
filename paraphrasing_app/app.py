from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import csv

app = Flask(__name__)

# -------------------------------
# MODEL (FLAN-T5)
# -------------------------------
model_name = "google/flan-t5-large"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()


# -------------------------------
# INPUT CLEANING
# -------------------------------
def clean_text(text):
    text = text.strip()

    replacements = {
        " u ": " you ",
        " ur ": " your ",
        " r ": " are ",
        " wanna ": " want to ",
        " gonna ": " going to "
    }

    text = " " + text.lower() + " "

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text.strip()


# -------------------------------
# GRAMMAR FIX
# -------------------------------
def grammar_fix(text):
    text = text.replace("i and my friends", "my friends and I")
    text = text.replace("me and my friends", "my friends and I")
    text = text.replace(" .", ".")
    text = text.replace(" ,", ",")
    text = text.strip()

    return text[0].upper() + text[1:] if len(text) > 1 else text


# -------------------------------
# SIMILARITY CHECK
# -------------------------------
def is_too_similar(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())

    similarity = len(a_words & b_words) / max(len(a_words), 1)
    return similarity > 0.7


# -------------------------------
# QUALITY CHECK
# -------------------------------
def is_good_sentence(text, original):
    if len(text.split()) < 6:
        return False

    if text.lower() == original.lower():
        return False

    return True


# -------------------------------
# SCORING FUNCTION (RANKING)
# -------------------------------
def score_sentence(text):
    score = 0

    score += len(text.split())  # longer = better

    if "." in text:
        score += 2

    words = text.lower().split()
    if len(words) != len(set(words)):
        score -= 3

    return score


# -------------------------------
# SAVE DATA (FOR FUTURE TRAINING)
# -------------------------------
def save_data(input_text, outputs):
    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for o in outputs:
            writer.writerow([input_text, o])


# -------------------------------
# PARAPHRASING FUNCTION
# -------------------------------
def paraphrase(text, num_return_sequences=10):

    clean = clean_text(text)

    prompt = f"""
    Rewrite the following sentence in 5 different ways.

    Requirements:
    - Keep the exact meaning
    - Use natural, fluent English
    - Use different vocabulary and sentence structure
    - Avoid repetition
    - Make sentences sound human-like

    Sentence: {clean}
    """

    encoding = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,

        max_length=80,

        do_sample=True,
        top_k=40,
        top_p=0.85,
        temperature=0.7,

        repetition_penalty=2.2,
        no_repeat_ngram_size=3,

        num_return_sequences=num_return_sequences
    )

    paraphrases = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    final_results = []

    for p in paraphrases:
        p = grammar_fix(p)

        if is_good_sentence(p, clean):
            if not any(is_too_similar(p, existing) for existing in final_results):
                final_results.append(p)

    # Ranking
    scored = [(p, score_sentence(p)) for p in final_results]
    scored.sort(key=lambda x: x[1], reverse=True)

    best = [s[0] for s in scored[:5]]

    # Save for improvement
    save_data(text, best)

    return best


# -------------------------------
# ROUTES
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/paraphrase', methods=['POST'])
def api_paraphrase():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    results = paraphrase(text)

    return jsonify({'paraphrased_texts': results})


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)