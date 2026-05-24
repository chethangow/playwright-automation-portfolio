from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


# ─── TEST 1: Uses login_page fixture ───
# No need to goto() — fixture already did it!
def test_login_page_loaded(login_page):
    assert login_page.is_error_visible() == False
    print("✓ Login page loaded via fixture")


# ─── TEST 2: Uses login_page fixture ───
def test_valid_login_with_fixture(login_page):
    login_page.login("standard_user", "secret_sauce")
    print("✓ Logged in using fixture")


# ─── TEST 3: Uses logged_in fixture ───
# No need to login — fixture already did it!
def test_products_visible(logged_in):
    inventory = InventoryPage(logged_in)
    assert inventory.get_product_count() == 6
    print(f"✓ Products loaded: {inventory.get_product_count()}")


# ─── TEST 4: Uses inventory_page fixture ───
# Already logged in AND on products page!
def test_add_single_item(inventory_page):
    inventory_page.add_to_cart("sauce labs backpack")
    assert inventory_page.get_cart_count() == 1
    print(f"✓ Cart count: {inventory_page.get_cart_count()}")


# ─── TEST 5: Uses inventory_page fixture ───
def test_add_multiple_items(inventory_page):
    inventory_page.add_to_cart("sauce labs backpack")
    inventory_page.add_to_cart("sauce labs bike light")
    inventory_page.add_to_cart("sauce labs bolt t-shirt")
    assert inventory_page.get_cart_count() == 3
    print(f"✓ Cart count: {inventory_page.get_cart_count()}")


# ─── TEST 6: Uses cart_with_items fixture ───
# Already logged in, items added, cart open!
def test_checkout_with_fixture(cart_with_items):
    assert cart_with_items.is_open()
    assert cart_with_items.get_item_count() == 2
    cart_with_items.start_checkout()
    cart_with_items.fill_checkout_details("Test", "User", "560001")
    cart_with_items.finish_order()
    assert cart_with_items.is_order_complete()
    print(f"✓ Order complete: {cart_with_items.get_success_message()}")


# ─── TEST 7: Multiple fixtures in one test ───
def test_full_journey_fixtures(login_page, page):
    login_page.login("standard_user", "secret_sauce")
    inventory = InventoryPage(page)
    assert inventory.is_loaded()
    assert inventory.get_product_count() == 6
    inventory.add_to_cart("sauce labs backpack")
    assert inventory.get_cart_count() == 1
    inventory.open_cart()
    cart = CartPage(page)
    assert cart.is_open()
    cart.start_checkout()
    cart.fill_checkout_details("QA", "Engineer", "560001")
    cart.finish_order()
    assert cart.is_order_complete()
    print("✓ Full journey using fixtures complete!")
    