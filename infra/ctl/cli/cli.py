import json
import os
import re
import requests
import sys
import yaml
from dotenv import load_dotenv


def loadObjectStruct(objects_file):
    try:
        with open(objects_file) as file:
            objects = yaml.safe_load(file)
    except FileNotFoundError:
        return None
    return objects


def loadVerbStruct(verbs_file):
    try:
        with open(verbs_file) as file:
            verbs = yaml.safe_load(file)
    except FileNotFoundError:
        return None
    return verbs


def loadArgs(verbs_struct, objects_struct, args):
    verbs = []
    for key in verbs_struct:
        verbs.append(key)
    objects = []
    for key in objects_struct:
        objects.append(key)
    try:
        # First arg should be the Verb
        if args[1] in verbs:
            verb = args[1]
            try:
                # Second arg should be the Object
                if args[2] in objects:
                    obj = args[2]
                    params = ' '.join(args[3:])
                    return verb, obj, params
                else:
                    showError("OBJECT " +
                              args[2] +
                              " could not be understood.",
                              verbs,
                              objects)
            except IndexError:
                showError("OBJECT is missing.", verbs, objects)
        else:
            showError("VERB " +
                      args[1] +
                      " could not be understood.",
                      verbs,
                      objects)
    except IndexError:
        showError("VERB is missing.", verbs, objects)


def createObject(verb_struct, obj_struct, obj, params):
    '''
    Check what type of params were received,
    build an object of type 'object',
    fail if anything goes wrong
    '''
    result_object = {}
    if os.path.isfile(params):
        # params type = 'object_full'
        with open(params) as file:
            result_object = yaml.safe_load(file)
    elif re.search('.*=.*', params):
        # params type = 'key_value'
        # TODO: be able to use : too (?)
        search_split = re.split('=', params)
        if search_split[0] not in obj_struct[obj]:
            showError('Parameter ' +
                      search_split[0] +
                      " nor found!",
                      verb_struct,
                      obj_struct)
        for key in obj_struct[obj]:
            if key == search_split[0]:
                result_object[key] = search_split[1]
            else:
                result_object[key] = None
    else:
        # params type = 'search_string'
        for key in obj_struct[obj]:
            # TODO: identify main key
            if key == 'name':
                result_object[key] = params
            else:
                result_object[key] = None
    return result_object


def runApiCall(call_type, data_struct):
    '''
    Depending on the type of call,
    build the data to send from object named "data",
     then do the call
    '''
    print("running " + call_type)
    if call_type == 'get' or call_type == 'delete':
        # build data
        data = ''
        for key in data_struct:
            if data != '':
                data = data + '&'
            data = data + key + "=" + str(data_struct[key])
        if call_type == 'get':
            # requests.post(url, data=[('interests',
            # 'football'), ('interests', 'basketball')])
            response = requests.get("http://" +
                                    API_HOST +
                                    ":" +
                                    API_PORT +
                                    "/host",
                                    params=data)
        elif call_type == 'delete':
            response = requests.delete("http://" +
                                       API_HOST +
                                       ":" +
                                       API_PORT +
                                       "/host",
                                       params=data)
    elif call_type == 'post':
        # build data
        data = json.dumps(data_struct)
        response = requests.post("http://" +
                                 API_HOST +
                                 ":" +
                                 API_PORT +
                                 "/host",
                                 json=data)
    jprint(response.json())


def do(verb_struct, obj_struct, verb, obj, params):
    '''
    Build an object with the data received as parameters,
     then run the API call with that
    '''
    # Check arg_1, _2...
    object_to_send = createObject(verb_struct, obj_struct, obj, params)
    # get command
    runApiCall(verb_struct[verb]['call'], object_to_send)


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def showError(message, verbs, objects):
    print("ERROR!")
    print(message + "\n")
    showHelp(verbs, objects)
    sys.exit(2)


def showHelp(verbs, objects):
    print("Usage: " + sys.argv[0] + " [VERB] [OBJECT] [parameters]")
    print("  Available VERB(s):")
    for verb in verbs:
        print("  - " + verb)
    print("  Available OBJECT(s):")
    for obj in objects:
        print("  - " + obj)


if __name__ == '__main__':
    load_dotenv()
    API_HOST = os.getenv("API_HOST")
    API_PORT = os.getenv("API_PORT")
    OBJECTS_STRUCT_FILE = os.getenv("OBJECTS_STRUCT_FILE")
    VERBS_STRUCT_FILE = os.getenv("VERBS_STRUCT_FILE")
    obj_struct = loadObjectStruct(OBJECTS_STRUCT_FILE)
    verb_struct = loadVerbStruct(VERBS_STRUCT_FILE)

    verb, obj, params = loadArgs(verb_struct, obj_struct, sys.argv[:])

    do(verb_struct, obj_struct, verb, obj, params)
