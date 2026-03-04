import requests
from urllib.parse import unquote

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost"

AUTH_CODE = unquote("")

TOKEN_URL = "https://app.asana.com/-/oauth_token"

data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": AUTH_CODE
}

response = requests.post(TOKEN_URL, data=data)
print("Status Code:", response.status_code)
print(response.json())