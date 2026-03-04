import json
import requests
from shared_files.lamb_secrets import get_secrets
from shared_files.lamb_dynamo import get_ticket_id


SYSTEM_MARKER = "[SYNC-SYSTEM]"


def update_ticket(ticket_id, comment):

    secret = get_secrets()
    subdomain = secret["zendesk_subdomain"]

    url = f"https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json"

    headers = {
        "Authorization": f"Bearer {secret['zendesk_access_token']}",
        "Content-Type": "application/json"
    }

    payload = {
        "ticket": {
            "comment": {
                "body": f"{comment}\n\n{SYSTEM_MARKER}",
                "public": False
            }
        }
    }

    resp = requests.put(url, headers=headers, json=payload, timeout=10)
    resp.raise_for_status()


def lambda_handler(event, context):

    # asana handshake
    headers = event.get("headers") or {}
    headers = {k.lower(): v for k, v in headers.items()}

    hook_secret = headers.get("x-hook-secret")

    if hook_secret:
        return {
            "statusCode": 200,
            "headers": {
                "X-Hook-Secret": hook_secret
            },
            "body": ""
        }

    # normal event processing
    body = json.loads(event.get("body") or "{}")

    events = body.get("events", [])
    if not events:
        return {"statusCode": 200}

    for event_data in events:

        resource = event_data.get("resource", {})
        task_gid = resource.get("gid")
        task_name = resource.get("name", "Updated Task")

        if not task_gid:
            continue

        ticket_id = get_ticket_id(task_gid)

        if not ticket_id:
            continue

        comment = f"Asana Task Updated:\n{task_name}"

        update_ticket(ticket_id, comment)

    return {"statusCode": 200}