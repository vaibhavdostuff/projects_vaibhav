from flask import Flask, render_template, request
import random
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

# Load model and tokenizer
model_name = 't5-base'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def set_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def paraphrase(text):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            max_length=60,
            num_return_sequences=3,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=1.5
        )
    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]


@app.route('/', methods=['GET', 'POST'])
def index():
    paraphrased_texts = []
    if request.method == 'POST':
        text = request.form['text']
        set_seed(42)
        paraphrased_texts = paraphrase(text)
        return render_template('index.html', paraphrased_texts=paraphrased_texts)

if __name__ == "__main__":
    app.run(debug=True)

