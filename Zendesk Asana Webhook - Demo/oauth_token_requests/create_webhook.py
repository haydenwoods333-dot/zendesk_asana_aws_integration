import requests

url = "https://app.asana.com/api/1.0/webhooks"

headers = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}

payload = {
    "data": {
        "resource": "",
        "target": ""
    }
}


resp = requests.post(url, headers=headers, json=payload)
print(resp.json())