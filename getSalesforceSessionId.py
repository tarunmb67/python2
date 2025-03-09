import requests

# Replace with your Salesforce credentials
SF_LOGIN_URL = "https://jll-2a-dev-ed.develop.my.salesforce.com/services/oauth2/token"
CLIENT_ID = "3MVG9n_HvETGhr3DpGec3Mcot0tfG_KZWFsQxcX45g2H3sG8kvEYWI76mawf7dT6Pqk6UwEgqDqn.8ThW6_aS"
CLIENT_SECRET = "3AC678537C1B30716B1527BB0E0853A2751CCF10FE83A652837B4AC77B0CA81E"
USERNAME = "tarun@jll.com"
PASSWORD = "G@w97009703"
SECURITY_TOKEN = "kq6DnRJ0xNiu7YfPgsGxM0CN"  # Get from Salesforce settings

# Authentication Payload
payload = {
    "grant_type": "password",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "username": USERNAME,
    "password": PASSWORD + SECURITY_TOKEN  # Append security token to password
}

# Send POST request to get token
response = requests.post(SF_LOGIN_URL, data=payload)

# Process response
if response.status_code == 200:
    access_token = response.json()["access_token"]
    instance_url = response.json()["instance_url"]
    print("✅ Access Token:", access_token)
    print("✅ Instance URL:", instance_url)
else:
    print("❌ Error:", response.json())
