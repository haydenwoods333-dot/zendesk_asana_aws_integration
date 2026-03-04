import requests
from lamb_secrets import get_secrets, update_secrets
ASANA_TOKEN_URL = "https://app.asana.com/-/oauth_token"
ASANA_API_URL = "https://app.asana.com/api/1.0/tasks"

def get_access_token():
    secret = get_secrets()
    return secret["asana_access_token"], secret

def refresh_token(secret):
    resp = requests.post(
        ASANA_TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "client_id": secret["asana_client_id"],
            "client_secret": secret["asana_client_secret"],
            "refresh_token": secret["asana_refresh_token"]
        },
        timeout=5
    )
    resp.raise_for_status()
    data = resp.json()

    secret["asana_access_token"] = data["access_token"]
    if "refresh_token" in data:
        secret["asana_refresh_token"] = data["refresh_token"]

    update_secrets(secret)
    return secret["asana_access_token"]

def update_task(task_gid, fields, token):
    url = f"{ASANA_API_URL}/{task_gid}"
    headers = {"Authorization": f"Bearer {token}"}

    return requests.put(
        url,
        headers=headers,
        json={"data": fields},
        timeout=10
    )