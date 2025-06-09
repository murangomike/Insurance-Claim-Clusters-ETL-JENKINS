# Insurance Risk Predictor

A Flask web application that predicts customer risk levels for insurance pricing using a pre-trained K-Means clustering model.

## Features

- **Web Interface**: User-friendly form to input customer information
- **Real-time Predictions**: Instant risk assessment and pricing recommendations
- **Risk Classification**: 
  - **Cluster 0 (High Risk - Premium Pricing)**: High accidents, newer/expensive cars, less experience
  - **Cluster 1 (Low Risk - Standard Pricing)**: Low accidents, more experience, older drivers
- **REST API**: JSON endpoints for integration with other systems

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure Model File Exists

Make sure your trained model `kmeans_pipeline.joblib` is in the same directory as `app.py`.

### 3. Directory Structure

```
your-project/
├── app.py
├── requirements.txt
├── kmeans_pipeline.joblib
└── templates/
    └── index.html
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## API Endpoints

### POST /predict
Predict customer risk level and pricing recommendation.

**Request Body:**
```json
{
    "age": 30,
    "gender": "Male",
    "driving_experience": 10,
    "car_model": "Toyota",
    "year_of_manufacture": 2020,
    "car_usage": "Personal",
    "annual_mileage": 15000,
    "location": "Urban",
    "has_caused_accident": 0,
    "num_of_accidents": 0,
    "vehicle_value": 25000
}
```

**Response:**
```json
{
    "cluster": 1,
    "risk_level": "Low Risk",
    "pricing": "Standard Pricing",
    "description": "Low-risk drivers with more experience and fewer accidents",
    "characteristics": [
        "Lower number of accidents",
        "More driving experience",
        "Older age group",
        "Higher annual mileage",
        "Lower vehicle value",
        "Older cars"
    ]
}
```

### GET /cluster_info
Get information about all clusters.

### GET /health
Check application health and model status.

## Usage

1. **Web Interface**: Navigate to `http://localhost:5000` and fill out the customer information form
2. **API**: Send POST requests to `/predict` endpoint with customer data
3. **Results**: Get instant risk assessment with pricing recommendations

## Cluster Interpretation

### Cluster 0 - High Risk (Premium Pricing)
- Higher number of accidents
- High vehicle value
- Newer cars
- Less driving experience  
- Younger age group
- Lower annual mileage

### Cluster 1 - Low Risk (Standard Pricing)
- Lower number of accidents
- More driving experience
- Older age group
- Higher annual mileage
- Lower vehicle value
- Older cars

## Model Features

The model uses the following features for prediction:
- **Categorical**: gender, car_model, car_usage, location
- **Numerical**: age, driving_experience, year_of_manufacture, annual_mileage, has_caused_accident, num_of_accidents, vehicle_value

## Technical Details

- **Framework**: Flask with CORS support
- **ML Pipeline**: scikit-learn Pipeline with ColumnTransformer
- **Preprocessing**: StandardScaler for numerical features, OneHotEncoder for categorical
- **Model**: K-Means clustering (k=2)
- **Frontend**: Responsive HTML/CSS/JavaScript interface