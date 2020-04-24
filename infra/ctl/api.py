from flask import Flask, jsonify, request
from os import getenv


api_port = getenv("API_PORT")
api_host = getenv("API_HOST")

app = Flask(__name__)
app.config["debug"] = True

hosts = []

@app.route('/', methods=['GET'])
def home():
    return "<h1>Available paths</h1> \
            <p>/host</p>"

@app.route('/host', methods=['GET', 'PUT', 'POST', 'DELETE'])
def do_host():
    if request.method=='GET':
        return jsonify({'hosts': hosts})
    elif request.method=='PUT':
        host = {
            'name': request.json['name'],
            'mac_address': request.json['mac_address']
        }
        for entry in hosts:
            if entry['name'] == host['name']:
                entry['mac_address'] = host['mac_address']
        return jsonify({'host': hosts}), 201
    elif request.method=='POST':
        host = {
            'name': request.json['name'],
            'mac_address': request.json['mac_address']
        }
        hosts.append(host)
        return jsonify({'host': hosts}), 201
    elif request.method=='DELETE':
        host = {
            'name': request.json['name'],
        }
        for entry in hosts:
            if entry['name'] == host['name']:
                hosts.remove(entry)
        return jsonify({'host': hosts}), 201

if api_host is None:
    api_host = "0.0.0.0"
app.run(host=api_host, port=api_port)
