from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name,
    low_cpu_mem_usage=True
)

# Load CSV
dataset = load_dataset("csv", data_files="data.csv")

# ✅ Keep only good data
dataset = dataset["train"].filter(lambda x: x["quality"] == "good")

# -------------------------------
# PREPROCESS (IMPROVED)
# -------------------------------
def preprocess(example):

    inputs = []
    targets = []

    for inp, out in zip(example["input"], example["output"]):

        prompt = f"""
        Rewrite the following sentence clearly and correctly.
        Do not change the meaning.

        Sentence: {inp}
        """

        inputs.append(prompt)
        targets.append(out)

    model_inputs = tokenizer(
        inputs,
        max_length=128,
        truncation=True,
        padding="max_length"
    )

    labels = tokenizer(
        targets,
        max_length=128,
        truncation=True,
        padding="max_length"
    )

    model_inputs["labels"] = labels["input_ids"]

    return model_inputs

dataset = dataset.map(preprocess, batched=True)

# -------------------------------
# TRAINING CONFIG
# -------------------------------
training_args = TrainingArguments(
    output_dir="./my_paraphrase_model",
    per_device_train_batch_size=2,
    num_train_epochs=10,            # 🔥 increased
    learning_rate=5e-5,            # 🔥 important
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()

model.save_pretrained("./my_paraphrase_model")
tokenizer.save_pretrained("./my_paraphrase_model")