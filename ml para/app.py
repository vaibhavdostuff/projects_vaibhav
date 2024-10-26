from flask import Flask, render_template, request
import random
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

# Load model and tokenizer
model_name = 't5-base'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

