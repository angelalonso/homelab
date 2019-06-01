"""Get new code into a docker image

- Builds a list of git folders to check,
- Checks for changes in master,
- Pulls if needed,
- Checks for changes in the 'VERSION' file,
- If it changed, it runs 'test.sh',
- Builds the image,
- Pushes to Dockerhub.

"""
import json
import subprocess
from git import Repo

def getConfig(filename):
    """- Builds a list of git folders to check,
    """
    with open(filename) as json_file:  
        data = json.load(json_file)
    return data

def getMasterChanges():
    """- Checks for changes in master,
    - Pulls if needed,
    """
    working_tree_dir = '/home/aaf/Software/Dev/homelab'
    repo = Repo(working_tree_dir)
    current_hash = repo.head.object.hexsha
    o = repo.remotes.origin
    o.pull()
    pull_hash = repo.head.object.hexsha
    if current_hash != pull_hash:
        print("files have changed")
    else:
        print("no changes")
    #git pull > /dev/null 2>&1

def checkVersion():
    """- Checks for changes in the 'VERSION' file,
    """
    pass

def runTest():
    """- If it changed, it runs 'test.sh',
    """
    pass

def buildImage():
    """- Builds the image,
    """
    pass

def pushImage():
    """- Pushes to Dockerhub.
    """
    pass

def main():
    configfile = 'apps.json'
    apps = getConfig(configfile)
    for app in apps:
        print(app)
    getMasterChanges()

if __name__ == '__main__':
    main()
