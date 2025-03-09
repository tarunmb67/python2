import requests
import pandas as pd
from Salesforce_Autehntication import SalesforceAuth

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
