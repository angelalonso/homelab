from __future__ import print_function
import socket
from pyu2f import hardware, hid, u2f


def getKey():
    devs = hid.Enumerate()
    for dev in devs:
        if dev['product_string'] == 'Yubico Security Key by Yubico':
            return dev

if __name__ == '__main__':
    interface = u2f.GetLocalU2FInterface(origin=socket.gethostname())
    interface.Register()
    print(interface)
