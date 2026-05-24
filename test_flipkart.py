from playwright.sync_api import Page
import time

def test_flipkart_login_and_search(page: Page):

    # ─── STEP 1: Open Flipkart ───
    page.goto("https://www.flipkart.com/")
    page.wait_for_load_state("networkidle")
    print("✓ Flipkart opened")

    # ─── STEP 2: Enter phone number ───
    page.locator("form").filter(
        has_text="Enter Email/Mobile numberBy"
    ).get_by_role("textbox").fill("YOUR_PHONE_NUMBER")

    page.locator("form").filter(
        has_text="Enter Email/Mobile numberBy"
    ).get_by_role("textbox").press("Enter")
    print("✓ Phone number entered — OTP sent!")

    # ─── STEP 3: PAUSE for OTP ───
    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  CHECK YOUR PHONE FOR OTP")
    print("  TYPE IT MANUALLY IN THE BROWSER")
    print("  YOU HAVE 60 SECONDS!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")

    # Wait until Flipkart home page loads after OTP
    page.wait_for_url("https://www.flipkart.com/", timeout=60000)
    page.wait_for_load_state("networkidle")
    print("✓ Logged in successfully!")

    # ─── STEP 4: Screenshot after login ───
    page.screenshot(path="flipkart_loggedin.png")
    print("✓ Screenshot saved — flipkart_loggedin.png")

    # ─── STEP 5: Search for a product ───
    page.get_by_role("textbox", name="Search for Products, Brands").click()
    page.get_by_role("textbox", name="Search for Products, Brands").fill("iPhone 15")
    page.get_by_role("textbox", name="Search for Products, Brands").press("Enter")
    page.wait_for_load_state("networkidle")
    print("✓ Searched for iPhone 15")

    # ─── STEP 6: Screenshot of search results ───
    page.screenshot(path="flipkart_search.png")
    print("✓ Screenshot saved — flipkart_search.png")

    # ─── STEP 7: Click first product ───
    page.locator("._75nlfW").first.click()
    page.wait_for_load_state("networkidle")
    print("✓ Opened first product")

    # ─── STEP 8: Get product details ───
    try:
        title = page.locator(".VU-ZEz").first.text_content()
        price = page.locator(".Nx9bqj").first.text_content()
        print(f"✓ Product  : {title}")
        print(f"✓ Price    : {price}")
    except:
        print("✓ Product page opened")

    # ─── STEP 9: Final screenshot ───
    page.screenshot(path="flipkart_product.png")
    print("✓ Screenshot saved — flipkart_product.png")