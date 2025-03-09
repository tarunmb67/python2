# Step 1: Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from flask import Flask, request, jsonify
import joblib  # To save the scaler and encoder

# Step 2: Load and Preprocess Data
# Replace 'salesforce_opportunity_data.csv' with your actual file
data = pd.read_csv('salesforce_opportunity_data.csv')

# Separate features (X) and target (y)
X = data.drop('Target', axis=1)  # Features
y = data['Target']  # Target variable (1 = Won, 0 = Lost)

# Define categorical and numerical columns
categorical_cols = ['StageName', 'LeadSource', 'Industry']  # Example categorical columns
numerical_cols = ['Amount']  # Example numerical column

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ])

# Apply preprocessing
X_processed = preprocessor.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Step 3: Build the TensorFlow Model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),  # Input layer
    Dropout(0.2),  # Dropout to prevent overfitting
    Dense(32, activation='relu'),  # Hidden layer
    Dropout(0.2),
    Dense(1, activation='sigmoid')  # Output layer (binary classification)
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy:.2f}")

# Step 4: Save the Model and Preprocessor
model.save('opportunity_scoring_model.h5')
joblib.dump(preprocessor, 'preprocessor.pkl')  # Save the preprocessor for later use

# Step 5: Create a Flask API to Serve Predictions
app = Flask(__name__)

# Load the model and preprocessor
model = tf.keras.models.load_model('opportunity_scoring_model.h5')
preprocessor = joblib.load('preprocessor.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the request
    data = request.json['data']
    
    # Convert data to DataFrame
    input_data = pd.DataFrame([data])
    
    # Preprocess the input data
    processed_data = preprocessor.transform(input_data)
    
    # Make a prediction
    prediction = model.predict(processed_data)
    
    # Return the prediction as JSON
    return jsonify({'prediction': prediction.tolist()[0][0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)