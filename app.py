from flask import Flask, request, jsonify
import numpy as np
import joblib

# Load the trained model
model = joblib.load('deal_risk_model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    return "AI-Driven Deal Risk Prediction API is Running!"

@app.route('/predict', methods=['POST','GET'])
def predict():
    try:
        data = request.get_json()
        features = np.array([[data['deal_size'], data['customer_engagement'], data['competitor_presence']]])
        prediction = model.predict(features)[0]
        
        risk_level = "High" if prediction == 0 else "Low"
        return jsonify({'risk_score': risk_level})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
