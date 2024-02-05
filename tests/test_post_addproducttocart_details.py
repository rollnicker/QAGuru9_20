from time import sleep

import allure
import pytest
import requests
from allure_commons._allure import step
from selene import browser, have

from utils.logging import post_shop

BASE_URL = "https://demowebshop.tricentis.com"
CART_URL = "https://demowebshop.tricentis.com/cart"
UNSUCCESFULL_MESSAGE = ['Enter valid recipient name',
                        'Enter valid recipient email',
                        'Enter valid sender name',
                        'Enter valid sender email']
SUCCESFULL_MESSAGE = 'The product has been added to your <a href="/cart">shopping cart</a>'


@allure.title("Проверка добавления нескольких товаров в корзину через страницу детальной информации")
def test_add_to_cart_two_products_from_details():
    with step("add product to cart"):
        ADD_PRODUCT = "/addproducttocart/details/"
        with step("add product to cart"):
            response = post_shop(
                ADD_PRODUCT + "74/1",
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


@allure.title("Проверка добавления подарочной карты без данных")
def test_unsuccesfull_add_gift_card_to_cart():
    with step("add gift_card to cart"):
        response = requests.post(
            url="https://demowebshop.tricentis.com/addproducttocart/details/2/1",
            data={
                "giftcard_2.RecipientName": "",
                "giftcard_2.RecipientEmail": "",
                "giftcard_2.SenderName": "",
                "giftcard_2.SenderEmail": "",
                "giftcard_2.Message": "",
                "addtocart_74.EnteredQuantity": 1
            }
        )
        add_status = response.json()['success']
        message = response.json()['message']
        assert message == UNSUCCESFULL_MESSAGE
        assert add_status == False


@allure.title("Проверка успешного добавления подарочной карты")
def test_add_gift_card_to_cart():
    with step("add gift_card to cart"):
        response = requests.post(
            url="https://demowebshop.tricentis.com/addproducttocart/details/2/1",
            data={
                "giftcard_2.RecipientName": "Lol",
                "giftcard_2.RecipientEmail": "lol@mail.ru",
                "giftcard_2.SenderName": "Kek",
                "giftcard_2.SenderEmail": "kek@mail.ru",
                "giftcard_2.Message": "Verni moi chebureki",
                "addtocart_74.EnteredQuantity": 1
            }
        )
        add_status = response.json()['success']
        message = response.json()['message']
        print(message)
        assert message == SUCCESFULL_MESSAGE
        assert add_status == True


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
        browser.all('.product-name').first.should(have.text('Smartphone'))

    with step("check product name"):
        browser.all('.product-name').second.should(have.text('Build your own expensive computer'))


def test_add_to_cart_from_details3():
    with step("add product to cart"):
        response = post_shop("/addproducttocart/catalog/43/1/1", allow_redirects=False)
        cookie = response.cookies.get("Nop.customer")

    with step("open shop"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("add product to cart"):
        response2 = requests.post(
            url="https://demowebshop.tricentis.com/addproducttocart/details/74/1&quot",
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
        browser.all('.product-name').first.should(have.text('Smartphone'))

    with step("check product name"):
        browser.all('.product-name').second.should(have.text('Build your own expensive computer'))
