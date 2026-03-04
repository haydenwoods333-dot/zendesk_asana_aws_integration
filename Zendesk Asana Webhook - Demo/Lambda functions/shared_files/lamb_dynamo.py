import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO_TABLE"])


def store_mapping(task_gid, ticket_id):
    table.put_item(
        Item={
            "task_gid": str(task_gid),
            "ticket_id": str(ticket_id)
        }
    )


def get_ticket_id(task_gid):
    resp = table.get_item(
        Key={"task_gid": str(task_gid)}
    )

    item = resp.get("Item")
    if not item:
        return None

    return item["ticket_id"]