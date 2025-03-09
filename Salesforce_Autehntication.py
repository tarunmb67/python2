import requests

class SalesforceAuth:   

    # def __init__(self, login_url, client_id, client_secret, username, password, security_token):
    # self.login_url = login_url
    # self.client_id = client_id
    # self.client_secret = client_secret
    # self.username = username
    # self.password = password
    # self.security_token = security_token
    SF_LOGIN_URL = "https://jll-2a-dev-ed.develop.my.salesforce.com/services/oauth2/token"
    CLIENT_ID = "3MVG9n_HvETGhr3DpGec3Mcot0tfG_KZWFsQxcX45g2H3sG8kvEYWI76mawf7dT6Pqk6UwEgqDqn.8ThW6_aS"
    CLIENT_SECRET = "3AC678537C1B30716B1527BB0E0853A2751CCF10FE83A652837B4AC77B0CA81E"
    USERNAME = "tarun@jll.com"
    PASSWORD = "G@w97009703"
    SECURITY_TOKEN = "kq6DnRJ0xNiu7YfPgsGxM0CN"  # Get from Salesforce settings

    def __init__(self):
        self.access_token = None
        self.instance_url = None
        self.error = None

    def authenticate(self):

        # Authentication Payload
        payload = {
            "grant_type": "password",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "username": self.USERNAME,
            "password": self.PASSWORD + self.SECURITY_TOKEN
        }

        # Send POST request to get token
        response = requests.post(self.SF_LOGIN_URL, data=payload)

        # Process response
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
            self.instance_url = response.json()["instance_url"]
            print("✅ Access Token:", self.access_token)
            print("✅ Instance URL:", self.instance_url)
            return True
        else:
            self.error = response.json()
            print("✅ Instance Error:", self.error)
            return False

    def get_access_token(self):
        return self.access_token

    def get_instance_url(self):
        return self.instance_url

    def get_error(self):
        return self.error 
