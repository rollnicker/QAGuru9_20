import requests
from allure_commons._allure import step
from jsonschema import validate
from selene import browser, have

from utils.logging import post_shop
from utils.open_schemas import load_schema

BASE_URL = "https://demowebshop.tricentis.com"
CART_URL = "https://demowebshop.tricentis.com/cart"



def test_open_shop_with_status():
    response = requests.get(
        url=BASE_URL
    )
    assert response.status_code == 200


def test_add_to_cart_laptop():
    with step("add product to cart"):
        response = post_shop("/addproducttocart/catalog/31/1/1", allow_redirects=False)
        body = response.json()
        validate(body, schema=load_schema("add_to_cart_schema.json"))
        assert response.status_code == 200
        cookie = response.cookies.get("Nop.customer")

    with step("open shop"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("check product name"):
        browser.element('.product-name').should(have.text('14.1-inch Laptop'))


def test_add_to_cart_smartphone():
    with step("add product to cart"):
        response = post_shop("/addproducttocart/catalog/43/1/1", allow_redirects=False)
        body = response.json()
        validate(body, schema=load_schema("add_to_cart_schema.json"))
        assert response.status_code == 200
        cookie = response.cookies.get("Nop.customer")

    with step("open shop"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("check product name"):
        browser.element('.product-name').should(have.text('Smartphone'))
