import ctl_params


class TestParameterMap:
    @classmethod
    def setup_class(cls):
        pass

    def test_check_input(self):
        """Must return correct response to test case."""

        self.params = ctl_params.ParameterMap("parametermap.json")

        test_input_noparam = self.params.check_args_input(["test"])
        assert test_input_noparam == "Error: not enough parameters for test"

        test_input_errparam = self.params.check_args_input(["test", "nodes", "all"])
        assert test_input_errparam == "Error: wrong parameter for test"

        test_input_1param = self.params.check_args_input(["test", "get", "all"])
        assert test_input_1param == "Error: wrong or not enough parameters for get"

        test_input_2param = self.params.check_args_input(["test", "get", "nodes", "all"])
        assert test_input_2param == ["get_nodes", "all"]

        test_filenotfound = self.params.load_parametermap_file("test_parametermap.json")
        assert test_filenotfound == "Error: parameter map json file not found"

        test_search_command = self.params.search_command(["test", "get", "nodes", "all"])
        assert test_search_command == ["get_nodes", "all"]

        test_showhelp = self.params.show_help(["test", "get", "nodes", "all"])
        assert test_showhelp is None
