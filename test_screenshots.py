from playwright.sync_api import Page

def test_manual_screenshot(page: Page):

    # ─── MANUAL SCREENSHOTS at key moments ───
    page.goto("https://www.saucedemo.com")
    page.wait_for_load_state("networkidle")

    # Screenshot 1 — Login page
    page.screenshot(path="screenshots/01_login_page.png")
    print("✓ Screenshot 1: Login page captured")

    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")

    # Screenshot 2 — Filled form before clicking
    page.screenshot(path="screenshots/02_filled_form.png")
    print("✓ Screenshot 2: Filled form captured")

    page.locator("#login-button").click()
    page.wait_for_load_state("networkidle")

    # Screenshot 3 — After login
    page.screenshot(path="screenshots/03_after_login.png")
    print("✓ Screenshot 3: Products page captured")

    # Add to cart
    page.locator("#add-to-cart-sauce-labs-backpack").click()

    # Screenshot 4 — Cart badge visible
    page.screenshot(path="screenshots/04_item_added.png")
    print("✓ Screenshot 4: Item added to cart")

    # Full page screenshot
    page.screenshot(
        path="screenshots/05_full_page.png",
        full_page=True        # captures ENTIRE page including scroll
    )
    print("✓ Screenshot 5: Full page captured")

    print("✓ All manual screenshots saved in /screenshots folder!")


def test_automatic_screenshot_on_failure(page: Page):

    page.goto("https://www.saucedemo.com")
    page.wait_for_load_state("networkidle")

    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.wait_for_load_state("networkidle")

    # This assertion will FAIL on purpose
    # to show automatic screenshot on failure!
    products = page.locator(".inventory_item")
    print(f"Found {products.count()} products")

    # Intentional wrong assertion — will fail!
    assert products.count() == 99, "Expected 99 products but found 6!"


def test_video_recording(page: Page):

    # Video records automatically — no extra code needed!
    # Just run your test normally
    page.goto("https://www.saucedemo.com")
    page.wait_for_load_state("networkidle")
    print("✓ Video recording started automatically")

    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.wait_for_load_state("networkidle")

    # Browse products
    products = page.locator(".inventory_item")
    print(f"✓ Found {products.count()} products")

    page.locator("#add-to-cart-sauce-labs-backpack").click()
    page.wait_for_selector(".shopping_cart_badge")
    print("✓ Added item to cart")

    page.locator(".shopping_cart_link").click()
    page.wait_for_load_state("networkidle")
    print("✓ Opened cart")

    page.screenshot(path="screenshots/video_test_end.png")
    print("✓ Video saved automatically in /videos folder!")