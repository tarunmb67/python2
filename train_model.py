import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import joblib
from flask import Flask, request, jsonify

# Sample Opportunity Data with Categorical Features
data = pd.DataFrame({
    'DealAmount': [10000, 50000, 20000, 80000, 15000, 40000, 25000, 60000, 90000, 30000],
    'Stage': ['Prospecting', 'Negotiation', 'Proposal', 'Closed', 'Prospecting', 'Negotiation', 'Proposal', 'Closed', 'Won', 'Negotiation'],
    'DaysToClose': [30, 60, 15, 90, 20, 45, 35, 70, 100, 55],
    'LeadSource': ['Referral', 'Web', 'Phone', 'Web', 'Referral', 'Event', 'Event', 'Web', 'Referral', 'Event'],
    'Industry': ['Tech', 'Finance', 'Tech', 'Retail', 'Tech', 'Health', 'Finance', 'Retail', 'Health', 'Tech'],
    'CompetitorPresence': [1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    'EngagementScore': [0.9, 0.3, 0.7, 0.2, 0.8, 0.5, 0.4, 0.6, 0.95, 0.55],
    'Won': [1, 0, 1, 0, 1, 1, 0, 0, 1, 0]  # Target variable (1 = Won, 0 = Lost)
})

# Add "MarketSentiment" to Training Data
data['MarketSentiment'] = np.random.uniform(-1, 1, size=len(data))  # Simulated values

# Generate Simulated Customer Interaction Sentiment (For Training)
data['InteractionSentiment'] = np.random.uniform(-1, 1, size=len(data))

# Encode Categorical Variables
categorical_features = ['Stage', 'LeadSource', 'Industry']
data_encoded = pd.get_dummies(data, columns=categorical_features)


# Split Features & Target
X = data_encoded.drop(columns=['Won'])
y = data_encoded['Won']

# Normalize Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define Deep Learning Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Binary classification
])

# Compile Model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train Model
model.fit(X_train, y_train, epochs=50, batch_size=4, validation_data=(X_test, y_test))

# Save Model & Scaler
model.save('deal_risk_model.h5')
joblib.dump(scaler, 'scaler.pkl')

print("✅ Model trained and saved successfully!")