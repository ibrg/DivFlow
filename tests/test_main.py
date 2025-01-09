import httpx

URL = "http://127.0.0.1:8000"


def test_main_():
    with httpx.Client() as client:
        response = client.get(URL)
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}


def test_status():
    with httpx.Client() as client:
        response = client.get(URL + "/status")
        assert response.status_code == 200
        assert "status" in response.json()