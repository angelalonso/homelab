import d8s


class TestD8s:
    @classmethod
    def setup_class(cls):
        pass

    def test_get_nodes(self):
        """Must return correct response to test case."""

        test_input_1param = d8s.get_nodes(["hello"])
        assert test_input_1param == "you got this far hello"
