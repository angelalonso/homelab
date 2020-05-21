import json
import mysql.connector as mysql
import yaml
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

@app.route('/<path:obj>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def all_routes(obj): # obj is defined by the path received and must be on the objects definition structure
    if request.method=='GET':
        if "name" in request.args:
            if STORAGE == 'local':
                result = []
                for entry in DATA_MAIN[obj]:
                    # TODO: avoid explicit use of "name" and so on
                    if request.args['name'] in entry['name']:
                        result.append(entry)
            elif STORAGE == 'mysql':
                # TODO: avoid explicit use of "name"
                try:
                    db_conn = connectDb_mysql()
                    result = select_mysql(db_conn, DB_NAME, obj, 'name, mac_address', "name LIKE '" + request.args["name"] + "'")
                except mysql.errors.ProgrammingError as e:
                    if mysql.errorcode.ER_NO_SUCH_TABLE == e.errno:
                        structure = buildSchemeFromObj_mysql(DB_NAME, obj)
                        try:
                            createTable_mysql(db_conn, DB_NAME, obj, structure)
                            result = select_mysql(db_conn, DB_NAME, obj, 'name, mac_address', "name LIKE '" + request.args["name"] + "'")
                        except mysql.errors.ProgrammingError as e:
                            result = str(e)
                            return jsonify(result), 503
                    else:
                        result = e
        return jsonify(result), 201
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
            # TODO: avoid explicit use of "name" and so on
            data_entry['name'] = json_data['name']
            data_entry['mac_address'] = json_data['mac_address']
            DATA_MAIN[obj].append(data_entry)
            result = DATA_MAIN
        elif STORAGE == 'mysql':
            # TODO: change this to host (NOT hosts) on the DB itself, avoid explicit use of "name"
            json_data = json.loads(request.json)
            result = insert_mysql(connectDb_mysql(), DB_NAME, obj, 'name, mac_address', "'" + json_data["name"] + "','" + json_data["mac_address"] + "'")
        return jsonify(result), 201
    elif request.method=='DELETE':
        if "name" in request.args:
            if STORAGE == 'local':
                for data_entry in DATA_MAIN[obj]:
                # TODO: avoid explicit use of "name" and so on
                    if data_entry['name'] == request.args['name']:
                        DATA_MAIN['host'].remove(data_entry)
                result = DATA_MAIN
            elif STORAGE == 'mysql':
                # TODO: change this to host (NOT hosts) on the DB itself, avoid explicit use of "name"
                result = delete_mysql(connectDb_mysql(), DB_NAME, obj, "name LIKE '" + request.args["name"] + "'")
        return jsonify(result), 201

''' Local Storage functions '''

def createDb_local(obj_struct):
    data_struct = {}
    for entry in obj_struct:
        data_struct[entry] = []
    return data_struct


''' MYSQL functions '''

def buildSchemeFromObj_mysql(database, table):
    scheme = '('
    for entry in obj_struct[table]:
        scheme += '`' + entry + '` '
        scheme += obj_struct[table][entry]['mysql_scheme'] + ', '
    scheme = scheme[:-2] + ' )'
    return scheme

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
def connectDb_mysql():
    db_conn = mysql.connect(
        host = DB_HOST,
        user = DB_USER,
        passwd = DB_PASS, 
        database = DB_NAME
    )
    return db_conn

def showDbs_mysql(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SHOW DATABASES")
    records = cursor.fetchall()
    return records

def createDb_mysql(db_conn, db_name):
    cursor = db_conn.cursor()
    cursor.execute("CREATE DATABASE " + db_name)

def createTable_mysql(db_conn, db_name, table_name, structure):
    cursor = db_conn.cursor()
    cursor.execute("CREATE TABLE " + table_name + " " + structure)

def select_mysql(db_conn, db_name, table_name, fields, where_params):
    cursor = db_conn.cursor()
    sql_command = "SELECT " + fields + " FROM " + db_name + "." + table_name + " WHERE " + where_params + ";"
    cursor.execute(sql_command)
    records = cursor.fetchall()
    return records

def insert_mysql(db_conn, db_name, table_name, fields, values):
    cursor = db_conn.cursor()
    sql_command = "INSERT INTO " + db_name + "." + table_name + "(" + fields + ") VALUES(" + values + ")"
    cursor.execute(sql_command)
    db_conn.commit()
    result = cursor.rowcount
    return str(result)

def update_mysql():
    pass

def delete_mysql(db_conn, db_name, table_name, where_params):
    cursor = db_conn.cursor()
    sql_command = "DELETE FROM " + db_name + "." + table_name + " WHERE " + where_params + ";"
    cursor.execute(sql_command)
    db_conn.commit()
    result = cursor.rowcount
    return str(result)

''' AUX Functions '''

def loadObjectStruct(objects_file):
    '''
    Loads a yaml file into a data structure
    '''
    try:
        with open(objects_file) as file:
            objects = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        return None
    return objects


if __name__ == '__main__':
    load_dotenv()

    OBJECTS_STRUCT_FILE = getenv("OBJECTS_STRUCT_FILE")
    obj_struct = loadObjectStruct(OBJECTS_STRUCT_FILE)

    API_HOST = getenv("API_HOST")
    API_PORT = getenv("API_PORT")
    if API_HOST is None:
        API_HOST = "0.0.0.0"

    STORAGE = getenv("STORAGE")
    if STORAGE == 'local':
        DATA_MAIN = createDb_local(obj_struct)
    elif STORAGE == 'mysql':
        DB_HOST = getenv("DB_HOST")
        DB_PORT = getenv("DB_PORT")
        DB_USER = getenv("DB_USER")
        DB_PASS = getenv("DB_PASS")
        DB_NAME = 'ctl'

    app.run(host=API_HOST, port=API_PORT)
