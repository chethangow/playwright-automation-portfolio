import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
))

import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


# ─── TEST 1: Login works on all browsers ───
def test_login_all_browsers(page: Page, browser_name: str):

    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    assert "inventory" in page.url
    print(f"✓ Login works on {browser_name}!")
    page.screenshot(
        path=f"screenshots/login_{browser_name}.png"
    )


# ─── TEST 2: Products visible on all browsers ───
def test_products_all_browsers(page: Page, browser_name: str):

    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    count = inventory.get_product_count()
    assert count == 6
    print(f"✓ {browser_name}: Found {count} products")
    page.screenshot(
        path=f"screenshots/products_{browser_name}.png"
    )


# ─── TEST 3: Full journey on all browsers ───
def test_full_journey_all_browsers(page: Page, browser_name: str):

    login     = LoginPage(page)
    inventory = InventoryPage(page)
    cart      = CartPage(page)

    # Login
    login.goto()
    login.login("standard_user", "secret_sauce")
    assert inventory.is_loaded()
    print(f"✓ {browser_name}: Logged in")

    # Add to cart
    inventory.add_to_cart("sauce labs backpack")
    assert inventory.get_cart_count() == 1
    print(f"✓ {browser_name}: Item added to cart")

    # Checkout
    inventory.open_cart()
    cart.start_checkout()
    cart.fill_checkout_details("Test", "User", "560001")
    cart.finish_order()
    assert cart.is_order_complete()
    print(f"✓ {browser_name}: Order complete!")

    page.screenshot(
        path=f"screenshots/journey_{browser_name}.png"
    )


# ─── TEST 4: API works on all browsers ───
def test_api_all_browsers(page: Page, browser_name: str):

    page.goto("https://jsonplaceholder.typicode.com")
    page.wait_for_load_state("networkidle")

    assert "JSONPlaceholder" in page.title()
    print(f"✓ {browser_name}: API site loaded")
    page.screenshot(
        path=f"screenshots/api_{browser_name}.png"
    )