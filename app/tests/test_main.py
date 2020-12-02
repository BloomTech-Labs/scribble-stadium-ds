from fastapi.testclient import TestClient
from os import getenv
from app.main import app

client = TestClient(app)


def test_docs():
    """Return HTML docs for root route."""
    # set the authorization token so that the API accepts the connection
    client.headers["Authorization"] = getenv("DS_SECRET_TOKEN", None)
    # pull the content with from the root page (in this case swagger_ui)
    response = client.get("/")
    # check to make sure status_code is good and site is up
    assert response.status_code == 200
    # checks to make sure that the swagger_ui loads as html
    assert response.headers["content-type"].startswith("text/html")

    # change the headers to unauthorized
    client.headers["Authorization"] = None
    # pull the root page content again
    response = client.get("/")
    # should be working independent of auth header
    assert response.status_code == 200
