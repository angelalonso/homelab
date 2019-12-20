import crypt
import glob
import os
import subprocess
import sys
import yaml

from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

def createInventory():
    pass

def createPlaybooksPerGroup(secrets, templates_folder, manifests_folder):
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    # templated playbooks per group
    for group in secrets['groups']:
        print(group)
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

def createConfigFiles(secrets, templates_folder, manifests_folder):
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    for group in secrets['groups']:
        if secrets['groups'][group] is None:
            print(group + " is empty. Nothing to be done there.")
        else:
            cfg_ssh_file = 'sshd_config'
            template_cfg_ssh = env.get_template(cfg_ssh_file)
            with open(manifests_folder + '/' + group + '_' + cfg_ssh_file, "w") as fcssh:
                fcssh.write(template_cfg_ssh.render(secrets_group=secrets['groups'][group]))

def createTemplatedManifests(secrets, templates_folder, manifests_folder):
    hosts_file = 'hosts'
    playbooks_file = 'playbooks.yaml'

    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)

    # templated hosts inventory
    template_hosts = env.get_template(hosts_file)
    with open(manifests_folder + '/' + hosts_file, "w") as fh:
        fh.write(template_hosts.render(secrets=secrets))
    # templated config files
    #  sshd config
    createConfigFiles(secrets, templates_folder, manifests_folder)
    # templated playbook(s)
    createPlaybooksPerGroup(secrets, templates_folder, manifests_folder)
    ##  template_playbooks = env.get_template(playbooks_file)
    ##  with open(manifests_folder + '/' + playbooks_file, "w") as fm:
    ##      fm.write(template_playbooks.render(secrets=secrets, getSaltedPassword=getSaltedPassword))

def getSaltedPassword(password):
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    return crypt.crypt(password, salt)

def getSecrets(filename):
    with open(filename) as file:
        secrets = yaml.safe_load(file)
    return secrets

def cleanupManifests(folder):
    files = glob.glob(folder + '/*')
    for f in files:
        print("removing old " + f)
        os.remove(f)

def init():
    cleanupManifests(MANIFESTS_FOLDER)
    createTemplatedManifests(getSecrets(SECRETS_FILE), TEMPLATES_FOLDER, MANIFESTS_FOLDER)
#    createPlaybooksPerGroup(getSecrets(SECRETS_FILE), TEMPLATES_FOLDER, MANIFESTS_FOLDER)

def plan(secrets, manifests_folder):
    print("Planning")
    for group in secrets['groups']:
        playbook_file = manifests_folder + "/playbook_" + group + ".yaml"
        if os.path.isfile(playbook_file):
            subprocess.run(["ansible-playbook", "-i", "./manifests/hosts", playbook_file, "--check"])
    # this fails
    #print(sh.ansible-playbook("-i", "./manifests/hosts", "./manifests/playbooks.yaml", "--check"))

def apply():
    print("Applying")
    for group in secrets['groups']:
        playbook_file = manifests_folder + "/playbook_" + group + ".yaml"
        if os.path.isfile(playbook_file):
            subprocess.run(["ansible-playbook", "-i", "./manifests/hosts", playbook_file])

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
            plan(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
        elif sys.argv[1] == "apply":
            apply(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
        else:
            showHelp()

