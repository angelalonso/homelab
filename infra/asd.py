import crypt
import glob
import os
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
    hosts_file = templates_folder + 'hosts'
    groups = defaultdict(list)

    groups = defaultdict(list)
    for key, var in secrets["hosts"].items():
        for hostgroup in secrets["hosts"][key]["hostgroups"]:
            groups[hostgroup].append(key)
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)

    template_hosts = env.get_template('hosts')
    print(template_hosts.render(secrets=secrets, groups=groups))

    template_hosts = env.get_template('playbooks.yaml')
    print(template_hosts.render(secrets=secrets, getSaltedPassword=getSaltedPassword))

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

if __name__ == "__main__":
    SECRETS_FILE = './secrets.yaml'
    TEMPLATES_FOLDER = './templates'
    MANIFESTS_FOLDER = './manifests'

    clenaupManifests(MANIFESTS_FOLDER)
    #createManifests(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
    createTemplatedManifests(getSecrets(SECRETS_FILE), TEMPLATES_FOLDER, MANIFESTS_FOLDER)
