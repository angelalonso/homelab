import copy
import crypt
import glob
import ipaddress
import os
import paramiko
import shutil
import socket
import subprocess
import sys
import time
import yaml

from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


def createSecrets(secrets_template, secrets_file):
    verbose("Creating a new secrets.yaml file", 1)
    if os.path.isfile(secrets_file):
        verbose("ATTENTION! " + secrets_file + " already exists!", 2)
        verbose(" Please BACK IT UP or REMOVE IT, then run again", 2)
    else:
        dest = shutil.copyfile(secrets_template, secrets_file)
        verbose("DONE! You can now edit " + secrets_file + " accordingly", 2)
        verbose(" AND REMEMBER: this file will contain private data!", 2)

def createConfigFiles(secrets, templates_folder, manifests_folder, secrets_full):
    '''
    Creates different config files for different groups from templates
    So far only use case I have is config_sshd
    '''
    cfg_ssh_file = 'config_sshd'
    cfg_etchosts_file = 'config_etchosts'
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    for group in secrets['groups']:
        if (secrets['groups'][group] is None) or (secrets['groups'][group]['hosts'] is None):
            print(group + " is empty. Nothing to be done there.")
        else:
            # Only generate from template when group needs it
            # key to find is <service>_changes: [True|False]
            try:
                if secrets['groups'][group]['sshd_changes']:
                    template_cfg_ssh = env.get_template(cfg_ssh_file)
                    with open(manifests_folder + '/' + cfg_ssh_file + '_' + group, "w") as fcssh:
                        fcssh.write(template_cfg_ssh.render(secrets_group=secrets['groups'][group]))
            except KeyError:
                pass
    template_cfg_etchosts = env.get_template(cfg_etchosts_file)
    with open(manifests_folder + '/' + cfg_etchosts_file, "w") as fchst:
        fchst.write(template_cfg_etchosts.render(secrets=secrets_full))

def createPlaybooks(secrets, templates_folder, manifests_folder):
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    # templated playbooks per group
    for group in secrets['groups']:
        if secrets['groups'][group] is None:
            print(group + " is empty. Nothing to be done there.")
        else:
            playbook_file = 'playbook_' + group + '.yaml'
            if os.path.isfile(templates_folder + '/' + playbook_file):
                template_playbook = env.get_template(playbook_file)
                with open(manifests_folder + '/' + playbook_file, "w") as fm:
                    fm.write(template_playbook.render(secrets_group=secrets['groups'][group], secrets=secrets, getSaltedPassword=getSaltedPassword))
            else:
                print(templates_folder + '/' + playbook_file + ' does not exist! Nothing to be done there.')

def createManifests(secrets, templates_folder, manifests_folder, secrets_full):
    cleanupFolder(manifests_folder)
    hosts_filename = 'hosts'
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    # hosts inventory
    template_hosts = env.get_template(hosts_filename)
    with open(manifests_folder + '/' + hosts_filename, "w") as fh:
        fh.write(template_hosts.render(secrets=secrets))
    # config files
    createConfigFiles(secrets, templates_folder, manifests_folder, secrets_full)
    # playbooks
    createPlaybooks(secrets, templates_folder, manifests_folder)

def init(secrets, templates_folder, manifests_folder):
    cleanupFolder('tmp')
    phase1_needed = isPhase1Needed(secrets)
    if phase1_needed[0]:
        verbose("Phase 1 needed",1)
        secrets_phase1, secrets_others = getPhaseSplittedSecrets(secrets, phase1_needed[1])
        saveTempSecrets(secrets_others, 'secrets.others.yaml')
        saveTempSecrets(secrets_phase1, 'secrets.phase1.yaml')
        createManifests(secrets_phase1, templates_folder, manifests_folder, secrets)
    else:
        createManifests(secrets, templates_folder, manifests_folder, secrets)

def plan(secrets, manifests_folder):
    verbose("Planning playbooks", 1)
    # TODO: os.environ['ANSIBLE_HOST_KEY_CHECKING'] = str(False)
    for group in secrets['groups']:
        playbook_file = manifests_folder + "/playbook_" + group + ".yaml"
        if os.path.isfile(playbook_file):
            result = subprocess.run(["ansible-playbook", "-i", manifests_folder + "/hosts", playbook_file, "--check"])
            if result.returncode > 0:
                verbose("The dry run had issues. Modify secrets.yaml or your templates accordingly", 1)
                return result.returncode
    return 0

def apply(secrets, manifests_folder):
    verbose("Applying playbooks", 1)
    for group in secrets['groups']:
        playbook_file = manifests_folder + "/playbook_" + group + ".yaml"
        if os.path.isfile(playbook_file):
            result = subprocess.run(["ansible-playbook", "-i", manifests_folder + "/hosts", playbook_file])
            if result.returncode > 0:
                verbose("There were issues found while applying. Modify secrets.yaml or your templates accordingly", 1)
                return result.returncode
    if isPhase1Needed(secrets)[0]:
        backupAndOverwrite('secrets.yaml', 'tmp/secrets.others.yaml', 'secrets.yaml.bkp.' + time.strftime("%Y%m%d-%H%M%S"))
        verbose("This was the phase 1 run", 2)
        verbose("To continue the other playbooks, run make init && make apply again", 1)
    return 0


## Auxiliary Functions
######################

def saveTempSecrets(secrets, filename):
    if not os.path.exists(TMP_FOLDER):
        os.makedirs(TMP_FOLDER)
    with open(TMP_FOLDER + "/" + filename, 'w') as file2write:
        document = yaml.dump(secrets, file2write)

def backupAndOverwrite(old_file, new_file, backup_file):
    dest = shutil.copyfile(old_file, backup_file)
    dest2 = shutil.copyfile(new_file, old_file)
    verbose("We modified your secrets.yaml. Your original secrets.yaml has been saved under " + backup_file, 2)

def isPhase1Needed(secrets):
    hosts = []
    try:
        hosts = secrets['groups']['phase1']['hosts']
        if len(hosts) < 1:
            return False, hosts
        else:
            return True, hosts
    except KeyError:
        return False, hosts

def getPhaseSplittedSecrets(secrets, hosts):
    # If a host is being used on phase1, store it on secrets_phase1,
    #  but also a modified version for the other phases
    secrets_phase1 = {}
    secrets_phase1['hosts'] = {}
    secrets_phase1['groups'] = {}
    secrets_others = {}
    secrets_others['hosts'] = {}
    secrets_others['groups'] = {}
    # Here we focus on the hosts with phase1
    for host in hosts:
        secrets_phase1['hosts'][host] = copy.deepcopy(secrets['hosts'][host])
        # Create different config for the host on phase1 here
        # TODO: If there is no config for later, Show error
        host_after_phase1 = {}
        host_after_phase1['ansible_ssh_port'] = secrets['groups']['phase1']['phase2_ansible_user']['ssh_port']
        host_after_phase1['ip'] = secrets['hosts'][host]['ip']
        ansible_user = {}
        ansible_user['name'] = secrets['groups']['phase1']['phase2_ansible_user']['name']
        ansible_user['password'] = secrets['groups']['phase1']['phase2_ansible_user']['password']
        ansible_user['ssh_key'] = secrets['groups']['phase1']['phase2_ansible_user']['ssh_key']
        ansible_user['ssh_path'] = secrets['groups']['phase1']['phase2_ansible_user']['ssh_path']
        host_after_phase1['ansible_user'] = ansible_user
        secrets_others['hosts'][host] = host_after_phase1
    secrets_phase1['groups']['phase1'] = copy.deepcopy(secrets['groups']['phase1'])

    for host in secrets['hosts']:
        if host not in hosts:
            secrets_others['hosts'][host] = secrets['hosts'][host]

    for group in secrets['groups']:
        if group != 'phase1':
            secrets_others['groups'][group] = secrets['groups'][group]
        else:
            phase1_group = {}
            phase1_group = secrets['groups']['phase1']
            phase1_group['hosts'] = []
            secrets_others['groups'][group] = phase1_group

    return secrets_phase1, secrets_others

def runOnHost(ip, hostname, host_details, commands):
    responses = []
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh_key_defined = host_details['ansible_user']['ssh_key']
            client.connect(str(ip), 
                port=host_details['ansible_ssh_port'], 
                username=host_details['ansible_user']['name'], 
                key_filename=ssh_key_defined,
                password=host_details['ansible_user']['password'],
                timeout=10)
        except:
            client.connect(str(ip), 
                port=host_details['ansible_ssh_port'], 
                username=host_details['ansible_user']['name'], 
                password=host_details['ansible_user']['password'],
                timeout=10)

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            responses.append(stdout.read().decode("utf-8").replace("\n","",1))
    except (paramiko.ssh_exception.NoValidConnectionsError, TimeoutError, socket.timeout, EOFError):
        for i in range(len(commands)):
            responses.append("Connection Error")
    finally:
        client.close()
    return responses

def getRealIP(hostname, host_details, ip_start, ip_end):
    command_getmac = 'cat /sys/class/net/eth0/address'
    start_ip = ipaddress.IPv4Address(ip_start)
    end_ip = ipaddress.IPv4Address(ip_end)
    print("looking for " + hostname + "'s new IP", end = '', flush=True)
    for ip_int in range(int(start_ip), int(end_ip)):
        print(".", end = '', flush=True)
        check_mac = runOnHost(ipaddress.IPv4Address(ip_int), hostname, host_details, [command_getmac])[0]
        if host_details['mac_address'] == check_mac:
            return str(ipaddress.IPv4Address(ip_int))

def getNetwork(secrets, ip_start, ip_end):
    command_getmac = 'cat /sys/class/net/eth0/address'
    command_hostname = 'hostname'
    for host in secrets['hosts']:
        # check all hosts for
        #  connection
        #  hostname
        #  mac address
        check_mac, check_hostname = runOnHost(secrets['hosts'][host]['ip'], host, secrets['hosts'][host], [command_getmac, command_hostname])
        if check_mac != secrets['hosts'][host]['mac_address']:
            print("there is something wrong with host " + host) 
            new_ip = getRealIP(host, secrets['hosts'][host], ip_start, ip_end)
            check_hostname = runOnHost(new_ip, host, secrets['hosts'][host], [command_hostname])[0]
            verbose(host + " seems to have changed to IP " + new_ip , 2)
            if check_hostname == "Connection Error":
                verbose("Also, an ssh with the previous ssh config failed: " + check_hostname, 2)
            elif check_hostname != host:
                verbose("Also, for whatever reason its hostname is now " + check_hostname, 2)
            verbose("You have to choose before automatically changing or doing it yourself before continuing...", 1)
            if getConfirmation("\n\n\n\nDo you want it to be automatically changed in your secrets.yaml?"):
                secrets['hosts'][host]['ip'] = new_ip
                saveTempSecrets(secrets, 'secrets.yaml')
                backupAndOverwrite('secrets.yaml', 'tmp/secrets.yaml', 'secrets.yaml.bkp.' + time.strftime("%Y%m%d-%H%M%S"))
            else:
                verbose("You have chosen to correct it yourself. Please run this script again after that", 1)
                sys.exit(1)


        else:
            print(check_hostname + " - " + check_mac)
        # if anything fails:
        #   try all ips, look for mac address
        #     found?
        #       get hostname too
        #       add to change_list
        #     not found?
        #       ask user what to do
        # change secrets


## General Use Functions
########################

def verbose(message, message_type):
    if message_type == 1:
        print("\n//===" + '='*len(message) + "===\\\\")
        print("||   " + message + "   ||")
        print("\\\===" + '='*len(message) + "===//")
    elif message_type == 2:
        print("\n  --" + '-'*len(message) + "--")
        print("  | " + message + " |")
        print("  --" + '-'*len(message) + "--")
    elif message_type == 3:
        print("\n    -- " + message + " --")

def cleanupFolder(folder):
    files = glob.glob(folder + '/*')
    for f in files:
        verbose("removing old " + f, 3)
        os.remove(f)


def getConfirmation(message):
    answer = ""
    while answer not in ["y", "n"]:
        answer = input(message + " [Y/N]? ").lower()
    return answer == "y"

def getSaltedPassword(password):
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    return crypt.crypt(password, salt)

def getSecrets(filename):
    ''' Loads a yaml file of secrets and configs into a structure, returns it
    '''
    with open(filename) as file:
        secrets = yaml.safe_load(file)
    return secrets

def showHelp():
    print("SYNTAX: " + sys.argv[0] + " [init|create|make|apply]")
    sys.exit(1)


if __name__ == "__main__":
    LOCAL_IP_RANGE = ['192.168.0.1', '192.168.255.255'] # Modify this if it takes too long to check through all the IPs
    SECRETS_TEMPLATE = 'secrets.yaml.template'
    SECRETS_FILE = 'secrets.yaml'
    TEMPLATES_FOLDER = 'templates'
    MANIFESTS_FOLDER = 'manifests'
    TMP_FOLDER = 'tmp'

    if len(sys.argv) != 2:
        showHelp()
    else:
        if sys.argv[1] == "init":
            init(getSecrets(SECRETS_FILE), TEMPLATES_FOLDER, MANIFESTS_FOLDER)
        elif sys.argv[1] == "create":
            createSecrets(SECRETS_TEMPLATE, SECRETS_FILE)
        elif sys.argv[1] == "plan":
            plan(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
        elif sys.argv[1] == "apply":
            plan(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
            if getConfirmation("\n\n\n\nDo you want to apply?"):
                apply(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
        elif sys.argv[1] == "network":
            getNetwork(getSecrets(SECRETS_FILE), LOCAL_IP_RANGE[0], LOCAL_IP_RANGE[1])
        else:
            showHelp()

