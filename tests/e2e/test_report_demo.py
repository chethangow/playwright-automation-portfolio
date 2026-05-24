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


# ─── TEST 1: Smoke test ───
def test_website_is_up(page: Page):
    """Verify saucedemo website loads correctly"""
    page.goto("https://www.saucedemo.com")
    page.wait_for_load_state("networkidle")
    assert "Swag Labs" in page.title()
    print("✓ Website is up and running")


# ─── TEST 2: Valid login ───
def test_valid_login(page: Page):
    """Verify standard user can login"""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    assert "inventory" in page.url
    print("✓ Valid login works")


# ─── TEST 3: Invalid login ───
def test_invalid_login(page: Page):
    """Verify wrong credentials show error"""
    login = LoginPage(page)
    login.goto()
    login.login("wrong_user", "wrong_pass")
    assert login.is_error_visible()
    print("✓ Invalid login blocked")


# ─── TEST 4: Products count ───
def test_products_count(page: Page):
    """Verify exactly 6 products on inventory page"""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inventory = InventoryPage(page)
    assert inventory.get_product_count() == 6
    print("✓ Products count is correct")


# ─── TEST 5: Add to cart ───
def test_add_to_cart(page: Page):
    """Verify item can be added to cart"""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inventory = InventoryPage(page)
    inventory.add_to_cart("sauce labs backpack")
    assert inventory.get_cart_count() == 1
    print("✓ Add to cart works")


# ─── TEST 6: Full checkout ───
def test_full_checkout(page: Page):
    """Verify complete purchase journey"""
    login     = LoginPage(page)
    inventory = InventoryPage(page)
    cart      = CartPage(page)

    login.goto()
    login.login("standard_user", "secret_sauce")
    inventory.add_to_cart("sauce labs backpack")
    inventory.open_cart()
    cart.start_checkout()
    cart.fill_checkout_details("Test", "User", "560001")
    cart.finish_order()
    assert cart.is_order_complete()
    print("✓ Full checkout works")


# ─── TEST 7: Intentional failure for report demo ───
def test_intentional_failure(page: Page):
    """This test fails on purpose to show report"""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inventory = InventoryPage(page)

    # Wrong assertion on purpose
    assert inventory.get_product_count() == 99, \
        f"Expected 99 products but found {inventory.get_product_count()}"