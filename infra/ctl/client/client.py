import argparse
import json
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

    ''' class action functions '''

    def use_verb(self, verb, verb_description):
        parser = argparse.ArgumentParser(
            description=verb_description)
        parser.add_argument('object')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (ctl) and the subcommand (get)
        args = parser.parse_args(sys.argv[2:])
        self.doStuff(verb, args.object)

    def doStuff(self, verb, object_data):
        pass

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
#    try:
#        if sys.argv[1] == 'get':
#            get()
#        elif sys.argv[1] == 'add':
#            add()
#        elif sys.argv[1] == 'edit':
#            edit()
#        elif sys.argv[1] == 'delete':
#            delete()
#        elif sys.argv[1] == 'import':
#            import_ansible()
#    except IndexError:
#        show_help()

