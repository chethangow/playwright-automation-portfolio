import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
))

import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# ─── TEST 1: Multiple users login ───
# Same test runs 4 times with different users
@pytest.mark.parametrize("username, password, expected", [
    ("standard_user",  "secret_sauce", "inventory"),
    ("locked_out_user","secret_sauce", "locked"),
    ("problem_user",   "secret_sauce", "inventory"),
    ("standard_user",  "wrong_pass",   "error"),
])
def test_login_multiple_users(page: Page, username, password, expected):

    login = LoginPage(page)
    login.goto()
    login.login(username, password)

    if expected == "inventory":
        assert "inventory" in page.url
        print(f"✓ {username} → logged in successfully")

    elif expected == "locked":
        assert login.is_error_visible()
        print(f"✓ {username} → correctly blocked")

    elif expected == "error":
        assert login.is_error_visible()
        error = login.get_error_message()
        print(f"✓ {username} → error shown: {error}")

    page.screenshot(
        path=f"screenshots/login_{username}_{expected}.png"
    )


# ─── TEST 2: Multiple products add to cart ───
@pytest.mark.parametrize("product", [
    "sauce labs backpack",
    "sauce labs bike light",
    "sauce labs bolt t-shirt",
    "sauce labs fleece jacket",
])
def test_add_different_products(page: Page, product):

    # Login first
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    # Add specific product
    inventory = InventoryPage(page)
    inventory.add_to_cart(product)

    # Verify cart count
    assert inventory.get_cart_count() == 1
    print(f"✓ Added to cart: {product}")
    print(f"✓ Cart count: {inventory.get_cart_count()}")


# ─── TEST 3: Search with multiple terms via API ───
from playwright.sync_api import APIRequestContext, Playwright

@pytest.fixture
def api(playwright: Playwright):
    context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )
    yield context
    context.dispose()


@pytest.mark.parametrize("user_id, expected_posts", [
    (1, 10),
    (2, 10),
    (3, 10),
    (4, 10),
    (5, 10),
])
def test_user_post_count(api: APIRequestContext, user_id, expected_posts):

    response = api.get(f"/posts?userId={user_id}")

    assert response.status == 200
    posts = response.json()
    assert len(posts) == expected_posts
    print(f"✓ User {user_id} has {len(posts)} posts")


# ─── TEST 4: Multiple checkout details ───
@pytest.mark.parametrize("first, last, postal, valid", [
    ("John",  "Doe",   "560001", True),
    ("Jane",  "Smith", "110001", True),
    ("",      "Doe",   "560001", False),
    ("John",  "",      "560001", False),
    ("John",  "Doe",   "",       False),
])
def test_checkout_form_validation(page: Page, first, last, postal, valid):

    # Login
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    # Add item
    inventory = InventoryPage(page)
    inventory.add_to_cart("sauce labs backpack")
    inventory.open_cart()

    # Go to checkout
    page.locator("#checkout").click()
    page.wait_for_load_state("networkidle")

    # Fill form
    if first:
        page.locator("#first-name").fill(first)
    if last:
        page.locator("#last-name").fill(last)
    if postal:
        page.locator("#postal-code").fill(postal)

    page.locator("#continue").click()
    page.wait_for_timeout(500)

    if valid:
        assert "step-two" in page.url or "checkout" in page.url
        print(f"✓ Valid details accepted: {first} {last} {postal}")
    else:
        error = page.locator("[data-test='error']")
        assert error.is_visible()
        print(f"✓ Invalid details rejected: '{first}' '{last}' '{postal}'")

    page.screenshot(
        path=f"screenshots/checkout_{first}_{last}_{postal}.png"
    )