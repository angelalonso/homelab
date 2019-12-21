import crypt
import glob
import os
import shutil
import subprocess
import sys
import yaml

from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

def createNewGroupsConfigFiles(secrets, templates_folder, manifests_folder):
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    for group in secrets['groups']:
        if group.startswith('new_'):
            if (secrets['groups'][group] is None) or (secrets['groups'][group]['hosts'] is None):
                print(group + " is empty. Nothing to be done there.")
            else:
                cfg_ssh_file = 'sshd_config'
                template_cfg_ssh = env.get_template(cfg_ssh_file)
                with open(manifests_folder + '/' + cfg_ssh_file + '_' + group, "w") as fcssh:
                    fcssh.write(template_cfg_ssh.render(secrets_group=secrets['groups'][group]))

def createNewGroupsPlaybooks(secrets, templates_folder, manifests_folder):
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    # templated playbooks per group
    for group in secrets['groups']:
        if group.startswith('new_'):
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

def createNotNewGroupsConfigFiles(secrets, templates_folder, manifests_folder):
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    for group in secrets['groups']:
        if not group.startswith('new_'):
            if (secrets['groups'][group] is None) or (secrets['groups'][group]['hosts'] is None):
                print(group + " is empty. Nothing to be done there.")
            else:
                cfg_ssh_file = 'sshd_config'
                template_cfg_ssh = env.get_template(cfg_ssh_file)
                with open(manifests_folder + '/' + cfg_ssh_file + '_' + group, "w") as fcssh:
                    fcssh.write(template_cfg_ssh.render(secrets_group=secrets['groups'][group]))

def createNotNewGroupsPlaybooks(secrets, templates_folder, manifests_folder):
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    # templated playbooks per group
    for group in secrets['groups']:
        if not group.startswith('new_'):
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

def createNewGroupsManifests(secrets, templates_folder, manifests_folder):
    verbose("Creating manifests for new_ groups", 1)
    hosts_file = 'hosts_new'
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    for group in secrets['groups']:
        if group.startswith('new_'):
            verbose("Manifest for " + group + " created", 3)
            # hosts inventory
            template_hosts = env.get_template(hosts_file)
            with open(manifests_folder + '/hosts_' + group, "w") as fh:
                fh.write(template_hosts.render(secrets=secrets))
            # config files
            createNewGroupsConfigFiles(secrets, templates_folder, manifests_folder)
            # playbooks
            createNewGroupsPlaybooks(secrets, templates_folder, manifests_folder)

def createNotNewGroupsManifests(secrets, templates_folder, manifests_folder):
    verbose("Creating manifests for NON new_ groups", 1)
    hosts_file = 'hosts_notnew'
    env = Environment(loader = FileSystemLoader(templates_folder), trim_blocks=True, lstrip_blocks=True)
    for group in secrets['groups']:
        if not group.startswith('new_'):
            verbose("Manifest for " + group + " created", 3)
            # hosts inventory
            template_hosts = env.get_template(hosts_file)
            with open(manifests_folder + '/hosts_' + group, "w") as fh:
                fh.write(template_hosts.render(secrets=secrets))
            # config files
            createNotNewGroupsConfigFiles(secrets, templates_folder, manifests_folder)
            # playbooks
            createNotNewGroupsPlaybooks(secrets, templates_folder, manifests_folder)

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
        verbose("removing old " + f, 3)
        os.remove(f)

def getConfirmation(message):
    answer = ""
    while answer not in ["y", "n"]:
        answer = input(message + " [Y/N]? ").lower()
    return answer == "y"

def init(secrets, templates_folder, manifests_folder):
    verbose("Cleaning Manifests folder", 1)
    cleanupManifests(manifests_folder)
    verbose("Creating Manifests", 1)
    createNewGroupsManifests(secrets, templates_folder, manifests_folder)
    createNotNewGroupsManifests(secrets, templates_folder, manifests_folder)

