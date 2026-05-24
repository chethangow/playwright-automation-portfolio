from playwright.sync_api import Page

def test_all_assertions(page: Page):

    page.goto("https://www.saucedemo.com")

    # ─── 1. Check page TITLE ───
    assert "Swag Labs" in page.title()
    print("✓ Title is correct")

    # ─── 2. Check URL ───
    assert page.url == "https://www.saucedemo.com/"
    print("✓ URL is correct")

    # ─── 3. Check element IS VISIBLE ───
    assert page.locator("#login-button").is_visible()
    print("✓ Login button is visible")

    # ─── 4. Check element TEXT ───
    button_text = page.locator("#login-button").get_attribute("value")
    assert button_text == "Login"
    print("✓ Button text is correct")

    # ─── 5. Check input is ENABLED ───
    assert page.locator("#user-name").is_enabled()
    print("✓ Username input is enabled")

    # ─── 6. Login and check URL changes ───
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.wait_for_load_state("networkidle")

    # ─── 7. Check URL changed after login ───
    assert "inventory" in page.url
    print("✓ Redirected to inventory page")

    # ─── 8. Check element COUNT ───
    products = page.locator(".inventory_item")
    assert products.count() == 6
    print(f"✓ Found {products.count()} products on page")

    # ─── 9. Check text IS present on page ───
    assert page.locator(".title").text_content() == "Products"
    print("✓ Page heading says Products")

    # ─── 10. Screenshot as proof ───
    page.screenshot(path="assertions_proof.png")
    print("✓ All 9 assertions passed!")