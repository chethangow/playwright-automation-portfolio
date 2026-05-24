import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


# ─── FIXTURE 1: Fresh login page ───
@pytest.fixture
def login_page(page):
    login = LoginPage(page)
    login.goto()
    return login


# ─── FIXTURE 2: Already logged in ───
@pytest.fixture
def logged_in(page):
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    return page


# ─── FIXTURE 3: Inventory page ready ───
@pytest.fixture
def inventory_page(logged_in):
    return InventoryPage(logged_in)


# ─── FIXTURE 4: Cart with items ───
@pytest.fixture
def cart_with_items(logged_in):
    inventory = InventoryPage(logged_in)
    inventory.add_to_cart("sauce labs backpack")
    inventory.add_to_cart("sauce labs bike light")
    inventory.open_cart()
    return CartPage(logged_in)

# ─── ATTACH SCREENSHOT TO HTML REPORT ───
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("[chromium]", "")
            screenshot_path = f"reports/FAILED_{test_name}_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)

            # Attach screenshot to HTML report
            if hasattr(report, "extras"):
                from pytest_html import extras
                report.extras = report.extras or []
                report.extras.append(
                    extras.image(screenshot_path)
                )
            print(f"\n📸 Screenshot → {screenshot_path}")