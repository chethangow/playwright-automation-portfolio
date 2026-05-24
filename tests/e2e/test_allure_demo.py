import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
))

import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@allure.epic("SauceDemo Testing")
@allure.feature("Smoke Tests")
@allure.severity(allure.severity_level.BLOCKER)
def test_website_is_up(page: Page):
    with allure.step("Open SauceDemo website"):
        page.goto("https://www.saucedemo.com")
        page.wait_for_load_state("networkidle")
    with allure.step("Verify title"):
        assert "Swag Labs" in page.title()
    allure.attach(page.screenshot(), name="homepage", attachment_type=allure.attachment_type.PNG)
    print("? Website is up")


@allure.epic("SauceDemo Testing")
@allure.feature("Authentication")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_login(page: Page):
    with allure.step("Navigate to login page"):
        login = LoginPage(page)
        login.goto()
    with allure.step("Enter valid credentials"):
        login.login("standard_user", "secret_sauce")
    with allure.step("Verify redirected to inventory"):
        assert "inventory" in page.url
    allure.attach(page.screenshot(), name="after_login", attachment_type=allure.attachment_type.PNG)
    print("? Valid login works")


@allure.epic("SauceDemo Testing")
@allure.feature("Authentication")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_login(page: Page):
    with allure.step("Navigate to login page"):
        login = LoginPage(page)
        login.goto()
    with allure.step("Enter invalid credentials"):
        login.login("wrong_user", "wrong_pass")
    with allure.step("Verify error message"):
        assert login.is_error_visible()
    allure.attach(page.screenshot(), name="error_message", attachment_type=allure.attachment_type.PNG)
    print("? Invalid login blocked")


@allure.epic("SauceDemo Testing")
@allure.feature("Shopping")
@allure.severity(allure.severity_level.CRITICAL)
def test_full_shopping_journey(page: Page):
    login     = LoginPage(page)
    inventory = InventoryPage(page)
    cart      = CartPage(page)
    with allure.step("Login"):
        login.goto()
        login.login("standard_user", "secret_sauce")
    with allure.step("Add items to cart"):
        inventory.add_to_cart("sauce labs backpack")
        inventory.add_to_cart("sauce labs bike light")
        assert inventory.get_cart_count() == 2
    allure.attach(page.screenshot(), name="items_in_cart", attachment_type=allure.attachment_type.PNG)
    with allure.step("Checkout"):
        inventory.open_cart()
        cart.start_checkout()
        cart.fill_checkout_details("Test", "User", "560001")
    with allure.step("Complete order"):
        cart.finish_order()
        assert cart.is_order_complete()
    allure.attach(page.screenshot(), name="order_complete", attachment_type=allure.attachment_type.PNG)
    print("? Order complete")


@allure.epic("SauceDemo Testing")
@allure.feature("Products")
@allure.severity(allure.severity_level.MINOR)
def test_intentional_failure(page: Page):
    with allure.step("Login"):
        login = LoginPage(page)
        login.goto()
        login.login("standard_user", "secret_sauce")
    with allure.step("Verify wrong product count"):
        inventory = InventoryPage(page)
        allure.attach(page.screenshot(), name="products_page", attachment_type=allure.attachment_type.PNG)
        assert inventory.get_product_count() == 99, f"Expected 99 but found {inventory.get_product_count()}"
