import spacy
import random

# Load spacy model for English
nlp = spacy.load("en_core_web_sm")

def restructure_sentence(text):
    """Restructure the sentence to sound natural, allowing extra words and grammatical corrections."""
    doc = nlp(text)

    subject = []
    verb = []
    object_ = []
    other = []

    # Extract sentence components
    for token in doc:
        if token.dep_ in ["nsubj", "nsubjpass"]:  # Subject
            subject.append(token.text)
        elif token.dep_ in ["ROOT", "aux", "auxpass", "cop"]:  # Main verbs or auxiliary verbs
            verb.append(token.text)
        elif token.dep_ in ["dobj", "attr", "prep", "pobj", "advmod"]:  # Object or object modifier
            object_.append(token.text)
        else:
            other.append(token.text)

   # Handle cases where components may be empty
    subject = ' '.join(subject) if subject else "We"  # Default subject if none found
    verb = ' '.join(verb) if verb else "are"  # Default verb
    object_ = ' '.join(object_) if object_ else "playing"  # Default object

    