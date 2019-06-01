"""Get new code into a docker image

- Builds a list of git folders to check,
- Checks for changes in master,
- Pulls if needed,
- Checks for changes in the 'VERSION' file,
- If it changed, it runs 'test.sh',
- Builds the image,
- Pushes to Dockerhub.

"""

def getConfig():
    """- Builds a list of git folders to check,
    """
    pass

def GetMasterChanges():
    """- Checks for changes in master,
    - Pulls if needed,
    """
    pass

def CheckVersion():
    """- Checks for changes in the 'VERSION' file,
    """
    pass

def RunTest():
    """- If it changed, it runs 'test.sh',
    """
    pass

def BuildImage():
    """- Builds the image,
    """
    pass

def PushImage():
    """- Pushes to Dockerhub.
    """
    pass

