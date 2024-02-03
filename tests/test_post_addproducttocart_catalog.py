import allure
from allure_commons._allure import step
from jsonschema import validate
from selene import browser, have

from utils.logging import post_shop
from utils.open_schemas import load_schema

BASE_URL = "https://demowebshop.tricentis.com"
CART_URL = "https://demowebshop.tricentis.com/cart"
ADD_PRODUCT = "/addproducttocart/catalog/"


@allure.title("Проверка статуса добавления в корзину")
def test_add_to_cart_succes_status():
    with step("add product to cart"):
        response = post_shop(ADD_PRODUCT + "43/1/1", allow_redirects=False)
        add_status = response.json()['success']
        assert add_status == True


@allure.title("Проверка добавления 14.1-inch Laptop в корзину")
def test_add_to_cart_laptop():
    with step("add product to cart"):
        response = post_shop(ADD_PRODUCT + "31/1/1",
                             allow_redirects=False)
        body = response.json()
        validate(body,
                 schema=load_schema("add_to_cart_schema.json"))
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
        response = post_shop(ADD_PRODUCT + "43/1/1",
                             allow_redirects=False)
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
