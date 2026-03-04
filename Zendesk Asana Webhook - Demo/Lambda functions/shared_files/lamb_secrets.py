import boto3
import json
import os
SECRET = os.environ["SECRET_NAME"]

client = boto3.client("secretsmanager")

def get_secrets():
    resp = client.get_secret_value(SecretId=SECRET)
    return json.loads(resp["SecretString"])

def update_secrets(data):
    client.update_secret(
        SecretId=SECRET,
        SecretString=json.dumps(data)
    )