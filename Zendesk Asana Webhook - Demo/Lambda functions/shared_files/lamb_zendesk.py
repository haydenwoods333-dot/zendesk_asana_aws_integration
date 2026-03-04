import requests
from lamb_secrets import get_secrets

def get_ticket(ticket_id):
    secret = get_secrets()

    subdomain = secret["zendesk_subdomain"]

    url = f"https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json"

    headers = {
        "Authorization": f"Bearer {secret['zendesk_access_token']}",
        "Content-Type": "application/json"
    }

    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()

    return resp.json()["ticket"], secret