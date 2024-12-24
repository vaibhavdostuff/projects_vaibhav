from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
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
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

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