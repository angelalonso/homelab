import binascii
import os
import sys
from pyu2f import model
from pyu2f.u2f import GetLocalU2FInterface

# Originally based on https://github.com/google/pyu2f/issues/9

APP_ID = u"SecTest"
CHALLENGE = b'01234567890123456789012345678901'

def getHexlify(string):
    try:
        string = string.encode()
    except:
        pass
    return binascii.hexlify(string)

def getUnhexlify(data):
    return binascii.unhexlify(data.replace("b'","").replace("'",""))


def saveRegisteredDevices(loaded_keys, keys_file):
    with open(keys_file, "w") as fh:
        for key in loaded_keys:
            fh.write(str(getHexlify(key)))
    #os.chmod(keys_file, 0600)

def loadRegisteredDevices(keys_file):
    with open(keys_file) as f:
        keys_list = f.readlines()
    return keys_list

def getConnectedDevice():
    interface = None
    message_shown = False
    while interface is None:
        try:
            interface = GetLocalU2FInterface()
        except:
            if not message_shown:
                print("Please connect your device")
                message_shown = True
    return interface


def registerKey(registered_keys, interface):
    print("Touch your U2F Key to register it...")
    register_result = interface.Register(APP_ID, CHALLENGE, registered_keys)
    raw_data = register_result.registration_data
    print("Key registered successfully!")

    assert raw_data[0] == 5
    public_key = bytes(raw_data[1:66])
    key_handle_control = raw_data[66]
    key_handle = bytes(raw_data[67:67 + key_handle_control])
    return key_handle, getHexlify(public_key)


def authenticateKey(interface, key):
    print("Touch your U2F Key to authenticate...")
    response = interface.Authenticate(APP_ID, CHALLENGE, [key])
    sig = response.signature_data
    client_data = response.client_data
    print("signature_data=%s (%s len=%i)" % (getHexlify(sig), type(sig), len(sig)))
    print("client_data=%s (%s)" % (client_data, type(client_data),))

if __name__ == '__main__':
    keys_file = 'keys.list'
    interface = getConnectedDevice()
    registered_keys = []
    loaded_keys = []
    if sys.argv[1] == 'register':
        key_handle, public_key = registerKey(registered_keys, interface)
        loaded_keys.append(key_handle)
        saveRegisteredDevices(loaded_keys, keys_file)
        print(key_handle)
        print(public_key)
    elif sys.argv[1] == 'authenticate':
        loaded_keys = loadRegisteredDevices(keys_file)
        print(loaded_keys)
        key = model.RegisteredKey(getUnhexlify(loaded_keys[0]))
        authenticateKey(interface, key)
    else:
        print("Wrong syntax")
        sys.exit(2)

