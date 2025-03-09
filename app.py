from flask import Flask, request, jsonify
import tensorflow as tf
import joblib
import pandas as pd
import numpy as np

# Load Trained Model & Scaler
model = tf.keras.models.load_model('deal_risk_model.h5')
scaler = joblib.load('scaler.pkl')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from Salesforce
        data = request.get_json()

        # Convert JSON to Pandas DataFrame
        input_data = pd.DataFrame([data])

        # Ensure All Categorical Columns Exist
        category_columns = ['Stage_Closed', 'Stage_Negotiation', 'Stage_Proposal', 'Stage_Prospecting', 'Stage_Won',
                            'LeadSource_Event', 'LeadSource_Phone', 'LeadSource_Referral', 'LeadSource_Web',
                            'Industry_Finance', 'Industry_Health', 'Industry_Retail', 'Industry_Tech']

        for col in category_columns:
            if col not in input_data:
                input_data[col] = 0  # Add missing columns as 0

        # Scale Input Data
        input_scaled = scaler.transform(input_data)

        # Predict Risk Score
        risk_score = model.predict(input_scaled)[0][0]

        return jsonify({"risk_score": float(risk_score)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
