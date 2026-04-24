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

    # Minimal normalization (DO NOT kill personality)
    replacements = {
        "tmrw": "tomorrow",
        "tmr": "tomorrow",
        "frnds": "friends",
        "pls": "please",
        "plz": "please"
    }

    words = text.split()
    new_words = []

    for w in words:
        lw = w.lower()
        if lw in replacements:
            new_words.append(replacements[lw])
        else:
            new_words.append(w)

    text = " ".join(new_words)

    return text

# -------------------------------
# AI NORMALIZATION (SMART FIX)
# -------------------------------
def normalize_input(text):

    prompt = f"""
    Rewrite the following sentence correctly.

    Rules:
    - Keep the SAME meaning
    - Do NOT add new information
    - Do NOT explain anything
    - Only return the corrected sentence

    Sentence: {text}
    """

    encoding = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=80,
        do_sample=False
    )

    fixed = tokenizer.decode(output[0], skip_special_tokens=True)

    # 🔥 SAFETY CHECK
    if "correct grammar" in fixed.lower():
        return text

    return fixed

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

    if len(text.split()) < 6:
        return False

    if text.lower() == original.lower():
        return False

    if is_too_similar(text, original):
        return False

    if "i and my friends" in text.lower():
        return False

    # Prevent incomplete meaning
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
# SAVE DATA (CLEAN + NO DUPLICATES)
# -------------------------------
def save_data(input_text, outputs):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data.csv")

    file_exists = os.path.isfile(file_path)

    # Load existing outputs to prevent duplicates across runs
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
            writer.writerow(["Input", "Output", "Quality"])

        for o in outputs:
            if (
                o != "Could not generate" and
                len(o.split()) > 5 and
                o.strip() != "" and
                (input_text, o) not in existing
            ):
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

    # -------------------------------
    # INPUT HANDLING
    # -------------------------------
    clean = clean_text(text)

    # ❌ DO NOT globally normalize (this was breaking outputs)
    # clean = normalize_input(clean)   ← REMOVE THIS

    # ✅ Style-based inputs
    formal_input = clean.replace(" u ", " you ").replace(" wanna ", " want to ")
    expressive_input = clean
    casual_input = text  # raw input = best for natural tone

    # -------------------------------
    # PROMPTS (IMPROVED)
    # -------------------------------

    prompt1 = f"""
    Rewrite the sentence in a formal and professional tone.

    Requirements:
    - Fix grammar mistakes
    - Do not remove any important information
    - Preserve full meaning
    - Improve clarity and structure
    - Make it sound professional

    Sentence: {formal_input}
    """

    prompt2 = f"""
    Rewrite the sentence in an expressive and engaging way.

    Requirements:
    - Preserve full meaning
    - Use richer vocabulary
    - Add natural variation in structure
    - Make it more interesting and descriptive

    Sentence: {expressive_input}
    """

    prompt3 = f"""
    Rewrite the sentence in a casual and conversational tone.

    Requirements:
    - Keep it natural and human-like
    - Slight slang is allowed
    - Preserve meaning
    - Do not make it overly formal

    Sentence: {casual_input}
    """

    # -------------------------------
    # GENERATION
    # -------------------------------
    p1_list = generate_text(prompt1)
    p2_list = generate_text(prompt2)
    p3_list = generate_text(prompt3)

    # -------------------------------
    # LIGHT GRAMMAR FIX (SAFE)
    # -------------------------------
    p1_list = [grammar_fix(t) for t in p1_list]
    p2_list = [grammar_fix(t) for t in p2_list]
    p3_list = [grammar_fix(t) for t in p3_list]

    # -------------------------------
    # SELECT BEST
    # -------------------------------
    def select_best(candidates, original):

        valid = []

        for c in candidates:
            if is_good_sentence(c, original):
                if not any(is_too_similar(c, v) for v in valid):
                    valid.append(c)

        # 🔄 fallback (important for tough sentences)
        if not valid:
            for c in candidates:
                if len(c.split()) >= 5 and c.lower() != original.lower():
                    valid.append(c)

        if not valid:
            return "Could not generate"

        scored = [(c, score_sentence(c)) for c in valid]
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored[0][0]

    final_results = [
        select_best(p1_list, clean),   # Professional
        select_best(p2_list, clean),   # Expressive
        select_best(p3_list, clean)    # Casual
    ]

    # -------------------------------
    # SAVE DATA (IMPORTANT)
    # -------------------------------
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