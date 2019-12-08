"""Docker Swarm Controller

Use case:
    This program is meant to help manage docker swarm, wrapping some commands up
"""
from dotenv import load_dotenv
import time
import os
import paramctl
import paramiko
import sh
import sys


def run_on_ssh(command, host):
    HOST = host
    USER = os.getenv("SSHUSER")
    PORT = os.getenv("SSHPORT")
    KEYFILENAME = os.getenv("SSHKEYFILENAME")
    k = paramiko.RSAKey.from_private_key_file(KEYFILENAME) 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=HOST, port=PORT, username=USER, pkey=k)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    return ssh_stdout.read()

def run_on_master_ssh(command):
    MASTERHOST = os.getenv("SSHMASTERHOST")
    return run_on_ssh(command, MASTERHOST)

def hi_node(*argv):
    host = argv[0][0]
    print(host + " is now blinking back at you")
    print(run_on_ssh('bash /home/aafmin/homelab/scripts/led_alert.sh', host))

def hi_all_nodes(*argv):
    hosts = get_nodes()
    for host in hosts:
        host_tuple = (host,) # better to have this as a tuple for the hi_node function
        hi_node(host_tuple)

def get_nodes(*argv):
    result = run_on_master_ssh('docker node ls --format "{{.Hostname}}"')

    result_list = result.decode("utf-8").split("\n")
    while("" in result_list) : 
        result_list.remove("") 
    return result_list


if __name__ == '__main__':
    """
    Calls the ctl_params library to retrieve the function name
      and parameters, according to the parametermap loaded,
      then calls the corresponding function
    """
    load_dotenv()
    #params = ctl_params.ParameterMap("parametermap.json")
    params = paramctl.ParameterMap("parametermap.json")

    # This builds  and runs the call to a function dinamically
    function = params.check_args_input(sys.argv)
    try:
        print(globals()[function[0]](function[1:]))
    except KeyError:
        print("No function available like " + " ".join(function[:]))
