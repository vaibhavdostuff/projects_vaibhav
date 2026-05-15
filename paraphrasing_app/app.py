from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import csv
import os
import re

app = Flask(__name__)

# =========================================================
# MODEL SETUP
# =========================================================

MODEL_PATH = (
    "./my_paraphrase_model"
    if os.path.exists("./my_paraphrase_model")
    else "google/flan-t5-large"
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_PATH,
    low_cpu_mem_usage=True
)

device = "cuda" if torch.cuda.is_available() else "cpu"

model = model.to(device)
model.eval()

# =========================================================
# INPUT CLEANING
# =========================================================

def clean_text(text):

    text = text.strip()

    replacements = {
        "tmrw": "tomorrow",
        "tmr": "tomorrow",
        "frnds": "friends",
        "pls": "please",
        "plz": "please",
        "u": "you",
        "ur": "your"
    }

    words = text.split()
    cleaned_words = []

    for w in words:

        lw = w.lower()

        if lw in replacements:
            cleaned_words.append(replacements[lw])
        else:
            cleaned_words.append(w)

    text = " ".join(cleaned_words)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# =========================================================
# BASIC GRAMMAR FIX
# =========================================================

def grammar_fix(text):

    text = text.strip()

    fixes = {
        "i and my friends": "my friends and I",
        "me and my friends": "my friends and I",
        " .": ".",
        " ,": ",",
        " !": "!",
        " ?": "?",
        "  ": " "
    }

    for k, v in fixes.items():
        text = text.replace(k, v)

    # capitalize first letter
    if len(text) > 1:
        text = text[0].upper() + text[1:]

    return text

# =========================================================
# SIMILARITY CHECK
# =========================================================

def is_too_similar(a, b):

    a_words = set(a.lower().split())
    b_words = set(b.lower().split())

    overlap = len(a_words & b_words)
    similarity = overlap / max(len(b_words), 1)

    return similarity > 0.82

# =========================================================
# QUALITY CHECK
# =========================================================

def is_good_sentence(text, original):

    if not text:
        return False

    if len(text.split()) < 5:
        return False

    if text.lower() == original.lower():
        return False

    if is_too_similar(text, original):
        return False

    if len(text.split()) < len(original.split()) * 0.60:
        return False

    if "i and my friends" in text.lower():
        return False

    return True

# =========================================================
# MAIN SCORING
# =========================================================

def score_sentence(text):

    score = 0

    words = text.lower().split()

    # good length
    if 8 <= len(words) <= 35:
        score += 4

    # punctuation
    if "." in text:
        score += 1

    if "," in text:
        score += 1

    # vocabulary diversity
    unique_ratio = len(set(words)) / max(len(words), 1)

    score += unique_ratio * 5

    # repetition penalty
    if len(words) != len(set(words)):
        score -= 2

    return score

# =========================================================
# STYLE MATCHING
# =========================================================

def style_match_score(text, style):

    text = text.lower()

    formal_words = [
        "therefore",
        "however",
        "furthermore",
        "significantly",
        "professional",
        "management",
        "organization",
        "consequently",
        "ultimately"
    ]

    expressive_words = [
        "deeply",
        "remarkable",
        "incredible",
        "beautiful",
        "powerful",
        "emotional",
        "immersive",
        "vivid",
        "heartfelt"
    ]

    casual_words = [
        "really",
        "pretty",
        "kinda",
        "gonna",
        "wanna",
        "stuff",
        "cool",
        "totally"
    ]

    if style == "formal":
        return sum(word in text for word in formal_words)

    elif style == "expressive":
        return sum(word in text for word in expressive_words)

    elif style == "casual":
        return sum(word in text for word in casual_words)

    return 0

# =========================================================
# CSV SAVE
# =========================================================

def save_data(input_text, outputs, styles):

    base_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(base_dir, "data.csv")

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

        for output, style in zip(outputs, styles):

            if (
                output != "Could not generate"
                and output.strip() != ""
                and len(output.split()) >= 5
                and (input_text, output) not in existing
            ):

                writer.writerow([
                    input_text,
                    output,
                    style,
                    "unrated"
                ])

# =========================================================
# UPDATE QUALITY
# =========================================================

