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
    newline = ""
    with open("/etc/hosts", "r") as sources:
        lines = sources.readlines()
    for line in lines:
        for host in HOSTS:
            if host in line:
                newline = get_ip(host, "192.168.0", 255)
                break
            else:
                newline = line.rstrip('\n')
        print(newline)

def get_ip(hostname, base_ip, range_ips):
    for ip_end in range(1, range_ips):
        ip = base_ip + "." + str(ip_end)
        hostresult = get_hostname(hostname, ip)
        if hostresult != None:
            return hostresult

def get_hostname(hostname, ip):
    try:
        entry = socket.gethostbyaddr(ip)[0]
        if entry == hostname:
            return ip + " " + entry 
    except socket.herror:
        pass
    except socket.gaierror:
        pass

if __name__ == "__main__":
    sed_etchosts()
    #print(get_ip("tokyo", "192.168.0", 255))
