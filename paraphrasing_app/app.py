from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import csv
import os

app = Flask(__name__)

# -------------------------------
# MODEL
# -------------------------------
MODEL_PATH = "./my_paraphrase_model" if os.path.exists("./my_paraphrase_model") else "google/flan-t5-large"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_PATH,
    low_cpu_mem_usage=True
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()

# -------------------------------
# INPUT CLEANING
# -------------------------------
def clean_text(text):
    text = text.strip()

    replacements = {
        "tmrw": "tomorrow",
        "tmr": "tomorrow",
        "frnds": "friends",
        "pls": "please",
        "plz": "please"
    }

    words = text.split()
    new_words = [replacements.get(w.lower(), w) for w in words]

    return " ".join(new_words)

# -------------------------------
# GRAMMAR FIX
# -------------------------------
def grammar_fix(text):
    text = text.replace("i and my friends", "my friends and I")
    text = text.replace("me and my friends", "my friends and I")
    text = text.replace(" .", ".").replace(" ,", ",")
    text = text.strip()

    return text[0].upper() + text[1:] if len(text) > 1 else text

# -------------------------------
# SIMILARITY
# -------------------------------
def is_too_similar(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    similarity = len(a_words & b_words) / max(len(b_words), 1)
    return similarity > 0.6

# -------------------------------
# QUALITY CHECK
# -------------------------------
def is_good_sentence(text, original):

    if len(text.split()) < 6:
        return False

    if text.lower().strip() == original.lower().strip():
        return False

    if is_too_similar(text, original):
        return False

    if len(text.split()) < len(original.split()) * 0.7:
        return False

    return True

# -------------------------------
# SCORING
# -------------------------------
def score_sentence(text):
    score = len(text.split())

    if "." in text:
        score += 2

    words = text.lower().split()
    if len(words) != len(set(words)):
        score -= 3

    return score

# -------------------------------
# GENERATE TEXT
# -------------------------------
def generate_text(prompt):

    encoding = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=150,
        do_sample=True,
        top_k=50,
        top_p=0.92,
        temperature=0.9,
        repetition_penalty=2.2,
        no_repeat_ngram_size=3,
        num_return_sequences=6
    )

    texts = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    cleaned = []
    for t in texts:
        t = grammar_fix(t)
        if t not in cleaned:
            cleaned.append(t)

    return cleaned

# -------------------------------
# SELECT BEST
# -------------------------------
def select_best(candidates, original):

    valid = []

    for c in candidates:
        if c.strip().lower() == original.strip().lower():
            continue

        if is_good_sentence(c, original):
            if not any(is_too_similar(c, v) for v in valid):
                valid.append(c)

    if not valid:
        for c in candidates:
            if len(c.split()) >= 5 and c.lower() != original.lower():
                valid.append(c)

    if not valid:
        return "Could not generate"

    scored = [(c, score_sentence(c)) for c in valid]
    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[0][0]

# -------------------------------
# SAVE DATA (UPDATED)
# -------------------------------
def save_data(input_text, outputs, styles):

    file_path = os.path.join(os.path.dirname(__file__), "data.csv")
    file_exists = os.path.isfile(file_path)

    existing = set()
    if file_exists:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    existing.add((row[0], row[1]))

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        if not file_exists:
            writer.writerow(["Input", "Output", "Style", "Quality"])

        for o, s in zip(outputs, styles):
            if (
                o != "Could not generate"
                and len(o.split()) > 5
                and o.strip() != ""
                and o.lower() != input_text.lower()
                and (input_text, o) not in existing
            ):
                writer.writerow([input_text, o, s, "unrated"])

# -------------------------------
# UPDATE RATING
# -------------------------------
def update_quality(input_text, output_text, quality):

    file_path = os.path.join(os.path.dirname(__file__), "data.csv")

    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    for i in range(1, len(rows)):
        if rows[i][0] == input_text and rows[i][1] == output_text:
            rows[i][3] = quality

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# -------------------------------
# MAIN FUNCTION
# -------------------------------
def paraphrase(text):

    clean = clean_text(text)

    formal_input = clean.replace(" u ", " you ").replace(" wanna ", " want to ")
    expressive_input = clean
    casual_input = text

    prompt1 = f"""Rewrite the sentence in a formal and professional tone.
Sentence: {formal_input}"""

    prompt2 = f"""Rewrite the sentence in an expressive and engaging way.
Sentence: {expressive_input}"""

    prompt3 = f"""Rewrite the sentence in a casual and conversational tone.
Sentence: {casual_input}"""

    p1 = generate_text(prompt1)
    p2 = generate_text(prompt2)
    p3 = generate_text(prompt3)

    out1 = select_best(p1, clean)
    out2 = select_best(p2, clean)
    out3 = select_best(p3, clean)

    results = [out1, out2, out3]
    styles = ["formal", "expressive", "casual"]

    save_data(text, results, styles)

    return results

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

    results = paraphrase(text)

    return jsonify({
        'paraphrased_texts': results,
        'styles': ["formal", "expressive", "casual"]
    })

@app.route('/api/rate', methods=['POST'])
def rate():
    data = request.get_json()

    update_quality(
        data.get("input"),
        data.get("output"),
        data.get("quality")
    )

    return jsonify({"message": "Rating saved"})

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)