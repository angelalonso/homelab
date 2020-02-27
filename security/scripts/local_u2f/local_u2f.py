import binascii
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

def registerKey(registered_keys):
    interface = GetLocalU2FInterface()
    register_result = interface.Register(APP_ID, CHALLENGE, registered_keys)
    raw_data = register_result.registration_data

    assert raw_data[0] == 5
    public_key = bytes(raw_data[1:66])
    key_handle_control = raw_data[66]
    key_handle = bytes(raw_data[67:67 + key_handle_control])
    return getHexlify(key_handle), getHexlify(public_key)


if __name__ == '__main__':
    registered_keys = []
    key_handle, public_key = registerKey(registered_keys)
    print(key_handle)
    print(public_key)
