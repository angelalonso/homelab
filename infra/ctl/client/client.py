import argparse
import json
import yaml
import os
import requests
import sys
from ansible.module_utils._text import to_text

''' CTL CLASS '''

class Ctl(object):
    '''
    The argument tree object that triggers the related function(s)
    '''
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='client to the ctl cluster api',
            usage='''ctl <verb> [<args>]''')
        parser.add_argument('verb', help='[get|add|update|delete] <args>')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.verb):
            print('Unrecognized verb')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.verb)()

    ''' class argument functions '''

    def get(self):
        self.use_verb('get', 'Get a list of objects')

    def add(self):
        self.use_verb('add', 'Add an object')

    def update(self):
        self.use_verb('update', 'Update an object')

    def delete(self):
        self.userverb('delete', 'Delete an object')

    ''' class action forwarding functions '''

    def use_verb(self, verb, verb_description):
        parser = argparse.ArgumentParser(
            description=verb_description)
        parser.add_argument('object_type')
        parser.add_argument('object_data')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (ctl) and the subcommand (get)
        args = parser.parse_args(sys.argv[2:])
        if self.is_ok_object_type(args.object_type):
            self.manage_do(verb, args.object_type, args.object_data)
        else:
            print('Unrecognized object type ' + args.object_type)
            parser.print_help()

    def is_ok_object_type(self, object_type):
        accepted_types = ['host']
        return object_type in accepted_types

    def manage_do(self, verb, object_type, object_data):
        if verb == 'get':
            pass
        elif verb == 'add':
            self.do_add(object_type, self.get_data_mode(object_data), object_data)
        elif verb == 'update':
            pass
        elif verb == 'delete':
            pass

    def get_data_mode(self, data):
        if os.path.isdir(data):  
            return 'dir'
        elif os.path.isfile(data):  
            return 'file'
        else:
            return 'string'

    ''' class action forwarding functions '''

    def do_add(self, object_type, data_mode, data):
        data_objects = {}
        data_objects[object_type] = {}
        if data_mode == 'dir':
            for entry in os.scandir(data):
                if os.path.isfile(entry) and entry.name != 'template':
                    yaml_file = open(entry)
                    parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
                    data_objects[object_type][entry.name] = parsed_yaml_file
        elif data_mode == 'file':
            yaml_file = open(data)
            parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
            data_objects[object_type][os.path.basename(data)] = parsed_yaml_file
        elif data_mode == 'string':
            data_objects[object_type] = yaml.safe_load(data)
        self.send(data_objects)

    def get_sendable_json(self, data):
        json_data = {}
        for key, value in data.items():
            for object_name in value:
                json_data['name'] = object_name
                for attribute in value[object_name]:
                    json_data[attribute] = value[object_name][attribute]
        return json_data

    def send(self, data):
        json_data = self.get_sendable_json(data)
        # TODO: investigate why it doesnt work for folders
        response = requests.post("http://127.0.0.1:5000/host", verify=False, json=json_data)
        jprint(response.json())


''' AUX FUNCTIONS '''


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


''' API DIRECT FUNCTIONS '''


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

def delete():
    object_data = {
        'name': u'sidney',     
        'mac_address': u'00:00:00:00:00:00'
        }
    response = requests.delete("http://127.0.0.1:5000/host", verify=False, json=object_data)
    jprint(response.json())


''' IO FUNCTIONS '''


def import_ansible_hosts(host_vars_folder):
    ''' Imports all files within a given folder, typically the host_vars one
          that ansible would use. This means:
          - each file has the name of the host
          - each file MUST HAVE the related mac_address as a variable defined there

    '''
    pass

def import_ansible():
    with open('production', 'rb') as my_file:
        b_data = my_file.read()
        try:
            data = to_text(b_data, errors='surrogate_or_strict')
        except UnicodeError:
            # Handle the exception gracefully -- usually by displaying a good
            # user-centric error message that can be traced back to this piece
            # of code.
            pass
    print(data)


''' MAIN FUNCTIONS '''


if __name__ == "__main__":
    Ctl()
