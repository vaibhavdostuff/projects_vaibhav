from flask import Flask, render_template, request

app = Flask(__name__)

# Simple synonym dictionary
synonyms = {
    "happy": ["joyful", "content", "pleased"],
    "play": ["participate", "engage", "perform"],
    "good": ["great", "excellent", "superb"],
    "game": ["match", "competition", "event"]
}