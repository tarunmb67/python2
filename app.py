from flask import Flask, request, jsonify
import tensorflow as tf
import joblib
import pandas as pd
import numpy as np
import requests
from textblob import TextBlob
from serpapi import GoogleSearch
from Salesforce_Autehntication import SalesforceAuth
import nltk
nltk.download('punkt')

# Load Trained Model & Scaler
model = tf.keras.models.load_model('deal_risk_model.h5')
scaler = joblib.load('scaler.pkl')

app = Flask(__name__)

def fetch_news_sentiment():
    params = {
        "engine": "google_news",
        "q": "CRM industry trends",
        "hl": "en",
        "gl": "us",
        "api_key": "8b1594b5e915ababd16e9c6dd470e14be66cce47436b674a5caec6fda6a14203"  # Replace with your SerpAPI key
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    sentiment_scores = []
    
    if "news_results" in results:
        for news in results["news_results"]:
            title = news["title"]
            sentiment = TextBlob(title).sentiment.polarity
            sentiment_scores.append(sentiment)
    
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

# 🟢 Fetch Customer Interaction Data (Tasks & Events)
def fetch_salesforce_interactions(account_id, access_token, instance_url):
    headers = {"Authorization": f"Bearer {access_token}"}
    
    query = f"SELECT Subject, Description FROM Task WHERE WhatId = '{account_id}'"
    response = requests.get(f"{instance_url}/services/data/v59.0/query?q={query}", headers=headers)
    
    sentiment_scores = []
    if response.status_code == 200:
        data = response.json()
        for record in data.get("records", []):
            description = record.get("Description", "")
            sentiment = TextBlob(description).sentiment.polarity if description else 0
            sentiment_scores.append(sentiment)
    
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

sf_auth = SalesforceAuth()
# Process response
if sf_auth.authenticate():
    access_token = sf_auth.get_access_token()
    instance_url = sf_auth.get_instance_url()
else:
    print("❌ Error:", sf_auth.get_error())
# Salesforce credentials
SF_INSTANCE_URL = instance_url
ACCESS_TOKEN = access_token

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from Salesforce
        data = request.get_json()
        account_id = data.get("AccountId")
        deal_amount = float(data.get("DealAmount", 0))
        days_to_close = float(data.get("DaysToClose", 30))
        competitor_presence = int(data.get("CompetitorPresence", 0))
        engagement_score = float(data.get("EngagementScore", 0))

        # Convert JSON to Pandas DataFrame
        input_data = pd.DataFrame([data])

        # Fetch Customer Interaction Sentiment
        interaction_sentiment = fetch_salesforce_interactions(account_id, ACCESS_TOKEN, SF_INSTANCE_URL)
        
        # Fetch External Market Sentiment
        market_sentiment = fetch_news_sentiment()

        input_data = pd.DataFrame({
            'DealAmount': [deal_amount],
            'DaysToClose': [days_to_close],
            'CompetitorPresence': [competitor_presence],
            'EngagementScore': [engagement_score],
            'MarketSentiment': [market_sentiment],
            'InteractionSentiment': [interaction_sentiment],
            'Stage_Closed': [0], 'Stage_Negotiation': [1], 'Stage_Proposal': [0], 'Stage_Prospecting': [0], 'Stage_Won': [0],
            'LeadSource_Event': [0], 'LeadSource_Phone': [0], 'LeadSource_Referral': [1], 'LeadSource_Web': [0],
            'Industry_Finance': [1], 'Industry_Health': [0], 'Industry_Retail': [0], 'Industry_Tech': [0]
        })

        # Scale Data
        input_scaled = scaler.transform(input_data)

        # Predict Risk Score
        risk_score = model.predict(input_scaled)[0][0]

        return jsonify({"risk_score": float(risk_score)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
