import sys
import sh
import platform
"""
- Check we are running the latest version of this program
  - If not, download latest
- Do something
"""

def run_default(maincommand, ARGS):
    comm = '/usr/local/bin/' + maincommand.replace("\n", "") + ' ' + str(' '.join(ARGS))
    print(sh.zsh('-c', comm))

def get_alias(main_command):
    return sh.zsh('-c', 'source /Users/a.fonseca/.zshrc && alias kkst').split("=")[1].replace("'", "")

def am_I_latest():
    """
    Check if the current version is the latest at master
    , and returns:
    - True/False if it's up to date
    - the details if it's not up to date
    """

    upToDate = """On branch master
Your branch is up to date with 'origin/master'.

nothing to commit (use -u to show untracked files)
"""
    check = sh.git.status('-uno')
    if str(check) == upToDate:
        result = True
        return True, ""
    else:
        return False, str(check)


if __name__ == "__main__":
    #maincommand = 'kk' + sys.argv[1]
    #ARGS = sys.argv[2:]
    #run_default(get_alias(maincommand), ARGS)
    #print(platform.system())
    uptodate, err = am_I_latest()
    if uptodate:
        print("Continuing")
    else:
        print( \
                "                  ERROR                 \n" + \
                " Please, solve the following conflicts  \n" + \
                " , and get the latest master branch     \n" + \
                "      before using this program         \n" + \
                "----------------------------------------\n")
        print(err)
    

