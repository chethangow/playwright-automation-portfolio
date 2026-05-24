from playwright.sync_api import Page

def test_without_waits(page: Page):
    
    page.goto("https://www.saucedemo.com")
    
    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Immediately try to find products
    # NO WAIT — test runs faster than page loads!
    products = page.locator(".inventory_item")
    print(f"Found: {products.count()} products")
    
    # Add to cart immediately
    page.locator("#add-to-cart-sauce-labs-backpack").click()
    
    # Immediately go to cart
    page.locator(".shopping_cart_link").click()
    
    # Immediately click checkout
    page.locator("#checkout").click()
    
    print("✓ Done without waits")

def test_with_smart_waits(page: Page):

    # ─── WAIT TYPE 1: wait_for_load_state ───
    # Waits for entire page to finish loading
    page.goto("https://www.saucedemo.com")
    page.wait_for_load_state("networkidle")
    print("✓ Type 1: Page fully loaded")

    # Login
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    # ─── WAIT TYPE 2: wait_for_url ───
    # Waits until URL changes to inventory page
    page.wait_for_url("**/inventory.html", timeout=10000)
    print(f"✓ Type 2: URL changed to → {page.url}")

    # ─── WAIT TYPE 3: wait_for_selector ───
    # Waits until products actually appear on screen
    page.wait_for_selector(".inventory_item", timeout=10000)
    products = page.locator(".inventory_item")
    print(f"✓ Type 3: Found {products.count()} products on page")

    # Add item to cart
    page.locator("#add-to-cart-sauce-labs-backpack").click()

    # Wait for cart badge to appear
    page.wait_for_selector(".shopping_cart_badge", timeout=5000)
    cart_count = page.locator(".shopping_cart_badge").text_content()
    print(f"✓ Type 3: Cart badge appeared → shows {cart_count} item")

    # Go to cart
    page.locator(".shopping_cart_link").click()
    page.wait_for_url("**/cart.html", timeout=5000)
    print("✓ Type 2: Cart page loaded")

    # Checkout
    page.locator("#checkout").click()
    page.wait_for_selector("#first-name", timeout=5000)
    print("✓ Type 3: Checkout form appeared")

    # Fill checkout form
    page.locator("#first-name").fill("Test")
    page.locator("#last-name").fill("User")
    page.locator("#postal-code").fill("560001")
    page.locator("#continue").click()

    # ─── WAIT TYPE 4: wait_for_timeout ───
    # Using sparingly — just to see the summary page clearly
    page.wait_for_timeout(1000)
    print("✓ Type 4: Waited 1 second to view summary")

    # Finish order
    page.locator("#finish").click()
    page.wait_for_selector(".complete-header", timeout=10000)
    
    # Final check
    message = page.locator(".complete-header").text_content()
    assert "Thank you" in message
    print(f"✓ Order complete: {message}")

    page.screenshot(path="smart_waits_proof.png")
    print("✓ All 4 wait types used successfully!")