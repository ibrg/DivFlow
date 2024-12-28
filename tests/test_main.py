import requests
from pytest import fixture


@fixture
def url():
    return "http://127.0.0.1:8000/"


def test_main(url):
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_status(url, uri="/status"):
    response = requests.get(url + uri)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
