from playwright.sync_api import Page

def test_full_shopping_journey(page: Page):

    # ─── STEP 1: Open the website ───
    page.goto("https://www.saucedemo.com")
    assert "Swag Labs" in page.title()
    print("✓ Website opened")

    # ─── STEP 2: Login ───
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.wait_for_load_state("networkidle")
    assert "inventory" in page.url
    print("✓ Logged in successfully")

    # ─── STEP 3: Add item to cart ───
    page.locator("#add-to-cart-sauce-labs-backpack").click()
    cart_count = page.locator(".shopping_cart_badge").text_content()
    assert cart_count == "1"
    print(f"✓ Item added to cart — badge shows: {cart_count}")

    # ─── STEP 4: Open cart ───
    page.locator(".shopping_cart_link").click()
    page.wait_for_load_state("networkidle")
    assert "cart" in page.url
    print("✓ Cart opened")

    # ─── STEP 5: Checkout ───
    page.locator("#checkout").click()
    page.locator("#first-name").fill("Test")
    page.locator("#last-name").fill("User")
    page.locator("#postal-code").fill("560001")
    page.locator("#continue").click()
    print("✓ Checkout details filled")

    # ─── STEP 6: Finish order ───
    page.locator("#finish").click()
    page.wait_for_load_state("networkidle")

    # ─── STEP 7: Verify order complete ───
    success = page.locator(".complete-header").text_content()
    assert "Thank you for your order" in success
    print(f"✓ Order placed! Message: {success}")

    # ─── STEP 8: Screenshot as proof ───
    page.screenshot(path="order_complete.png")
    print("✓ Screenshot saved as order_complete.png")