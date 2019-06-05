"""Get new code into a docker image

- Builds a list of git folders to check,
- Pulls master, throws possible errors,
- Checks for changes in the 'VERSION' file,
- If it changed, it runs 'test.sh',
- Builds the image,
- Pushes to Dockerhub.

"""
import argparse
import git
import json
import os
import sh
import subprocess
import sys

def getConfig(filename):
    """- Builds a list of git folders to check,
    """
    with open(filename) as json_file:  
        data = json.load(json_file)
    return data

def getMasterChanges(git_dir):
    """- Pulls master, throws possible errors,
    """
    try:
        repo = git.Repo(git_dir)
    except git.exc.InvalidGitRepositoryError as gitErr: 
        return gitErr
    try:
        repo.remotes.origin.pull()
    except git.exc.GitCommandError as gitErr: 
        return gitErr

def doVersionsMatch(version_filename, version):
    """- Checks for changes in the 'VERSION' file,
    """
    try:
        with open (version_filename, "r") as myfile:
            version_file = myfile.read().replace('\n', '')
    except FileNotFoundError:
        version_file = ""
    if version != version_file:
        return False
    else:
        return True

def runTest(app_dir):
    """- Runs 'run_tests.sh', located on the provided folder
    """
    print(" - Running tests on " + app_dir + "...")
    try:
        print(sh.bash(app_dir + "/run_tests.sh"))
    except sh.ErrorReturnCode:
        return False
    return True

def buildImage(app_dir):
    """- Builds the image,
    """
    pass

def pushImage():
    """- Pushes to Dockerhub.
    """
    pass

def createParser():
    # TODO: add a helper function
    parser = argparse.ArgumentParser()  
    parser.add_argument("-D", "--directory", help="full path of the main git directory")
    return parser

def checkArgs(args):
    # https://stackabuse.com/command-line-arguments-in-python/
    if args.directory:  
        main_git_dir = args.directory
    else:
        # NOTE: I assume the current structure of this repo
        main_git_dir = os.getcwd() + "/.."
    return main_git_dir

def mainLogic(main_git_dir):
    configfile = 'apps.json'
    apps = getConfig(configfile)
    gitErr = getMasterChanges(main_git_dir)
    if gitErr != None:
        print("ERROR: the provided folder, " + main_git_dir + " is not the main directory of a Git repo")
        sys.exit(2)
    for app in apps:
        print(app)
        app_dir = main_git_dir + "/" + apps[app]['dir']
        if not doVersionsMatch(app_dir + "/VERSION", apps[app]['version']):
            print(" - " + app + " will be rebuilt")
            if runTest(app_dir):
                print(" - test passed")
                build(app_dir)
            else:
                print(" - test FAILED")
        else: 
            print(" - " + app + " does not need a rebuilt")


if __name__ == '__main__':
    args = createParser().parse_args()
    mainLogic(checkArgs(args))
