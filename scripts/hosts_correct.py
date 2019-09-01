import paramiko
import socket
import sys
import os

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
        USER = os.getenv("USER")
        PORT = os.getenv("PORT")
        KEYFILENAME = os.getenv("KEYFILE")
        COMMAND = "hostname"
        k = paramiko.RSAKey.from_private_key_file(KEYFILENAME) 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=PORT, username=USER, pkey=k)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(COMMAND)
        entry = ssh_stdout.read().decode("utf-8").rstrip('\r').rstrip('\n')
        if entry == hostname:
            return ip + " " + entry 
    except paramiko.ssh_exception.NoValidConnectionsError:
        pass

if __name__ == "__main__":
    sed_etchosts()
    #print(get_ip("tokyo", "192.168.0", 255))
