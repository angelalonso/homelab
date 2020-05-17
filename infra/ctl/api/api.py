import json
import mysql.connector as mysql
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from os import getenv


hosts = []

app = Flask(__name__)
app.config["debug"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Available paths</h1> \
            <p>/host</p>"

@app.route('/host', methods=['GET', 'PUT', 'POST', 'DELETE'])
def do_host():
    if request.method=='GET':
        if "name" in request.args:
            if STORAGE == 'local':
                result = DATA_MAIN['hosts']
            elif STORAGE == 'mysql':
                result = db_select(db_connect(), DB_NAME, 'hosts', 'name, mac_address', "name LIKE '" + request.args["name"] + "'")
        return jsonify(result)
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
        if STORAGE == 'local':
            json_data = json.loads(request.json)
            data_entry = {}
            data_entry['name'] = json_data['name']
            data_entry['mac_address'] = json_data['mac_address']
            DATA_MAIN['hosts'].append(data_entry)
            result = DATA_MAIN
        elif STORAGE == 'mysql':
            result = db_insert(db_connect(), DB_NAME, 'hosts', 'name, mac_address', "'" + request.json["name"] + "','" + request.json["mac_address"] + "'")
        return jsonify(result)
    elif request.method=='DELETE':
        if "name" in request.args:
            if STORAGE == 'local':
                for data_entry in DATA_MAIN['hosts']:
                    if data_entry['name'] == request.args['name']:
                        DATA_MAIN['hosts'].remove(data_entry)
                result = DATA_MAIN
            elif STORAGE == 'mysql':
                result = db_delete(db_connect(), DB_NAME, 'hosts', "name LIKE '" + request.args["name"] + "'")
        return jsonify(result)

''' Local Storage functions '''

''' MYSQL functions '''

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
def db_connect():
    db_conn = mysql.connect(
        host = DB_HOST,
        user = DB_USER,
        passwd = DB_PASS 
    )
    return db_conn

def db_show_dbs(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SHOW DATABASES")
    records = cursor.fetchall()
    return records

def db_create_db(db_conn, db_name):
    cursor = db_conn.cursor()
    cursor.execute("CREATE DATABASE " + db_name)

def db_create_table(db_conn, db_name, table_name, structure):
    cursor = db_conn.cursor()
    cursor.execute("CREATE TABLE " + db_name + "." + table_name + " " + structure)

def db_select(db_conn, db_name, table_name, fields, where_params):
    cursor = db_conn.cursor()
    sql_command = "SELECT " + fields + " FROM " + db_name + "." + table_name + " WHERE " + where_params + ";"
    cursor.execute(sql_command)
    records = cursor.fetchall()
    return records

def db_insert(db_conn, db_name, table_name, fields, values):
    cursor = db_conn.cursor()
    sql_command = "INSERT INTO " + db_name + "." + table_name + "(" + fields + ") VALUES(" + values + ")"
    cursor.execute(sql_command)
    db_conn.commit()
    result = cursor.rowcount
    return str(result)

def db_update():
    pass

def db_delete(db_conn, db_name, table_name, where_params):
    cursor = db_conn.cursor()
    sql_command = "DELETE FROM " + db_name + "." + table_name + " WHERE " + where_params + ";"
    cursor.execute(sql_command)
    db_conn.commit()
    result = cursor.rowcount
    return str(result)


if __name__ == '__main__':
    load_dotenv()
    API_HOST = getenv("API_HOST")
    API_PORT = getenv("API_PORT")
    if API_HOST is None:
        API_HOST = "0.0.0.0"
    STORAGE = getenv("STORAGE")
    if STORAGE == 'local':
        DATA_MAIN = {}
        DATA_MAIN['hosts'] = []
    elif STORAGE == 'mysql':
        DB_HOST = getenv("DB_HOST")
        DB_PORT = getenv("DB_PORT")
        DB_USER = getenv("DB_USER")
        DB_PASS = getenv("DB_PASS")
        DB_NAME = 'ctl'

    app.run(host=API_HOST, port=API_PORT)
