import pytest

import asd

class TestAll:
    @classmethod
    def setup_class(cls):
        pass

    def test_getSecrets(self):
        """Must return decoded YAML response."""
        filename = './secrets_test.yaml'
        secrets = {'hosts': {'test01': {'users': {'name': 'testuser', 'password': 'testpass'}}}}

        assert asd.getSecrets(filename) == secrets
