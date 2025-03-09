from serpapi import GoogleSearch
from textblob import TextBlob
import requests
from Salesforce_Autehntication import SalesforceAuth

def fetch_news_sentiment():
    params = {
        "engine": "google_news",
        "q": "CRM industry trends",
        "hl": "en",
        "gl": "us",
        "api_key": "8b1594b5e915ababd16e9c6dd470e14be66cce47436b674a5caec6fda6a14203"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    sentiment_scores = []

    if "news_results" in results:
        for news in results["news_results"]:
            title = news["title"]
            sentiment = TextBlob(title).sentiment.polarity  # Sentiment score (-1 to 1)
            sentiment_scores.append(sentiment)
            #print(f"📰 {title} | Sentiment Score: {sentiment:.2f}")
    else:
        print("❌ No news found. Check API key.")

    # Return average sentiment score
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

sf_auth = SalesforceAuth()
# Process response
if sf_auth.authenticate():
    access_token = sf_auth.get_access_token()
    instance_url = sf_auth.get_instance_url()
else:
    print("❌ Error:", sf_auth.get_error())

SF_INSTANCE_URL = instance_url
ACCESS_TOKEN = access_token

# 🟢 Fetch Customer Interaction Data (Tasks & Events)
def fetch_salesforce_interactions(account_id):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    query = f"SELECT Subject, Description FROM Task WHERE WhatId = '{account_id}'"
    response = requests.get(f"{SF_INSTANCE_URL}/services/data/v59.0/query?q={query}", headers=headers)
    
    sentiment_scores = []
    if response.status_code == 200:
        data = response.json()
        for record in data.get("records", []):
            description = record.get("Description", "")
            if description:
                sentiment = TextBlob(description).sentiment.polarity if description else 10
                sentiment_scores.append(sentiment)
            else:
                print("🌍 1Interaction Sentiment Score: {record:.2f}")
    else:      
        print("🌍 2Interaction Sentiment Score: {response.status_code:.2f}")
    
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 20

# Test the function
market_sentiment = fetch_news_sentiment()
print(f"\n🌍 Market Sentiment Score: {market_sentiment:.2f}")
#interaction_sentiment = fetch_salesforce_interactions('0012w00001L61KnAAJ')
#print(f"\n🌍 Interaction Sentiment Score: {interaction_sentiment:.2f}")
