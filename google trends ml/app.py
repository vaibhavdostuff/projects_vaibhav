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

        if 'trend' in tokens or 'predict' in tokens:
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
            'message': f"Trend prediction for {target_column} has been generated. The graph shows the actual data and predicted future values.",
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

        # Create a comparison visualization
        plt.figure(figsize=(12, 6))
        for col in columns_to_compare:
            plt.plot(self.data.index, self.data[col], label=col)

        plt.title('Data Comparison')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.legend()

# Save the plot
        plot_filename = f'data_comparison_{uuid.uuid4()}.png'
        plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], plot_filename))
        plt.close()

        return {
            'message': f"Comparison of {', '.join(columns_to_compare)} has been generated. The graph shows the trends of the selected columns over time.",
            'plot': plot_filename
        }

    def general_query(self, tokens):
        results = {}
        for col in self.data.columns:
            if any(token in col.lower() for token in tokens):
                if self.data[col].dtype in ['int64', 'float64']:
                    results[col] = {
                        'mean': self.data[col].mean(),
                        'median': self.data[col].median(),
                        'std': self.data[col].std()
                    }
                elif self.data[col].dtype == 'object':
                    results[col] = self.data[col].value_counts().to_dict()
        return results

analyzer = DataAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            analyzer.load_data(file_path)
            analyzer.preprocess_data()
            session['file_uploaded'] = True
            return jsonify({'message': 'File uploaded and processed successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/questions')
def questions():
    if not session.get('file_uploaded'):
        return redirect(url_for('index'))
    return render_template('questions.html')

@app.route('/query', methods=['POST'])
def query_data():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    try:
        result = analyzer.query_data(query)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/plot/<filename>')
def serve_plot(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

