import requests

BASE_URL = "https://demowebshop.tricentis.com"


def test_open_shop_with_status():
    response = requests.get(
        url=BASE_URL
    )
    assert response.status_code == 200
