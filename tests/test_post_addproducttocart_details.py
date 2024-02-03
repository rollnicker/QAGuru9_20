from time import sleep

import allure
import pytest
import requests
from allure_commons._allure import step
from selene import browser, have

from utils.logging import post_shop

BASE_URL = "https://demowebshop.tricentis.com"
CART_URL = "https://demowebshop.tricentis.com/cart"


@allure.title("Проверка добавления нескольких товаров в корзину через страницу детальной информации")
def test_add_to_cart_two_products_from_details():
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

    with step("check product quantity"):
        browser.element('.qty-input').should(have.value("2"))


...


@pytest.mark.xfail(reason="Не получается сделать добавление в корзину двух разных предметов")
def test_add_to_cart_from_details2():
    with step("add product to cart"):
        response = post_shop("/addproducttocart/catalog/43/1/1", allow_redirects=False)
        cookie = response.cookies.get("Nop.customer")

    with step("open shop"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("add product to cart"):
        response2 = requests.post(
            url="https://demowebshop.tricentis.com/addproducttocart/details/74/1",
            data={
                "product_attribute_74_5_26": 81,
                "product_attribute_74_6_27": 83,
                "product_attribute_74_3_28": 86,
                "addtocart_74.EnteredQuantity": 1
            },
            cookies={"name": "Nop.customer", "value": cookie}
        )
        cookie2 = response2.cookies.get("Nop.customer")

    with step("open shop"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie2})
        browser.open(CART_URL)

    sleep(5)
    with step("check product name"):
        browser.element('.product-name').should(have.text('Smartphone'))

    with step("check product name"):
        browser.element('.qty-input').should(have.text('Build your own expensive computer'))
