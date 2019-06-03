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
    repo = git.Repo(git_dir)
    try:
        repo.remotes.origin.pull()
    except git.exc.GitCommandError as gitErr: 
        return gitErr

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
        sys.exit(2)
    for app in apps:
        pass
        #TODO: check VERSION, continue testing and building

if __name__ == '__main__':
    args = createParser().parse_args()
    mainLogic(checkArgs(args))
