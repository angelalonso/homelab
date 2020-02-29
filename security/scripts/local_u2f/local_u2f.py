import yaml
import getopt
import sys
import json
from pyu2f import model
from pyu2f.u2f import GetLocalU2FInterface
from pyu2f.convenience import authenticator

# Originally based on https://github.com/google/pyu2f/issues/9

APP_ID = u"SecTest"
CHALLENGE = b'01234567890123456789012345678901'

def getConnectedDevice():
    interface = None
    message_shown = False
    while interface is None:
        try:
            interface = GetLocalU2FInterface()
            print(interface)
        except:
            if not message_shown:
                print("Please connect your device")
                message_shown = True
    return interface


''' ############################### '''
def registerKey(registered_keys, interface):
    print("Touch your U2F Key to register it...")
    register_result = interface.Register(APP_ID, CHALLENGE, registered_keys)
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'client_data', 'registration_data']
    data = register_result.client_data
    jsloads = json.loads(data.GetJson())
    chall = jsloads['challenge']
    print(jsloads)
    print(chall)
    raw_data = register_result.registration_data
    print("Key registered successfully!")

    assert raw_data[0] == 5
    public_key = bytes(raw_data[1:66])
    key_handle_control = raw_data[66]
    key_handle = bytes(raw_data[67:67 + key_handle_control])
    origin = jsloads['origin']
    return key_handle, public_key, origin


def saveKey(key, keys_file):
    with open(keys_file, 'w') as file:
        result = yaml.dump(key, file)
    

def loadKey(keys_file):
    with open(keys_file) as file:
        yaml_keys = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_keys


if __name__ == '__main__':
    keys_file = 'key.yaml'
    argumentList = sys.argv[1:]
    unixOptions = "rav:"
    gnuOptions = ["register", "authenticate", "verbose="]
    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        sys.exit(2)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-v", "--verbose"):
            print(("enabling verbose level (%s)") % (currentValue))
        elif currentArgument in ("-r", "register"):
            print("registering")
        elif currentArgument in ("-a", "auth"):
            print ("authorising")
    if sys.argv[1] == 'register':
        interface = getConnectedDevice()
        registered_keys = []
        key = {}
        key['handle'], pubkey_raw, key['origin'] = registerKey(registered_keys, interface)
        saveKey(key, keys_file)
    elif sys.argv[1] == 'authenticate':
        loaded_key = loadKey(keys_file)
        registered_key = model.RegisteredKey(loaded_key['handle'])
        challenge_data = [{'key': registered_key, 'challenge': CHALLENGE}]
        api = authenticator.CreateCompositeAuthenticator(loaded_key['origin'])
        response = api.Authenticate(APP_ID, challenge_data)
        print(response)
    elif sys.argv[1] == 'dev':
        pass
    else:
        print("Wrong syntax")
        sys.exit(2)

