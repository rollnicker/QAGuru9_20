from time import sleep

import allure
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


def test_add_to_cart_succes_status():
    with step("add product to cart"):
        response = post_shop("/addproducttocart/catalog/43/1/1", allow_redirects=False)
        add_status = response.json()['success']
        assert add_status == True


@allure.title("Проверка добавления 14.1-inch Laptop в корзину")
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


@allure.title("Проверка добавления Smartphone в корзину")
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


@allure.title("Проверка добавления нескольких товаров в корзину через страницу детальной информации")
def test_add_to_cart_from_details():
    with step("add product to cart"):
        response = requests.post(
            url="https://demowebshop.tricentis.com/addproducttocart/details/74/1",
            data={
                "product_attribute_74_5_26": 81,
                "product_attribute_74_6_27": 83,
                "product_attribute_74_3_28": 86,
                "addtocart_74.EnteredQuantity": 2
            }
        )
        cookie = response.cookies.get("Nop.customer")

    with step("open shop"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("check product name"):
        browser.element('.qty-input').should(have.value("2"))


...


def test_add_to_cart_from_details():
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

    with step("add product to cart"):
        response = requests.post(
            url="https://demowebshop.tricentis.com/addproducttocart/details/74/1",
            data={
                "product_attribute_74_5_26": 81,
                "product_attribute_74_6_27": 83,
                "product_attribute_74_3_28": 86,
                "addtocart_74.EnteredQuantity": 1
            }
        )
        cookie = response.cookies.get("Nop.customer")

    with step("open shop"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    sleep(5)
    with step("check product name"):
        browser.element('.product-name').should(have.text('Smartphone'))

    with step("check product name"):
        browser.element('.qty-input').should(have.text('Build your own expensive computer'))
