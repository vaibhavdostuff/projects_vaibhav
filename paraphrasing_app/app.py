from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import csv
import os

app = Flask(__name__)

# -------------------------------
# MODEL LOAD
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
    return " ".join([replacements.get(w.lower(), w) for w in words])

# -------------------------------
# OPTIONAL AI NORMALIZATION (SAFE)
# -------------------------------
def normalize_input(text):

    prompt = f"""
Fix grammar of this sentence without changing meaning:

{text}
"""

    encoding = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)

    output = model.generate(
        input_ids=encoding["input_ids"].to(device),
        attention_mask=encoding["attention_mask"].to(device),
        max_length=80,
        do_sample=False
    )

    fixed = tokenizer.decode(output[0], skip_special_tokens=True)

    # Safety fallback
    if len(fixed.split()) < 3:
        return text

    return fixed

# -------------------------------
# GRAMMAR FIX (LIGHT POST FIX)
# -------------------------------
def grammar_fix(text):
    text = text.replace("i and my friends", "my friends and I")
    text = text.replace("me and my friends", "my friends and I")
    text = text.replace(" .", ".").replace(" ,", ",")
    text = text.strip()

    return text[0].upper() + text[1:] if len(text) > 1 else text

# -------------------------------
# SIMILARITY CHECK
# -------------------------------
def is_too_similar(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    return len(a_words & b_words) / max(len(b_words), 1) > 0.6

# -------------------------------
# QUALITY CHECK
# -------------------------------
def is_good_sentence(text, original):

    if len(text.split()) < 6:
        return False

    if text.lower() == original.lower():
        return False

    if is_too_similar(text, original):
        return False

    if len(text.split()) < len(original.split()) * 0.7:
        return False

    return True

# -------------------------------
# SCORING FUNCTION
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
# GENERATION
# -------------------------------
def generate_text(prompt):

    encoding = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)

    outputs = model.generate(
        input_ids=encoding["input_ids"].to(device),
        attention_mask=encoding["attention_mask"].to(device),
        max_length=120,
        do_sample=True,
        top_k=50,
        top_p=0.9,
        temperature=0.8,
        repetition_penalty=2.0,
        no_repeat_ngram_size=3,
        num_return_sequences=5
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
        if is_good_sentence(c, original):
            if not any(is_too_similar(c, v) for v in valid):
                valid.append(c)

    # fallback
    if not valid:
        valid = [c for c in candidates if len(c.split()) >= 5 and c.lower() != original.lower()]

    if not valid:
        return "Could not generate"

    return sorted(valid, key=score_sentence, reverse=True)[0]

# -------------------------------
# SAVE DATA (STYLE-AWARE)
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
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Input", "Output", "Style", "Quality"])

        for o, s in zip(outputs, styles):
            if o != "Could not generate" and (input_text, o) not in existing:
                writer.writerow([input_text, o, s, "unrated"])

# -------------------------------
# UPDATE QUALITY
# -------------------------------
def update_quality(input_text, output_text, quality):

    file_path = os.path.join(os.path.dirname(__file__), "data.csv")

    with open(file_path, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    for i in range(1, len(rows)):
        if rows[i][0] == input_text and rows[i][1] == output_text:
            rows[i][3] = quality

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

# -------------------------------
# MAIN PARAPHRASE FUNCTION
# -------------------------------
def paraphrase(text):

    clean = clean_text(text)

    # 🔥 OPTIONAL: only normalize VERY bad input
    if len(text.split()) < 6:
        clean = normalize_input(clean)

    # STYLE PROMPTS (aligned with training)
    prompt_formal = f"Paraphrase in formal tone: {clean}"
    prompt_expressive = f"Paraphrase in expressive tone: {clean}"
    prompt_casual = f"Paraphrase in casual tone: {text}"

    p1 = generate_text(prompt_formal)
    p2 = generate_text(prompt_expressive)
    p3 = generate_text(prompt_casual)

    out1 = select_best(p1, clean)
    out2 = select_best(p2, clean)
    out3 = select_best(p3, clean)

    outputs = [out1, out2, out3]
    styles = ["formal", "expressive", "casual"]

    save_data(text, outputs, styles)

    return outputs

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
        "paraphrased_texts": results,
        "styles": ["formal", "expressive", "casual"]
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