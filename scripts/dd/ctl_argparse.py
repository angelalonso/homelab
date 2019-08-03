"""Controller-style Argument Parser

    Adds a little bit of logic on the parsing of arguments, controlling 
      what arguments are valid on the first layer,
      which ones are valid on the second, depending
      on the first layer...and so on

Use case:
    main_program.py get list
    main_program.py edit object
    main_program.py edit list
"""
import json

class ParameterMap:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            self.map = json.load(f)
# TODO execute command from the mapped action
#  checking first if the parameter is correct
    def print_map(self):
        print(self.map)


