import json
import requests
import os
from shared_files.lamb_asana import get_access_token, refresh_token
from shared_files.lamb_secrets import get_secrets
from shared_files.lamb_dynamo import get_ticket_id
from shared_files.lamb_zendesk import get_ticket

ASANA_PROJECT_GID = os.environ["ASANA_PROJECT_GID"]
ASANA_API_URL = "https://app.asana.com/api/1.0/tasks"

SYSTEM_MARKER = "[SYNC-SYSTEM]"


def lambda_handler(event, context):

    body = json.loads(event.get("body") or "{}")

    if not body:
        return {"statusCode": 400, "body": "Invalid payload"}

    ticket_id = body.get("id")

    if not ticket_id:
        return {"statusCode": 400, "body": "Missing ticket id"}

    ticket, _ = get_secrets(), None

    # Get full ticket from Zendesk
    ticket, _ = get_ticket(ticket_id)

    description = ticket.get("description", "")
    subject = ticket.get("subject", "")
    priority = ticket.get("priority", "")

    # prevent infinite loop
    if SYSTEM_MARKER in description:
        return {"statusCode": 200}

    task_payload = {
        "data": {
            "name": f"Zendesk #{ticket_id}: {subject}",
            "notes": f"Priority: {priority}\n\n{description}",
            "projects": [ASANA_PROJECT_GID]
        }
    }

    token, _ = get_access_token()

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        ASANA_API_URL,
        headers=headers,
        json=task_payload,
        timeout=10
    )

    if response.status_code == 401:
        token = refresh_token(get_secrets())
        headers["Authorization"] = f"Bearer {token}"

        response = requests.post(
            ASANA_API_URL,
            headers=headers,
            json=task_payload,
            timeout=10
        )

    response.raise_for_status()

    return {"statusCode": 200}