"""Docker Swarm Controller

Use case:
    This program is meant to help manage docker swarm, wrapping some commands up
"""
import sys
import ctl_params

if __name__ == '__main__':
    """ 
    """
    params = ctl_params.ParameterMap("parametermap.json")
    params.print_map()
