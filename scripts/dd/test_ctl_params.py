import ctl_params


class TestParameterMap:
    @classmethod
    def setup_class(cls):
        pass

    def test_check_input(self):
        """Must return correct response to test case."""

        self.params = ctl_params.ParameterMap("parametermap.json")
        test_input = self.params.check_args_input(["test", "get", "nodes", "all"])
        assert test_input == ["docker get nodes", "all"]
