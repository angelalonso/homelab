import ctl_params


class TestParameterMap:
    @classmethod
    def setup_class(cls):
        pass

    def test_check_input(self):
        """Must return correct response to test case."""

        self.params = ctl_params.ParameterMap("test_parametermap.json", ["get", "all"])
        assert self.params.map == []
