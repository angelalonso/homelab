import json
import requests
import sys

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get():
    response = requests.get("http://127.0.0.1:5000/host")
    jprint(response.json())

def add():
    object_data = {
        'name': u'sidney',     
        'mac_address': u'00:00:00:00:00:00'
        }
    response = requests.post("http://127.0.0.1:5000/host", verify=False, json=object_data)
    jprint(response.json())

def edit():
    object_data = {
        'name': u'sidney',     
        'mac_address': u'00:00:00:00:00:00'
        }
    response = requests.put("http://127.0.0.1:5000/host", verify=False, json=object_data)
    jprint(response.json())

def show_help():
    print("SYNTAX:")
    print("  client.py <verb> <params>")
    print("  - verbs:")
    print("    get        - show current entries")

if __name__ == "__main__":
    try:
        if sys.argv[1] == 'get':
            get()
        elif sys.argv[1] == 'add':
            add()
        elif sys.argv[1] == 'edit':
            edit()
    except IndexError:
        show_help()

