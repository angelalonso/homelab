import binascii
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
    interface = GetLocalU2FInterface()
    registered_keys = []
    key_handle, public_key = registerKey(registered_keys, interface)
    print(key_handle)
    print(public_key)

    key = model.RegisteredKey(key_handle)
    authenticateKey(interface, key)
