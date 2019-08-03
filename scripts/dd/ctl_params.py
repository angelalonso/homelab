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
    def __init__(self, filename, input):
        self.filename = filename
        with open(filename, 'r') as f:
            self.map = json.load(f)
        self.check_input(input)

# TODO 
# - execute command from the mapped action
# - generate help automatically

    def check_input(self, input):
        print(input[1])
        if input[1] in self.map["params"]:
            print("ok")
        else:
            self.show_help()

    def print_map(self):
        print(self.map)

    def show_help(self):
        print("Error!")

