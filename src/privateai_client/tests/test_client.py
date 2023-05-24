from ..pai_client import PAIClient


def test_initialization_with_auth():
    client = PAIClient("http", "localhost", "8080", api_key="test")
    assert client.get.headers["x-api-key"] == "test"
    client = PAIClient("http", "localhost", "8080", bearer_token="test")
    assert client.get.headers["Authorization"] == "Bearer test"
