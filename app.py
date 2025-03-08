from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import joblib

app = Flask(__name__)

# ✅ Load the TFLite model
tflite_model_path = "deal_risk_model.tflite"
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# ✅ Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ✅ Load the trained scaler
scaler = joblib.load("scaler.pkl")

@app.route("/")
def home():
    return "🚀 AI Model is Running!"

@app.route("/predict", methods=["POST","GET"])
def predict():
    try:
        # ✅ Get JSON input from request
        data = request.get_json()
        
        # ✅ Convert input into NumPy array
        features = np.array([data["features"]])  # Example: {"features": [20000, 2, 30, 1, 0.6, 0, 0.7]}

        # ✅ Scale input using the saved scaler
        features_scaled = scaler.transform(features)

        # ✅ Set input tensor
        interpreter.set_tensor(input_details[0]['index'], features_scaled.astype(np.float32))

        # ✅ Run inference
        interpreter.invoke()

        # ✅ Get the prediction result
        prediction = interpreter.get_tensor(output_details[0]['index'])

        risk_level = "High" if prediction < 0.5 else "Low"

        # ✅ Format the output
        response = ({'Predicted Deal Risk Score': float(prediction[0][0]), 'risk_score': risk_level})
        
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
