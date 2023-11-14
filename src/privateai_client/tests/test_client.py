import pytest

from ..pai_client import PAIClient


def test_initialization_with_auth():
    client = PAIClient("http", "localhost", "8080", api_key="test")
    assert client.get.headers["x-api-key"] == "test"
    client = PAIClient("http", "localhost", "8080", bearer_token="test")
    assert client.get.headers["Authorization"] == "Bearer test"


def test_initialization_error_message():
    with pytest.raises(ValueError) as e:
        client = PAIClient()

    assert e.match(
        "PAIClient needs either a url, or a scheme and host to initialize. You can find more information on which url to use here: https://docs.private-ai.com/thin-client/"
    )
