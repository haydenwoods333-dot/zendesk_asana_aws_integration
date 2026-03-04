import requests

SUBDOMAIN = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost"
AUTH_CODE = ""

url = f"https://{SUBDOMAIN}.zendesk.com/oauth/tokens"

data = {
    "grant_type": "authorization_code",
    "code": AUTH_CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "scope": "read write",
    "expires_in": 172800,
    "refresh_token_expires_in": 800000
}

response = requests.post(url, data=data)
print(response.status_code)
print(response.json())