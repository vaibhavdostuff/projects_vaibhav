from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback
)
import torch

# -------------------------------
# MODEL
# -------------------------------
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name,
    low_cpu_mem_usage=True
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# -------------------------------
# LOAD DATA
# -------------------------------
dataset = load_dataset("csv", data_files="data.csv")

# -------------------------------
# FILTER GOOD DATA ONLY
# -------------------------------
dataset = dataset["train"].filter(lambda x: x["Quality"] == "good")

# -------------------------------
# TRAIN / VALID SPLIT (IMPORTANT)
# -------------------------------
dataset = dataset.train_test_split(test_size=0.1)

train_dataset = dataset["train"]
val_dataset = dataset["test"]

# -------------------------------
# PREPROCESS (STYLE-AWARE 🔥)
# -------------------------------
def preprocess(example):

    inputs = []
    targets = []

    for inp, out, style in zip(
        example["Input"],
        example["Output"],
        example["Style"]
    ):

        # 🔥 STYLE-CONDITIONED PROMPT (VERY IMPORTANT)
        prompt = f"""
Paraphrase the sentence in a {style} tone.

Rules:
- Keep the same meaning
- Do not add new information
- Improve clarity and grammar
- Match the tone exactly

Sentence: {inp}
"""

        inputs.append(prompt)
        targets.append(out)

    model_inputs = tokenizer(
        inputs,
        max_length=128,
        truncation=True,
        padding=True
    )

    labels = tokenizer(
        targets,
        max_length=128,
        truncation=True,
        padding=True
    )

    # Replace padding token with -100
    label_ids = labels["input_ids"]
    label_ids = [
        [(token if token != tokenizer.pad_token_id else -100) for token in label]
        for label in label_ids
    ]

    model_inputs["labels"] = label_ids

    return model_inputs


train_dataset = train_dataset.map(preprocess, batched=True)
val_dataset = val_dataset.map(preprocess, batched=True)

# -------------------------------
# DATA COLLATOR (DYNAMIC PADDING ✅)
# -------------------------------
data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model
)

# -------------------------------
# TRAINING CONFIG (UPGRADED)
# -------------------------------
training_args = TrainingArguments(
    output_dir="./my_paraphrase_model",

    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,

    num_train_epochs=8,
    learning_rate=3e-5,

    evaluation_strategy="epoch",
    save_strategy="epoch",

    logging_dir="./logs",
    logging_steps=20,

    save_total_limit=2,

    load_best_model_at_end=True,
    metric_for_best_model="loss",

    fp16=True if torch.cuda.is_available() else False
)

# -------------------------------
# TRAINER
# -------------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
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

print("✅ Training Complete & Model Saved")