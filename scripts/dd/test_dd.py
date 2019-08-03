import pytest

import dd


# Boilerplate code to mock Requests library.
@pytest.fixture
def m_requests(request):
    with requests_mock.Mocker() as m:
        yield m


class TestCloudflareIpChange:
    @classmethod
    def setup_class(cls):
        pass

    def test_get_current(self, m_requests):
        """Must return decoded JSON response."""

        # Test parameters: URL and expected payload.
        url = "http://example.com"
        payload = {'foo': 'bar'}

        # Configure the Request mock.
        m_requests.request(
            "get",
            url,
            json=payload,
            status_code=200,
        )

        # Call our function and verify it used Request correctly and returns
        # the decoded JSON response.
        assert cic.get_current(url) == payload
