import mysql.connector as mysql
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from os import getenv



load_dotenv()
API_HOST = getenv("API_HOST")
API_PORT = getenv("API_PORT")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")

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
        print(db_connect())
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
    db_conn = mysql.connect(
        host = DB_HOST,
        user = DB_USER,
        passwd = DB_PASS 
    )
    return db_conn

def db_create_db(db_conn, db_name):
    cursor = db_conn.cursor()
    cursor.execute("CREATE DATABASE " + db_name)

def db_create_table(db_conn, db_name, table_name, structure):
    cursor = db_conn.cursor()
    cursor.execute("CREATE TABLE " + db_name + "." + table_name + " " + structure)

def db_select(db_conn, db_name, table_name, fields, where_params):
    cursor = db_conn.cursor()
    cursor.execute("SELECT " + fields + " FROM " + db_name + "." + table_name + " WHERE " + where_params)
    records = cursor.fetchall()
    return records

def db_insert():
    pass

def db_update():
    pass

def db_delete():
    pass


if API_HOST is None:
    API_HOST = "0.0.0.0"
app.run(host=API_HOST, port=API_PORT)
