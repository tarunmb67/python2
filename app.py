from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import joblib

# Load Model & Scaler
model = tf.keras.models.load_model('deal_risk_model.h5')
scaler = joblib.load('scaler.pkl')

# Start Flask App
app = Flask(__name__)

@app.route('/predict', methods=['POST','GET'])
def predict():
    try:
        data = request.get_json()
        
        # Convert input data to array
        features = np.array([[
            data['customer_engagement'], data['competitor_presence'], data['Amount'], 
            data['StageName'], data['DaysToClose'], data['LeadSource'], 
            data['Probability'], data['CompetitorPresence'], data['EngagementScore']
        ]])

        # Normalize input
        features_scaled = scaler.transform(features)

        # Predict risk score
        prediction = model.predict(features_scaled)[0][0]

        # Convert to readable format
        risk_level = "High" if prediction < 0.5 else "Low"

        return jsonify({'risk_score': risk_level, 'confidence': float(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
