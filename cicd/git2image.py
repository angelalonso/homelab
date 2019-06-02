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

# TODO: instead, let's just pull latest and check change of version somewhere else
def getMasterChanges():
    """- Checks for changes in master,
    - Pulls if needed,
    """
    working_tree_dir = '/home/aaf/Software/Dev/homelab'
    repo = Repo(working_tree_dir)
    commit_dev = repo.commit("master")
    commit_origin_dev = repo.commit("origin/master")
    diff_index = commit_origin_dev.diff(commit_dev)

    #TODO: Check only VERSION on the folder we want 
    for diff_item in diff_index.iter_change_type('M'):
        print(diff_item.a_path)
        print("{}".format(diff_item.a_blob.data_stream.read().decode('utf-8')))
        print("{}".format(diff_item.b_blob.data_stream.read().decode('utf-8')))

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
