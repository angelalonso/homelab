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
        self.map = self.load_parametermap_file(filename)
# TODO
# - send back action to take from the parameters read

    def load_parametermap_file(self, filename):
        """
        Load the parameter map from a file
        """
        params_map = []
        try:
            with open(filename, 'r') as f:
                params_map = json.load(f)
        except FileNotFoundError:
            return "Error: parameter map json file not found"
        return params_map

    def check_args_input(self, args_input):
        """
        Check that the received args_input matches the parameter
          map we have configured.

        If so, it continues.
        If not, it calls the function to show help.
        """
        if len(args_input) < 2:
            self.show_help(args_input)
        elif args_input[1] in self.map["params"]:
            return args_input[1]
        else:
            self.show_help(args_input)

    def show_help(self, args_input):
        """
        Builds a list of helping lines from the parameter
          map received, and prints it.
        """
        print(args_input[0] + " syntax:\n")
        print("Commands:")
        for command in self.map["params"]:
            print("  " + command)
            for subcommand in self.map["params"][command]:
                print("    " + subcommand["subparam"] + "\t\t" + subcommand["help"])
