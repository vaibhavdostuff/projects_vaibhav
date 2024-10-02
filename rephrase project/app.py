import spacy
import random

# Load spacy model for English
nlp = spacy.load("en_core_web_sm")

def restructure_sentence(text):
    """Restructure the sentence to sound natural, allowing extra words and grammatical corrections."""
    doc = nlp(text)