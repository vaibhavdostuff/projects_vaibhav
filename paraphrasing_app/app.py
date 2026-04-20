from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import csv
import os

app = Flask(__name__)

# -------------------------------
# MODEL (CUSTOM OR DEFAULT)
# -------------------------------
MODEL_PATH = "./my_paraphrase_model" if os.path.exists("./my_paraphrase_model") else "google/flan-t5-large"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

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

    similarity = len(a_words & b_words) / max(len(b_words), 1)
    return similarity > 0.6

# -------------------------------
# QUALITY CHECK (STRICT)
# -------------------------------
def is_good_sentence(text, original):

    # ❌ Too short
    if len(text.split()) < 6:
        return False

    # ❌ Same as input
    if text.lower() == original.lower():
        return False

    # ❌ Too similar
    if is_too_similar(text, original):
        return False

    # ❌ Bad grammar pattern
    if "i and my friends" in text.lower():
        return False

    # ❌ Incomplete meaning (VERY IMPORTANT)
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
# SAVE DATA (CSV)
# -------------------------------
def save_data(input_text, outputs):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data.csv")

    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["input", "output", "quality"])

        for o in outputs:
            writer.writerow([input_text, o, "unrated"])

# -------------------------------
# UPDATE RATING
# -------------------------------
def update_quality(input_text, output_text, quality):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data.csv")

    rows = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    for i in range(1, len(rows)):
        if rows[i][0] == input_text and rows[i][1] == output_text:
            rows[i][2] = quality

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

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
# MAIN PARAPHRASE FUNCTION
# -------------------------------
def paraphrase(text):

    clean = clean_text(text)

    # 🔥 IMPROVED PROMPTS (VERY IMPORTANT)
    prompt1 = f"""
    Rewrite the following sentence in a formal and professional tone.

    Requirements:
    - Do not remove any important information
    - Preserve all parts of the sentence
    - Keep full meaning intact
    - Improve grammar and clarity
    - Change sentence structure

    Sentence: {clean}
    """

    prompt2 = f"""
    Rewrite the following sentence in a more expressive and engaging way.

    Requirements:
    - Do not remove any important information
    - Preserve all parts of the sentence
    - Keep full meaning intact
    - Use richer vocabulary
    - Make it more descriptive

    Sentence: {clean}
    """

    prompt3 = f"""
    Rewrite the following sentence in a casual and conversational tone.

    Requirements:
    - Do not remove any important information
    - Preserve all parts of the sentence
    - Keep full meaning intact
    - Make it friendly and natural
    - Slight slang allowed

    Sentence: {clean}
    """

    # Generate candidates
    p1_list = generate_text(prompt1)
    p2_list = generate_text(prompt2)
    p3_list = generate_text(prompt3)

    # -------------------------------
    # SELECT BEST
    # -------------------------------
    def select_best(candidates):
        valid = []

        for c in candidates:
            if is_good_sentence(c, clean):
                if not any(is_too_similar(c, v) for v in valid):
                    valid.append(c)

        scored = [(c, score_sentence(c)) for c in valid]
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored[0][0] if scored else "Could not generate"

    final_results = [
        select_best(p1_list),
        select_best(p2_list),
        select_best(p3_list)
    ]

    # Save data
    save_data(text, final_results)

    return final_results

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
    return jsonify({'paraphrased_texts': results})

# ⭐ RATING API
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