from pytrends.request import TrendReq
from serpapi import GoogleSearch
import yfinance as yf
import pandas as pd

crm_stock = yf.Ticker("CRM")
# Get historical market trends for last 6 months
market_data = crm_stock.history(period="6mo")

# Define keywords to track (example: CRM, AI, Cloud)
keywords = ["CRM"]
# Initialize PyTrends session
pytrends = TrendReq(hl="en-US", tz=360)
# Build payload for trends data
pytrends.build_payload(kw_list=keywords, cat=0, timeframe="today 3-m", geo="US")
# Get Interest Over Time
data = pytrends.interest_over_time()

if not data.empty:
    print("✅ Successfully fetched market trends data!")
    print(market_data.tail())
    print(data)
else:
    print("❌ No data received. Check the keyword or timeframe.")

params = {
    "engine": "google_news",
    "q": "CRM industry trends",
    "hl": "en",
    "gl": "us",
    "api_key": "8b1594b5e915ababd16e9c6dd470e14be66cce47436b674a5caec6fda6a14203"  # Replace with your SerpAPI key
}

search = GoogleSearch(params)
results = search.get_dict()

if "news_results" in results:
    for news in results["news_results"]:
        print(f"🔹 {news['title']} - {news['link']}")
else:
    print("❌ No news found. Check API key or query.")