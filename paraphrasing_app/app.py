from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import csv
import os

app = Flask(__name__)

# -------------------------------
# MODEL ((USE CUSTOM IF EXISTS)
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
# SCORING FUNCTION
# -------------------------------
def score_sentence(text):
    score = len(text.split())
    if "." in text:
        score += 2
    if len(set(text.split())) != len(text.split()):
        score -= 3
    return score


# -------------------------------
# FIXED SAVE DATA (ALWAYS PROJECT FOLDER)
# -------------------------------
def save_data(input_text, outputs):

    # Get absolute path of current file (app.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Create full path inside project folder
    file_path = os.path.join(base_dir, "data.csv")

    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["input", "output", "quality"])

        for o in outputs:
            writer.writerow([input_text, o, "unrated"])

# -------------------------------
# UPDATE QUALITY (RATING API)
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
        max_length=80,
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
# MAIN PARAPHRASE FUNCTION
# -------------------------------
def paraphrase(text):

    clean = clean_text(text)

    # -------------------------------
    # PROMPTS (3 STYLES)
    # -------------------------------
    prompt1 = f"""
    Paraphrase this sentence professionally.
    Keep it grammatically correct and clear.

    Sentence: {clean}
    """

    prompt2 = f"""
    Rewrite this sentence in a more expressive and engaging way.
    Use richer vocabulary.

    Sentence: {clean}
    """

    prompt3 = f"""
    Rewrite this sentence in a casual and friendly tone.
    Make it informal and conversational.

    Sentence: {clean}
    """

    # Generate multiple candidates per style
    p1_list = generate_text(prompt1)
    p2_list = generate_text(prompt2)
    p3_list = generate_text(prompt3)

    # -------------------------------
    # FILTER + SELECT BEST
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
        select_best(p1_list),  # Professional
        select_best(p2_list),  # Expressive
        select_best(p3_list)   # Casual
    ]

    # Save for improvement
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

# ⭐ NEW: RATING API
@app.route('/api/rate', methods=['POST'])
def rate():
    data = request.get_json()
    input_text = data.get("input")
    output_text = data.get("output")
    quality = data.get("quality")  # good / bad

    update_quality(input_text, output_text, quality)

    return jsonify({"message": "Rating saved"})


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__": 
    app.run(debug=True)
