import struct
import binascii
from hashlib import sha256
from pyu2f import model
from pyu2f.u2f import GetLocalU2FInterface

iface = GetLocalU2FInterface()
APP_ID = u"Xpra"

def h(s):
    try:
        s = s.encode()
    except:
        pass
    return binascii.hexlify(s)

registered_keys = []
challenge= b'01234567890123456789012345678901'
rr = iface.Register(APP_ID, challenge, registered_keys)
b = rr.registration_data
assert b[0]==5
pubkey = bytes(b[1:66])
khl = b[66]
key_handle = bytes(b[67:67 + khl])
print("key_handle=%s" % h(key_handle))
print("public key=%s" % h(pubkey))

key = model.RegisteredKey(key_handle)
challenge= b'01234567890123456789012345678901'
response = iface.Authenticate(APP_ID, challenge, [key])
sig = response.signature_data
client_data = response.client_data
print("signature_data=%s (%s len=%i)" % (h(sig), type(sig), len(sig)))
print("client_data=%s (%s)" % (client_data, type(client_data),))

touch = bool(sig[0])
counter = struct.unpack('>I', sig[1:5])[0]
print("touch=%s, counter=%i" % (touch, counter))
assert sig[5] == 0x30

def verify(sig):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import load_der_public_key
    from cryptography.hazmat.backends import default_backend
    PUB_KEY_DER_PREFIX = binascii.a2b_hex('3059301306072a8648ce3d020106082a8648ce3d030107034200')
    der_pubkey = PUB_KEY_DER_PREFIX+pubkey
    key = load_der_public_key(der_pubkey, default_backend())
    verifier = key.verifier(sig, ec.ECDSA(hashes.SHA256()))
    app_param = sha256(APP_ID.encode('utf8')).digest()
    client_param = sha256(client_data.GetJson().encode('utf8')).digest()
    verifier.update(app_param+
                    struct.pack('>B', True) +
                    struct.pack('>I', counter) +
                    client_param,
                    )
    verifier.verify()

#hacked asn1 parsing:
l1 = sig[5+3]
l2 = sig[5+4+l1+1]
from pyasn1.codec.der.decoder import decode
a1s = bytes(sig[5+2:5+2+2+l1])
a1 = decode(a1s)
a2s = bytes(sig[5+4+l1:])
a2 = decode(a2s)
#convert a big number back into bytes:
def si(v):
    s = b""
    while v>0:
        s = struct.pack("@B", v%256)+s
        v = v//256
    return s
n1 = si(a1[0])
n2 = si(a2[0])
for sig in (n1, n2, n1+n2):
    try:
        verify(sig)
    except Exception as e:
        print("signature %s failed: %s" % (h(sig), type(e)))
    else:
        print("SUCCESS!")
        break
