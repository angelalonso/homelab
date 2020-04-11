from flask import Flask, jsonify, request
from os import getenv


api_port = getenv("api_port")
api_host = getenv("api_host")

app = Flask(__name__)
app.config["debug"] = True

hosts = [
    {
        'name': u'sidney',
        'mac_address': u'b8:27:eb:c3:e8:e4'
    },
    {
        'name': u'beirut',
        'mac_address': u'b8:27:eb:23:a3:d4'
    }
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Available paths</h1> \
            <p>/host</p>"

@app.route('/host', methods=['GET', 'PUT', 'POST'])
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


app.run(host=api_host, port=api_port)
