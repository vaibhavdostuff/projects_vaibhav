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
        
def predict_trend(self, tokens):
        # Identify the column to predict
        target_column = None
        for col in self.data.columns:
            if any(token in col.lower() for token in tokens):
                target_column = col
                break

        if target_column is None:
            return "Could not identify the trend to predict."

        # Prepare data for prediction
        X = self.data.index.values.reshape(-1, 1)
        y = self.data[target_column].values

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predict future values
        future_X = np.array(range(len(X), len(X) + 10)).reshape(-1, 1)
        future_y = model.predict(future_X)

        # Visualize the trend
        plt.figure(figsize=(12, 6))
        plt.scatter(X, y, color='blue', label='Actual data')
        plt.plot(future_X, future_y, color='red', label='Predicted trend')
        plt.title(f'Trend Prediction for {target_column}')
        plt.xlabel('Time')
        plt.ylabel(target_column)
        plt.legend()
        
        # Save the plot
        plot_filename = f'trend_prediction_{uuid.uuid4()}.png'
        plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], plot_filename))
        plt.close()

        return {
            'message': f"Trend prediction for {target_column} has been generated.",
            'plot': plot_filename
        }

        def compare_data(self, tokens):
            # Identify columns to compare
            columns_to_compare = []
            for col in self.data.columns:
                if any(token in col.lower() for token in tokens):
                    columns_to_compare.append(col)
                    
                    if len(columns_to_compare) < 2:
                        return "Could not identify at least two columns to compare."
                    
                    