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
        try:
            if args_input[1] in self.map["params"]:
                return self.search_command(args_input)
            else:
                return "Error: wrong parameter for " + args_input[0]
                self.show_help(args_input)
        except IndexError:
            self.show_help(args_input)
            return "Error: not enough parameters for " + args_input[0]

    def search_command(self, args_input):
        """
        Looks for the command to be returned and adds any additional
          parameter as complementary
        """
        # NOTE: so far this only goes two levels down. Modify if needed
        # TODO: one day, open up the possibility for indefinite levels
        if len(args_input) > 2:
            try:
                return [self.map["params"][args_input[1]][args_input[2]]["action"]] \
                    + args_input[3:]
            except KeyError:
                try:
                    return [self.map["params"][args_input[1]]["action"]] \
                        + args_input[2:]
                except KeyError:
                    self.show_help(args_input)
                    return "Error: wrong or not enough parameters for " + args_input[1]

    def show_help(self, args_input):
        """
        Builds a list of helping lines from the parameter
          map received, and prints it.
        """
        print("Syntax:\n")
        print(args_input[0] + " [command] [object] [extra parameters]\n")
        print("Commands / objects:")
        for command in self.map["params"]:
            print("  " + command)
            for subcommand in self.map["params"][command]:
                print("    " + subcommand + "\t"
                      + self.map["params"][command][subcommand]["help"])  # noqa: W503
        print("\n")
