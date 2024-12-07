from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import json
import uuid

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DataAnalyzer:
    def __init__(self):
        self.data = None
        self.data_source = None

    def load_data(self, file_path):
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.csv':
            self.data = pd.read_csv(file_path)
        elif file_extension in ['.xls', '.xlsx']:
            self.data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        self.data_source = os.path.basename(file_path)

    def preprocess_data(self):
        # Handle missing values
        self.data = self.data.fillna(self.data.mean())
        
        # Convert date columns to datetime
        date_columns = self.data.select_dtypes(include=['object']).columns
        for col in date_columns:
            try:
                self.data[col] = pd.to_datetime(self.data[col])
            except:
                pass

    def query_data(self, query):
        tokens = word_tokenize(query.lower())
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]

        if 'trend' in tokens:
            return self.predict_trend(tokens)
        elif 'compare' in tokens:
            return self.compare_data(tokens)
        else:
            return self.general_query(tokens)
        
