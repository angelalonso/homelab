import sh
import socket
import sys

HOSTS = [
        "riga",
        "praha",
        "lisboa",
        "dublin",
        "sidney",
        "beirut",
        "tokyo"
        ]

def get_host():
    for ip_end in range(1, 255):
        ip = "192.168.0." + str(ip_end)
        try:
            entry = socket.gethostbyaddr(ip)[0]
            if entry in HOSTS:
                print(entry + " " + ip)
        except socket.herror:
            pass

if __name__ == "__main__":
    get_host()
