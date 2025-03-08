import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load Sample Data (Replace with actual Salesforce data)
data = pd.DataFrame({
    'deal_size': [10000, 50000, 20000, 80000, 15000, 35000, 60000, 45000],
    'customer_engagement': [0.8, 0.2, 0.6, 0.1, 0.7, 0.5, 0.3, 0.9],
    'competitor_presence': [1, 0, 0, 1, 0, 1, 0, 1],
    'won': [1, 0, 1, 0, 1, 0, 1, 1]  # Target variable: 1 = Won, 0 = Lost
})

# Prepare Features & Target
X = data[['deal_size', 'customer_engagement', 'competitor_presence']]
y = data['won']

# Save Feature Names for Later Use
joblib.dump(X.columns.tolist(), 'feature_names.pkl')

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost Model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred):.2f}')

# Save Model
joblib.dump(model, 'deal_risk_model.pkl')
print("✅ Model training complete. Files saved: `deal_risk_model.pkl`, `feature_names.pkl`")