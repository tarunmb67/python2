import numpy as np
import tensorflow as tf
import joblib

# ✅ Load the TFLite model
tflite_model_path = "deal_risk_model.tflite"
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# ✅ Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ✅ Load the saved StandardScaler
scaler = joblib.load("scaler.pkl")

# ✅ Define a sample new deal (raw features)
new_deal = np.array([[20000, 2, 30, 1, 0.6, 0, 0.7]])  # Adjust values as per your feature set

# ✅ Scale the input using the same scaler
new_deal_scaled = scaler.transform(new_deal)

# ✅ Set input tensor
interpreter.set_tensor(input_details[0]['index'], new_deal_scaled.astype(np.float32))

# ✅ Run inference
interpreter.invoke()

# ✅ Get the prediction result
prediction = interpreter.get_tensor(output_details[0]['index'])

# ✅ Display predicted risk score
print(f"🔮 Predicted Deal Risk Score: {prediction[0][0]:.4f}")