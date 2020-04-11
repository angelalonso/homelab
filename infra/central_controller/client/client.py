import json
import requests

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

response = requests.get("http://127.0.0.1:5000/host")

jprint(response.json())
