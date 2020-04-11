from flask import Flask, jsonify
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

@app.route('/host', methods=['GET'])
def get_host():
    return jsonify({'hosts': hosts})

@app.route('/host', methods=['post'])
def create_host():
    if not request.json or not 'title' in request.json:
        abort(400)
    host = {
        'name': request.json['name'],
        'mac_address': request.json.get('mac_address', ""),
        'done': false
    }
    hosts.append(host)
    return jsonify({'host': hosts}), 201


app.run(host=api_host, port=api_port)
