import requests
import pandas as pd

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

# Salesforce credentials
SF_INSTANCE_URL = "https://jll-2a-dev-ed.develop.my.salesforce.com"
ACCESS_TOKEN = access_token

# Salesforce API Query URL
query = "SELECT Id, Subject, ActivityDate, TaskSubtype, Status FROM Task"
url = f"{SF_INSTANCE_URL}/services/data/v57.0/query?q={query}"

# Headers with Bearer Token for Authentication
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Send GET request
response = requests.get(url, headers=headers)

# Process Response
if response.status_code == 200:
    data = response.json()

    df = pd.DataFrame(data["records"])
    if "attributes" in df.columns:
        df.drop(columns=["attributes"], inplace=True)    
        print("✅ "+df)  # Display the cleaned data
    else:
        print("❌ Error fetching data:", response.text)

    df_interactions = pd.DataFrame(data['records']).drop(columns=['attributes'])
    
    # Convert categorical values to numerical if needed
    df_interactions['TaskSubtype'] = df_interactions['TaskSubtype'].astype('category').cat.codes
    df_interactions['Status'] = df_interactions['Status'].astype('category').cat.codes
    df_interactions.fillna(0, inplace=True)

    print("✅ Customer interaction data retrieved successfully!")
else:
    print("❌ Error fetching Salesforce data:", response.text)
