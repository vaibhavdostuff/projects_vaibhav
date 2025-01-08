from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import uuid

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

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PLOT_FOLDER'] = 'plots/'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Max file size: 32MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PLOT_FOLDER'], exist_ok=True)

uploaded_data = None  # Store uploaded data globally


# File upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_data
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(file_path)

        # Load the data
        ext = os.path.splitext(file.filename)[1].lower()
        if ext == '.csv':
            uploaded_data = pd.read_csv(file_path)
        elif ext in ['.xls', '.xlsx']:
            uploaded_data = pd.read_excel(file_path)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

# Preprocess the data
        uploaded_data.fillna(uploaded_data.mean(), inplace=True)
        uploaded_data.columns = [str(col) for col in uploaded_data.columns]  # Ensure column names are strings
        session['file_uploaded'] = True
        return jsonify({'message': 'File uploaded and processed successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500


# Questions page
@app.route('/questions')
def questions():
    if not session.get('file_uploaded'):
        return redirect(url_for('index'))
    return render_template('questions.html', columns=uploaded_data.columns.tolist())

# Query endpoint
@app.route('/query', methods=['POST'])
def query_data():
    global uploaded_data
    if uploaded_data is None:
        return jsonify({'error': 'No data uploaded. Please upload a file first.'}), 400

    query = request.json.get('question', '').strip()
    column = request.json.get('column', '').strip()

    if not query:
        return jsonify({'error': 'Query is empty or invalid.'}), 400
    if not column:
        return jsonify({'error': 'Column not specified for the query.'}), 400
    if column not in uploaded_data.columns:
        return jsonify({'error': f'Column "{column}" not found in the uploaded data.'}), 400

    if 'predict' in query.lower():
        # Handle prediction
        if uploaded_data[column].dtype not in ['int64', 'float64']:
            return jsonify({'error': f'Column "{column}" is not numeric and cannot be used for prediction.'}), 400

        result = forecast_trend(uploaded_data[column], column)
        return jsonify(result), 200
    else:
        # Handle other queries
        return jsonify({'message': f'Your query "{query}" was received but could not be processed.'}), 200

