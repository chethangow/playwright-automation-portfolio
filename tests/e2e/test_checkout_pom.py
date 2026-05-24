import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

def test_full_journey_with_pom(page: Page):

    # ─── Use all 3 page classes together ───
    login     = LoginPage(page)
    inventory = InventoryPage(page)
    cart      = CartPage(page)

    # STEP 1: Login
    login.goto()
    login.login("standard_user", "secret_sauce")
    assert inventory.is_loaded()
    print(f"✓ Logged in — page title: {inventory.get_page_title()}")

    # STEP 2: Check products
    count = inventory.get_product_count()
    assert count == 6
    print(f"✓ Found {count} products")

    # STEP 3: Add items to cart
    inventory.add_to_cart("sauce labs backpack")
    inventory.add_to_cart("sauce labs bike light")
    assert inventory.get_cart_count() == 2
    print(f"✓ Cart has {inventory.get_cart_count()} items")

    # STEP 4: Open cart
    inventory.open_cart()
    assert cart.is_open()
    assert cart.get_item_count() == 2
    print(f"✓ Cart open — {cart.get_item_count()} items inside")

    # STEP 5: Checkout
    cart.start_checkout()
    cart.fill_checkout_details("Test", "User", "560001")
    print("✓ Checkout details filled")

    # STEP 6: Finish order
    cart.finish_order()
    assert cart.is_order_complete()
    print(f"✓ Order complete: {cart.get_success_message()}")

    page.screenshot(path="screenshots/pom_full_journey.png")