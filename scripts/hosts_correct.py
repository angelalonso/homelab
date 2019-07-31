import sh
import socket
import sys


def get_host():
    for ip_end in range(1, 255):
        ip = "192.168.0." + str(ip_end)
        try:
            print(socket.gethostbyaddr(ip)[0] + " " + ip)
        except socket.herror:
            pass

if __name__ == "__main__":
    get_host()
