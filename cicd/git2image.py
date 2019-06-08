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

def getVersionFromFile(version_filename):
    """- Gets content of the 'VERSION' file,
    """
    try:
        with open (version_filename, "r") as myfile:
            version_file = myfile.read().replace('\n', '')
    except FileNotFoundError:
        version_file = ""
    return version_file


def doVersionsMatch(version_filename, version):
    """- Checks for changes in the 'VERSION' file,
    """
    version_file = getVersionFromFile(version_filename)
    if version != version_file:
        return False
    else:
        return True

def runTest(app_dir):
    """- Runs 'run_tests.sh', located on the provided folder
    """
    print(" - Running tests on " + app_dir + "...")
    try:
        sh.bash(app_dir + "/run_tests.sh", _out=sys.stdout)
    #except sh.ErrorReturnCode:
    except Exception as e:
        print("Error!")
        print(e)
        return False
    return True

def buildImage(app, version, app_dir):
    """- Builds the image,
    """
    print(" - Building image from " + app_dir + "...")
    try:
        sh.docker.build("-t", app + ":" + version, app_dir + "/.", _out=sys.stdout)
    #except sh.ErrorReturnCode:
    except Exception as e:
        print("Error!")
        print(e)
        return False
    return True

def pushImage(dockeruser, app, version, app_dir):
    """- Pushes to Dockerhub.
    """
    print(" - Pushing image " + app_dir + "...")
    sh.docker.tag(app + ":" + version, dockeruser + "/" + app + ":" + version, _out=sys.stdout)
    sh.docker.push(dockeruser + "/" + app + ":" + version, _out=sys.stdout)
    return True
    pass

def createParser():
    # TODO: add a helper function
    parser = argparse.ArgumentParser()  
    parser.add_argument("-D", "--directory", help="full path of the main git directory")
    parser.add_argument("-U", "--dockeruser", help="username for dockerhub account to upload to")
    return parser

def checkArgs(args, parser):
    # https://stackabuse.com/command-line-arguments-in-python/
    if not (args.dockeruser):
        parser.error("No Dockerhub username was provided. Please do so by adding -U <your docker user>")
    if args.directory:  
        main_git_dir = args.directory
    else:
        # NOTE: I assume the current structure of this repo
        main_git_dir = os.getcwd() + "/.."
    return main_git_dir

def mainLogic(main_git_dir, dockeruser):
    mainfolder = os.path.dirname(__file__)
    configfile = mainfolder + '/apps.json'
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
                if buildImage(app, getVersionFromFile(app_dir + "/VERSION"), app_dir):
                    if pushImage(dockeruser, app, getVersionFromFile(app_dir + "/VERSION"), app_dir):
                        print(" - DONE")
                    else:
                        print(" - Push to dockerhub FAILED")
                else:
                    print(" - Build FAILED")
            else:
                print(" - Test FAILED")
        else: 
            print(" - " + app + " does not need a rebuilt")


if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    mainLogic(checkArgs(args, parser), args.dockeruser)
