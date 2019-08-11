"""Docker Swarm Controller

Use case:
    This program is meant to help manage docker swarm, wrapping some commands up
"""
import sys
import paramctl
#import ctl_params
import sh


def get_nodes(*argv):
    args = " "
    print(sh.kubectl("--kubeconfig", "/home/aaf/.kube/config.testing", "get", "no"))
    for arg in argv:
        args = args.join(arg)
    return "you got this far " + args


if __name__ == '__main__':
    """
    Calls the ctl_params library to retrieve the function name
      and parameters, according to the parametermap loaded,
      then calls the corresponding function
    """
    #params = ctl_params.ParameterMap("parametermap.json")
    params = paramctl.ParameterMap("parametermap.json")

    # This builds  and runs the call to a function dinamically
    function = params.check_args_input(sys.argv)
    try:
        print(globals()[function[0]](function[1:]))
    except KeyError:
        print("No function available like " + " ".join(function[:]))
