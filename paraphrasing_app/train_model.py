from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Load CSV
dataset = load_dataset("csv", data_files="data.csv")

# ✅ FILTER ONLY GOOD DATA
dataset = dataset["train"].filter(lambda x: x["quality"] == "good")

def preprocess(example):
    inputs = ["paraphrase: " + x for x in example["input"]]
    targets = example["output"]

    model_inputs = tokenizer(inputs, max_length=128, truncation=True)
    labels = tokenizer(targets, max_length=128, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

dataset = dataset.map(preprocess, batched=True)

training_args = TrainingArguments(
    output_dir="./my_paraphrase_model",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    logging_dir="./logs"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()

model.save_pretrained("./my_paraphrase_model")
tokenizer.save_pretrained("./my_paraphrase_model")