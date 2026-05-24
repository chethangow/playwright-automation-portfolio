import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

from playwright.sync_api import Page
from pages.login_page import LoginPage

# ─── TEST 1: Valid Login ───
def test_valid_login(page: Page):
    login = LoginPage(page)

    login.goto()
    login.login("standard_user", "secret_sauce")

    assert "inventory" in page.url
    print("✓ Valid login successful")
    page.screenshot(path="screenshots/pom_valid_login.png")


# ─── TEST 2: Invalid Login ───
def test_invalid_login(page: Page):
    login = LoginPage(page)

    login.goto()
    login.login("wrong_user", "wrong_password")

    assert login.is_error_visible()
    error = login.get_error_message()
    print(f"✓ Error shown correctly: {error}")
    page.screenshot(path="screenshots/pom_invalid_login.png")


# ─── TEST 3: Empty Login ───
def test_empty_login(page: Page):
    login = LoginPage(page)

    login.goto()
    login.login("", "")

    assert login.is_error_visible()
    print("✓ Empty login blocked correctly")
    page.screenshot(path="screenshots/pom_empty_login.png")