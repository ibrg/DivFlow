import requests

def test_main_page():
    response = requests.get('http://0.0.0.0:5000')
    assert response.status_code == 200
