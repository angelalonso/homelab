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

def sed_etchosts():
    with open("/etc/hosts", "r") as sources:
        lines = sources.readlines()
    for line in lines:
        for host in HOSTS:
            if host in line:
                newline = get_ip(host, "192.168.0", 255)
            else:
                newline = line
        print(newline)

def get_ip(hostname, base_ip, range_ips):
    for ip_end in range(1, range_ips):
        ip = base_ip + "." + str(ip_end)
        if ip != None:
            return get_hostname(ip)

def get_hostname(ip):
    try:
        entry = socket.gethostbyaddr(ip)[0]
        if entry in HOSTS:
            return entry + " " + ip
    except socket.herror:
        pass
    except socket.gaierror:
        print("Error " + ip)

if __name__ == "__main__":
    sed_etchosts()
