from fastapi.testclient import TestClient
from os import getenv
from app.main import app

client = TestClient(app)
# set the authorization token so that the API accepts the connection
client.headers["Authorization"] = getenv("DS_SECRET_TOKEN", None)


def test_valid_input():
    """Return 200 Success for valid 2 character US state postal code."""
    response = client.get("/viz/IL")
    assert response.status_code == 200
    assert "Illinois Unemployment Rate" in response.text


def test_invalid_input():
    """Return 404 if the endpoint isn't valid US state postal code."""
    response = client.get("/viz/ZZ")
    body = response.json()
    assert response.status_code == 404
    assert body["detail"] == "State code ZZ not found"