def update_quality(input_text, output_text, quality):

    base_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(base_dir, "data.csv")

    rows = []

    with open(file_path, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    for i in range(1, len(rows)):

        if len(rows[i]) < 4:
            continue

        if (
            rows[i][0] == input_text
            and rows[i][1] == output_text
        ):

            rows[i][3] = quality

    with open(file_path, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)
        writer.writerows(rows)

# =========================================================
# TEXT GENERATION
# =========================================================

def generate_text(
    prompt,
    temperature=1.0,
    top_p=0.92,
    top_k=50,
    num_return_sequences=6
):

    encoding = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,

        max_length=220,

        do_sample=True,

        top_k=top_k,
        top_p=top_p,
        temperature=temperature,

        repetition_penalty=2.3,
        no_repeat_ngram_size=3,

        num_return_sequences=num_return_sequences,

        early_stopping=True
    )

    texts = tokenizer.batch_decode(
        outputs,
        skip_special_tokens=True
    )

    cleaned = []

    for t in texts:

        t = grammar_fix(t)

        if t not in cleaned:
            cleaned.append(t)

    return cleaned

# =========================================================
# BEST OUTPUT SELECTOR
# =========================================================

def select_best(candidates, original, style):

    valid = []

    for c in candidates:

        if is_good_sentence(c, original):

            duplicate = False

            for v in valid:

                if is_too_similar(c, v):
                    duplicate = True
                    break

            if not duplicate:
                valid.append(c)

    # fallback
    if not valid:

        for c in candidates:

            if (
                len(c.split()) >= 5
                and c.lower() != original.lower()
            ):

                valid.append(c)

    if not valid:
        return "Could not generate"

    scored = []

    for c in valid:

        final_score = (
            score_sentence(c)
            + style_match_score(c, style)
        )

        scored.append((c, final_score))

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scored[0][0]

# =========================================================
# MAIN PARAPHRASE
# =========================================================

def paraphrase(text):

    clean = clean_text(text)

    # -----------------------------------------------------
    # STYLE INPUTS
    # -----------------------------------------------------

    formal_input = clean
    expressive_input = clean
    casual_input = text

    # -----------------------------------------------------
    # FORMAL
    # -----------------------------------------------------

    prompt1 = f"""
    Rewrite the sentence in a highly formal,
    professional, polished, and sophisticated tone.

    Requirements:
    - Improve grammar significantly
    - Use refined vocabulary
    - Improve structure and readability
    - Make it sound executive or academic
    - Preserve the exact original meaning
    - Avoid casual wording

    Sentence:
    {formal_input}
    """

    # -----------------------------------------------------
    # EXPRESSIVE
    # -----------------------------------------------------

    prompt2 = f"""
    Rewrite the sentence in a vivid,
    emotionally expressive, and engaging style.

    Requirements:
    - Make the sentence feel immersive
    - Use richer and more descriptive wording
    - Add emotional depth naturally
    - Make it sound human and dynamic
    - Preserve the original meaning

    Sentence:
    {expressive_input}
    """

    # -----------------------------------------------------
    # CASUAL
    # -----------------------------------------------------

    prompt3 = f"""
    Rewrite the sentence in a relaxed,
    casual conversational tone.

    Requirements:
    - Sound natural and human
    - Use simple everyday wording
    - Make it smooth and friendly
    - Avoid sophisticated vocabulary
    - Preserve the exact meaning

    Sentence:
    {casual_input}
    """

    # =====================================================
    # GENERATE
    # =====================================================

    p1_list = generate_text(
        prompt1,
        temperature=0.72,
        top_p=0.88,
        num_return_sequences=6
    )

    p2_list = generate_text(
        prompt2,
        temperature=1.15,
        top_p=0.95,
        num_return_sequences=6
    )

    p3_list = generate_text(
        prompt3,
        temperature=0.95,
        top_p=0.90,
        num_return_sequences=6
    )

    # =====================================================
    # FINAL RESULTS
    # =====================================================

    final_results = [

        select_best(
            p1_list,
            clean,
            "formal"
        ),

        select_best(
            p2_list,
            clean,
            "expressive"
        ),

        select_best(
            p3_list,
            clean,
            "casual"
        )
    ]

    styles = [
        "formal",
        "expressive",
        "casual"
    ]

    save_data(
        text,
        final_results,
        styles
    )

    return final_results

# =========================================================
# ROUTES
# =========================================================

@app.route('/')
def index():
    return render_template('index.html')

# =========================================================
# API PARAPHRASE
# =========================================================

@app.route('/api/paraphrase', methods=['POST'])
def api_paraphrase():

    data = request.get_json()

    text = data.get('text', '').strip()

    if not text:

        return jsonify({
            "error": "No text provided"
        }), 400

    results = paraphrase(text)

    return jsonify({
        "paraphrased_texts": results,
        "styles": [
            "formal",
            "expressive",
            "casual"
        ]
    })

# =========================================================
# API RATE
# =========================================================

@app.route('/api/rate', methods=['POST'])
def rate():

    data = request.get_json()

    update_quality(
        data.get("input"),
        data.get("output"),
        data.get("quality")
    )

    return jsonify({
        "message": "Rating saved"
    })

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )