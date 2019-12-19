import crypt
import glob
import os
import subprocess
import sys
import yaml

from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


# No Jinja
def addServerToHosts(string, folder):
    hosts_filename = folder + '/hosts'
    with open(hosts_filename, "a") as hostsfile:
        hostsfile.write(string)

def addGroupsToHosts(groups, folder):
    hosts_filename = folder + '/hosts'
    for group in groups:
        with open(hosts_filename, "a") as hostsfile:
            hostsfile.write("\n[" + group + "]\n")
        for host in groups[group]:
            with open(hosts_filename, "a") as hostsfile:
                hostsfile.write(host + "\n")

def createManifests(secrets, folder):
    hosts_filename = folder + '/hosts'
    groups = defaultdict(list)
    for key, var in secrets["hosts"].items():
        for hostgroup in secrets["hosts"][key]["hostgroups"]:
            groups[hostgroup].append(key)
        line = key + " ansible_ssh_host=" + secrets["hosts"][key]["ip"] + \
                " ansible_ssh_user=" + secrets["hosts"][key]["ssh_user"] + \
                " ansible_ssh_pass=" + secrets["hosts"][key]["ssh_pass"] + "\n"
        addServerToHosts(line, folder)
    addGroupsToHosts(groups, folder)

# Jinja
def createTemplatedManifests(secrets, templates_folder, manifests_folder):
    hosts_file = 'hosts'
    playbooks_file = 'playbooks.yaml'

    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)

    template_hosts = env.get_template(hosts_file)

    with open(manifests_folder + '/' + hosts_file, "w") as fh:
        fh.write(template_hosts.render(secrets=secrets))

    template_hosts = env.get_template(playbooks_file)

    with open(manifests_folder + '/' + playbooks_file, "w") as fm:
        fm.write(template_hosts.render(secrets=secrets, getSaltedPassword=getSaltedPassword))

def getSaltedPassword(password):
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    return crypt.crypt(password, salt)

def getSecrets(filename):
    with open(filename) as file:
        secrets = yaml.safe_load(file)
    return secrets

def clenaupManifests(folder):
    files = glob.glob(folder + '/*')
    for f in files:
        os.remove(f)

def init():
    clenaupManifests(MANIFESTS_FOLDER)
    #createManifests(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
    createTemplatedManifests(getSecrets(SECRETS_FILE), TEMPLATES_FOLDER, MANIFESTS_FOLDER)

def plan():
    print("Planning")
    subprocess.run(["ansible-playbook", "-i", "./manifests/hosts", "./manifests/playbooks.yaml", "--check"])
    # this fails
    #print(sh.ansible-playbook("-i", "./manifests/hosts", "./manifests/playbooks.yaml", "--check"))

def apply():
    print("Applying")
    subprocess.run(["ansible-playbook", "-i", "./manifests/hosts", "./manifests/playbooks.yaml"])

def showHelp():
    print("SYNTAX: " + sys.argv[0] + " [init|make|apply]")
    sys.exit(1)

if __name__ == "__main__":
    SECRETS_FILE = 'secrets.yaml'
    TEMPLATES_FOLDER = 'templates'
    MANIFESTS_FOLDER = 'manifests'

    if len(sys.argv) != 2:
        showHelp()
    else:
        if sys.argv[1] == "init":
            init()
        elif sys.argv[1] == "plan":
            plan()
        elif sys.argv[1] == "apply":
            apply()
        else:
            showHelp()

