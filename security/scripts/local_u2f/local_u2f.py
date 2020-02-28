import inspect
import binascii
import os
import sys
import json
from pyu2f import model
from pyu2f.u2f import GetLocalU2FInterface

# Originally based on https://github.com/google/pyu2f/issues/9

APP_ID = u"SecTest"
CHALLENGE = b'01234567890123456789012345678901'

''' ############################### '''
def h(s):
    try:
        s = s.encode()
    except:
        pass
    return binascii.hexlify(s)

def verify(sig, pubkey, client_data, counter, this_APP_ID):
    from hashlib import sha256
    import struct
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import load_der_public_key
    from cryptography.hazmat.backends import default_backend
    PUB_KEY_DER_PREFIX = binascii.a2b_hex('3059301306072a8648ce3d020106082a8648ce3d030107034200')
    der_pubkey = PUB_KEY_DER_PREFIX+pubkey
    key = load_der_public_key(der_pubkey, default_backend())
    print(type(sig))
    #verifier = key.verifier(bytes(sig), ec.ECDSA(hashes.SHA256()))
    verifier = key.verify(bytes(sig), bytes('blah'.encode()),ec.ECDSA(hashes.SHA256()))
    app_param = sha256(this_APP_ID.encode('utf8')).digest()
    client_param = sha256(client_data.GetJson().encode('utf8')).digest()
    verifier.update(app_param+
                    struct.pack('>B', True) +
                    struct.pack('>I', counter) +
                    client_param,
                    )
    verifier.verify()

#convert a big number back into bytes:
def si(v):
    import struct
    s = b""
    while v>0:
        s = struct.pack("@B", v%256)+s
        v = v//256
    return s
    
def test():
    import struct
    import binascii
    from hashlib import sha256
    from pyu2f import model
    from pyu2f.u2f import GetLocalU2FInterface

    iface = GetLocalU2FInterface()
    this_APP_ID = u"Xpra"

    registered_keys = []
    challenge= b'01234567890123456789012345678901'
    rr = iface.Register(this_APP_ID, challenge, registered_keys)
    b = rr.registration_data
    assert b[0]==5
    pubkey = bytes(b[1:66])
    khl = b[66]
    key_handle = bytes(b[67:67 + khl])
    print("key_handle=%s" % h(key_handle))
    print("public key=%s" % h(pubkey))

    key = model.RegisteredKey(key_handle)
    challenge= b'01234567890123456789012345678901'
    response = iface.Authenticate(this_APP_ID, challenge, [key])
    sig = response.signature_data
    client_data = response.client_data
    print("signature_data=%s (%s len=%i)" % (h(sig), type(sig), len(sig)))
    print("client_data=%s (%s)" % (client_data, type(client_data),))

    touch = bool(sig[0])
    counter = struct.unpack('>I', sig[1:5])[0]
    print("touch=%s, counter=%i" % (touch, counter))
    assert sig[5] == 0x30

    #hacked asn1 parsing:
    l1 = sig[5+3]
    l2 = sig[5+4+l1+1]
    from pyasn1.codec.der.decoder import decode
    a1s = bytes(sig[5+2:5+2+2+l1])
    a1 = decode(a1s)
    a2s = bytes(sig[5+4+l1:])
    a2 = decode(a2s)
    n1 = si(a1[0])
    n2 = si(a2[0])
    verify(sig[5:], pubkey, client_data, counter, this_APP_ID)
    #for sig in (n1, n2, n1+n2):
    #    try:
    #        verify(sig)
    #    except Exception as e:
    #        print("signature %s failed: %s" % (h(sig), type(e)))
    #    else:
    #        print("SUCCESS!")
    #        break
''' ############################### '''


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
            print(interface)
        except:
            if not message_shown:
                print("Please connect your device")
                message_shown = True
    return interface


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
    print("key_handle")
    print(getHexlify(key_handle))
    return key_handle, getHexlify(public_key)


def authenticateKey(interface, key):
    print("Touch your U2F Key to authenticate...")
    response = interface.Authenticate(APP_ID, CHALLENGE, [key])
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'client_data', 'key_handle', 'signature_data']
    sig = response.signature_data
    client_data = response.client_data
    print(client_data)
    print(response.key_handle)
    print(sig)
    print("key_handle")
    print(getHexlify(response.key_handle))
    print("signature_data=%s (%s len=%i)" % (getHexlify(sig), type(sig), len(sig)))
    print("client_data=%s (%s)" % (client_data, type(client_data),))

    
''' ############################### '''

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
    elif sys.argv[1] == 'dev':
        test()
    else:
        print("Wrong syntax")
        sys.exit(2)

