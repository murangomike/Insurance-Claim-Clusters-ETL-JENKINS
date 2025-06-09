from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained pipeline
try:
    pipeline = joblib.load('kmeans_pipeline.joblib')
    print("Pipeline loaded successfully!")
except FileNotFoundError:
    print("Warning: kmeans_pipeline.joblib not found. Make sure to train and save the model first.")
    pipeline = None

# Cluster interpretation
CLUSTER_INFO = {
    0: {
        'risk_level': 'High Risk',
        'pricing': 'Premium Pricing',
        'description': 'High-risk drivers with newer, high-value vehicles but less experience and more accidents',
        'characteristics': [
            'Higher number of accidents',
            'High vehicle value',
            'Newer cars',
            'Less driving experience',
            'Younger age group',
            'Lower annual mileage'
        ]
    },
    1: {
        'risk_level': 'Low Risk',
        'pricing': 'Standard Pricing',
        'description': 'Low-risk drivers with more experience and fewer accidents',
        'characteristics': [
            'Lower number of accidents',
            'More driving experience',
            'Older age group',
            'Higher annual mileage',
            'Lower vehicle value',
            'Older cars'
        ]
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if pipeline is None:
            return jsonify({'error': 'Model not loaded. Please ensure kmeans_pipeline.joblib exists.'}), 500
        
        # Get data from request
        data = request.json
        
        # Create DataFrame with the same structure as training data
        input_data = pd.DataFrame([{
            'age': float(data.get('age', 0)),
            'gender': data.get('gender', ''),
            'driving_experience': float(data.get('driving_experience', 0)),
            'car_model': data.get('car_model', ''),
            'year_of_manufacture': float(data.get('year_of_manufacture', 0)),
            'car_usage': data.get('car_usage', ''),
            'annual_mileage': float(data.get('annual_mileage', 0)),
            'location': data.get('location', ''),
            'has_caused_accident': int(data.get('has_caused_accident', 0)),
            'num_of_accidents': int(data.get('num_of_accidents', 0)),
            'vehicle_value': float(data.get('vehicle_value', 0))
        }])
        
        # Make prediction
        cluster = pipeline.predict(input_data)[0]
        
        # Get cluster information
        cluster_info = CLUSTER_INFO.get(cluster, {})
        
        result = {
            'cluster': int(cluster),
            'risk_level': cluster_info.get('risk_level', 'Unknown'),
            'pricing': cluster_info.get('pricing', 'Unknown'),
            'description': cluster_info.get('description', ''),
            'characteristics': cluster_info.get('characteristics', []),
            'input_data': data
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/cluster_info')
def cluster_info():
    """Endpoint to get information about all clusters"""
    return jsonify(CLUSTER_INFO)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model_loaded': pipeline is not None})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)