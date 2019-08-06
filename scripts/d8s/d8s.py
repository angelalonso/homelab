"""Docker Swarm Controller

Use case:
    This program is meant to help manage docker swarm, wrapping some commands up
"""
import sys
import ctl_params


def get_nodes(*argv):
    args = " "
    for arg in argv:
        args = args.join(arg)
    return "you got this far " + args


if __name__ == '__main__':
    """
    Calls the ctl_params library to retrieve the function name
      and parameters, according to the parametermap loaded,
      then calls the corresponding function
    """
    params = ctl_params.ParameterMap("parametermap.json")

    # This builds  and runs the call to a function dinamically
    function = params.check_args_input(sys.argv)
    print(globals()[function[0]](function[1:]))
