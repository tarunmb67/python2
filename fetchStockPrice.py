import requests
url = "https://newsapi.org/v2/everything?q=industry&apiKey=YOUR_API_KEY"
response = requests.get(url).json()
print(response)