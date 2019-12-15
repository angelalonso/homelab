import glob
import os
import yaml

def addToHosts(string, folder):
    hosts_filename = folder + '/hosts'
    with open(hosts_filename, "a") as hostsfile:
        hostsfile.write(string)

def createManifests(secrets, folder):
    hosts_filename = folder + '/hosts'
    for key, var in secrets["hosts"].items():
        for key2, var2 in secrets["hosts"][key].items():
            line = key + " ansible_ssh_host=" + secrets["hosts"][key]["ip"] + \
                    " ansible_ssh_user=" + secrets["hosts"][key]["ssh_user"] + \
                    " ansible_ssh_pass=" + secrets["hosts"][key]["ssh_pass"] + "\n"
        addToHosts(line, folder)

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
    MANIFESTS_FOLDER = './manifests'

    clenaupManifests(MANIFESTS_FOLDER)
    createManifests(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
