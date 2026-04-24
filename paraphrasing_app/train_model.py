from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments

# -------------------------------
# MODEL
# -------------------------------
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name,
    low_cpu_mem_usage=True   # ✅ memory fix
)

# -------------------------------
# LOAD DATA
# -------------------------------
dataset = load_dataset("csv", data_files="data.csv")

# ✅ ONLY TRAIN ON GOOD DATA
dataset = dataset["train"].filter(lambda x: x["quality"] == "good")

# -------------------------------
# PREPROCESS (IMPORTANT FIX)
# -------------------------------
def preprocess(example):

    inputs = []
    targets = []

    for inp, out in zip(example["input"], example["output"]):

        # 🔥 MUCH BETTER PROMPT
        prompt = f"""
Paraphrase the following sentence while keeping the meaning the same.
Improve grammar and clarity if needed.

Sentence: {inp}
"""

        inputs.append(prompt)
        targets.append(out)

    # Tokenize inputs
    model_inputs = tokenizer(
        inputs,
        max_length=128,
        truncation=True,
        padding="max_length"
    )

    # Tokenize outputs
    labels = tokenizer(
        targets,
        max_length=128,
        truncation=True,
        padding="max_length"
    )

    # -------------------------------
    # ✅ CRITICAL FIX (VERY IMPORTANT)
    # -------------------------------
    label_ids = labels["input_ids"]

    # Replace padding token id with -100
    label_ids = [
        [(token if token != tokenizer.pad_token_id else -100) for token in label]
        for label in label_ids
    ]

    model_inputs["labels"] = label_ids

    return model_inputs


dataset = dataset.map(preprocess, batched=True)

# -------------------------------
# TRAINING CONFIG (IMPROVED)
# -------------------------------
training_args = TrainingArguments(
    output_dir="./my_paraphrase_model",

    per_device_train_batch_size=2,
    num_train_epochs=10,

    learning_rate=5e-5,

    logging_dir="./logs",
    logging_steps=10,

    save_strategy="epoch",

    # ✅ stability improvements
    save_total_limit=2,
    fp16=True if model.device.type == "cuda" else False
)

# -------------------------------
# TRAINER
# -------------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

# -------------------------------
# TRAIN
# -------------------------------
trainer.train()

# -------------------------------
# SAVE MODEL
# -------------------------------
model.save_pretrained("./my_paraphrase_model")
tokenizer.save_pretrained("./my_paraphrase_model")