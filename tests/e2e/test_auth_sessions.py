import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
))

import pytest
import json
from playwright.sync_api import Page, Browser, Playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# Path where session will be saved
SESSION_FILE = "data/session.json"


# ─── TEST 1: Save session to file ───
def test_save_session(browser: Browser):

    # Create a fresh browser context
    context = browser.new_context()
    page = context.new_page()

    # Login normally
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    # Wait for login to complete
    page.wait_for_url("**/inventory.html")
    print("✓ Logged in successfully")

    # Save ALL cookies + storage to file
    os.makedirs("data", exist_ok=True)
    context.storage_state(path=SESSION_FILE)
    print(f"✓ Session saved to {SESSION_FILE}")

    # Verify file was created
    assert os.path.exists(SESSION_FILE)

    # Read and show what was saved
    with open(SESSION_FILE) as f:
        session_data = json.load(f)
    print(f"✓ Cookies saved: {len(session_data['cookies'])}")

    context.close()


# ─── TEST 2: Reuse saved session ───
def test_reuse_session(browser: Browser):

    # Skip if session file doesn't exist
    if not os.path.exists(SESSION_FILE):
        pytest.skip("Run test_save_session first!")

    # Load context WITH saved session
    # No login needed!
    context = browser.new_context(
        storage_state=SESSION_FILE
    )
    page = context.new_page()

    # Go directly to inventory — already logged in!
    page.goto("https://www.saucedemo.com/inventory.html")
    page.wait_for_load_state("networkidle")

    # Verify we're logged in
    assert "inventory" in page.url
    inventory = InventoryPage(page)
    assert inventory.get_product_count() == 6
    print("✓ Already logged in via saved session!")
    print(f"✓ Products visible: {inventory.get_product_count()}")

    page.screenshot(path="screenshots/session_reused.png")
    context.close()


# ─── TEST 3: Multiple tests using session ───
# Fixture that loads session for any test
@pytest.fixture
def session_page(browser: Browser):

    if not os.path.exists(SESSION_FILE):
        # Create session if it doesn't exist
        context = browser.new_context()
        page = context.new_page()
        login = LoginPage(page)
        login.goto()
        login.login("standard_user", "secret_sauce")
        page.wait_for_url("**/inventory.html")
        context.storage_state(path=SESSION_FILE)
        context.close()

    # Return page with session loaded
    context = browser.new_context(
        storage_state=SESSION_FILE
    )
    page = context.new_page()
    yield page
    context.close()


def test_browse_products_with_session(session_page):
    # No login needed — session_page fixture handles it!
    session_page.goto("https://www.saucedemo.com/inventory.html")
    session_page.wait_for_load_state("networkidle")

    inventory = InventoryPage(session_page)
    count = inventory.get_product_count()
    assert count == 6
    print(f"✓ Session test: Found {count} products instantly!")
    session_page.screenshot(path="screenshots/session_test1.png")


def test_add_to_cart_with_session(session_page):
    session_page.goto("https://www.saucedemo.com/inventory.html")
    session_page.wait_for_load_state("networkidle")

    inventory = InventoryPage(session_page)
    inventory.add_to_cart("sauce labs backpack")
    assert inventory.get_cart_count() == 1
    print(f"✓ Session test: Added to cart instantly!")
    session_page.screenshot(path="screenshots/session_test2.png")


def test_check_cart_with_session(session_page):
    session_page.goto("https://www.saucedemo.com/inventory.html")
    session_page.wait_for_load_state("networkidle")

    inventory = InventoryPage(session_page)
    inventory.add_to_cart("sauce labs bike light")
    inventory.open_cart()

    from pages.cart_page import CartPage
    cart = CartPage(session_page)
    assert cart.is_open()
    print(f"✓ Session test: Cart opened instantly!")
    session_page.screenshot(path="screenshots/session_test3.png")


# ─── TEST 4: Verify session expires correctly ───
def test_invalid_session(browser: Browser):

    # Create fake/empty session
    fake_session = {
        "cookies": [],
        "origins": []
    }

    fake_session_file = "data/fake_session.json"
    with open(fake_session_file, "w") as f:
        json.dump(fake_session, f)

    # Try to use fake session
    context = browser.new_context(
        storage_state=fake_session_file
    )
    page = context.new_page()

    # Go to inventory — should redirect to login
    page.goto("https://www.saucedemo.com/inventory.html")
    page.wait_for_load_state("networkidle")

    # Should be redirected back to login page
    assert page.url == "https://www.saucedemo.com/"
    print("✓ Invalid session correctly redirected to login!")

    page.screenshot(path="screenshots/invalid_session.png")
    context.close()