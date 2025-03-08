import tensorflow as tf
import pandas as pd
import numpy as np
import joblib

# Load trained model and scaler
model = tf.keras.models.load_model("deal_risk_model.h5")
scaler = joblib.load("scaler.pkl")

# Sample test deal (Modify values for testing)
test_input = np.array([[20000, 3, 50, 1, 0.6, 1, 0.8]])

# Scale input
test_input_df = pd.DataFrame(test_input, columns=['DealAmount', 'Stage', 'DaysToClose', 'Lead_Source', 'DealProbability', 'CompetitorPresence', 'EngagementScore'])
test_input_scaled = scaler.transform(test_input_df)

# Make prediction
prediction = model.predict(test_input_scaled)

# Convert result to risk level
risk_level = "High" if prediction < 0.5 else "Low"

print(f"Risk Level: {risk_level}, Confidence: {float(prediction[0][0])}")