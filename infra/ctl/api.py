from flask import Flask, jsonify, request
from dotenv import load_dotenv
from os import getenv



load_dotenv()
API_HOST = getenv("API_HOST")
API_PORT = getenv("API_PORT")

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

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
def db_connect():
    pass

def db_create():
    pass

def db_select():
    pass


def db_insert():
    pass

def db_update():
    pass

def db_delete():
    pass


if API_HOST is None:
    API_HOST = "0.0.0.0"
app.run(host=API_HOST, port=API_PORT)
