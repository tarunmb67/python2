import numpy as np
import joblib
import tensorflow as tf
import pandas as pd

# Load Model & Scaler
model = tf.keras.models.load_model('deal_risk_model.h5')
scaler = joblib.load('scaler.pkl')

# Sample Test Opportunity Data (Modify as Needed)
test_data = pd.DataFrame({
    'DealAmount': [70000],
    'DaysToClose': [40],
    'CompetitorPresence': [1],
    'EngagementScore': [0.75],
    'Stage_Closed': [0], 'Stage_Negotiation': [1], 'Stage_Proposal': [0], 'Stage_Prospecting': [0], 'Stage_Won': [0],
    'LeadSource_Event': [0], 'LeadSource_Phone': [0], 'LeadSource_Referral': [1], 'LeadSource_Web': [0],
    'Industry_Finance': [1], 'Industry_Health': [0], 'Industry_Retail': [0], 'Industry_Tech': [0]
})

# Scale Input Data
test_scaled = scaler.transform(test_data)

# Predict Risk Score
risk_score = model.predict(test_scaled)

print(f"🔍 Predicted Deal Risk Score: {risk_score[0][0]:.2f}")