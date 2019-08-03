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
        if input[1] in self.map["params"]:
            print("ok")
        else:
            self.show_help(input)

    def print_map(self):
        print(self.map)

    def show_help(self, input):
        print(input[0] + " syntax:\n")
        print("Commands:")
        for command in self.map["params"]:
            print("  " + command)
            for subcommand in self.map["params"][command]:
                print("    " + subcommand["subparam"] + "\t\t" + subcommand["help"])