def plan(secrets, manifests_folder):
    verbose("Planning playbooks", 1)
    if 'new_' in str(secrets['groups'].keys()):
        verbose("Planning only new_ groups", 2)
        for group in secrets['groups']:
            if group.startswith('new_'):
                playbook_file = manifests_folder + "/playbook_" + group + ".yaml"
                if os.path.isfile(playbook_file):
                    subprocess.run(["ansible-playbook", "-i", "./manifests/hosts_" + group, playbook_file, "--check"])
    else:
        verbose("Planning all groups", 2)
        for group in secrets['groups']:
            playbook_file = manifests_folder + "/playbook_" + group + ".yaml"
            if os.path.isfile(playbook_file):
                subprocess.run(["ansible-playbook", "-i", "./manifests/hosts_" + group, playbook_file, "--check"])

def apply(secrets, manifests_folder):
    verbose("Applying playbooks", 1)
    verbose("Applying first the _new groups", 2)
    for group in secrets['groups']:
        if group.startswith('new_'):
            playbook_file = manifests_folder + "/playbook_" + group + ".yaml"
            if os.path.isfile(playbook_file):
                subprocess.run(["ansible-playbook", "-i", "./manifests/hosts_" + group, playbook_file])

    if 'new_' in str(secrets['groups'].keys()):
        removeNewFromSecrets(secrets)
    verbose("Applying then the NON _new groups", 2)
    for group in secrets['groups']:
        if not group.startswith('new_'):
            playbook_file = manifests_folder + "/playbook_" + group + ".yaml"
            if os.path.isfile(playbook_file):
                subprocess.run(["ansible-playbook", "-i", "./manifests/hosts_" + group, playbook_file])

def removeNewFromSecrets(secrets):
    for group in list(secrets['groups']):
        if group.startswith('new_'):
            secrets['groups'].pop(group)

    if getConfirmation("The 'new_' groups are no longer needed/working\n Do you want to remove them from your secrets.yaml?"):
        dest = shutil.copyfile('secrets.yaml', 'secrets.yaml.bkp')
        with open(r'secrets.yaml', 'w') as file:
            document = yaml.dump(secrets, file)
        verbose("Your original secrets.yaml has been saved under secrets.yaml.bkp", 2)

def verbose(message, message_type):
    if message_type == 1:
        print("//===" + '='*len(message) + "===\\\\")
        print("||   " + message + "   ||")
        print("\\\===" + '='*len(message) + "===//")
    elif message_type == 2:
        print("  --" + '-'*len(message) + "--")
        print("  | " + message + " |")
        print("  --" + '-'*len(message) + "--")
    elif message_type == 3:
        print("    -- " + message + " --")

def showHelp():
    print("SYNTAX: " + sys.argv[0] + " [init|make|apply]")
    sys.exit(1)

def test(secrets, templates_folder, manifests_folder):
    print(secrets)
    print("")
    for group in list(secrets['groups']):
        if group.startswith('new_'):
            secrets['groups'].pop(group)
    print(secrets)
    print("")

    with open(r'secrets_clean.yaml', 'w') as file:
        documents = yaml.dump(secrets, file)

if __name__ == "__main__":
    SECRETS_FILE = 'secrets.yaml'
    TEMPLATES_FOLDER = 'templates'
    MANIFESTS_FOLDER = 'manifests'

    if len(sys.argv) != 2:
        showHelp()
    else:
        if sys.argv[1] == "init":
            init(getSecrets(SECRETS_FILE), TEMPLATES_FOLDER, MANIFESTS_FOLDER)
        elif sys.argv[1] == "test":
            test(getSecrets(SECRETS_FILE), TEMPLATES_FOLDER, MANIFESTS_FOLDER)
        elif sys.argv[1] == "plan":
            plan(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
        elif sys.argv[1] == "apply":
            apply(getSecrets(SECRETS_FILE), MANIFESTS_FOLDER)
        else:
            showHelp()

