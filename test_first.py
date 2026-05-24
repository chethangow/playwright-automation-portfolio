from playwright.sync_api import sync_playwright, expect as pw_expect

def test_google_opens(page):
    # Open Google in the browser
    page.goto("https://www.google.com")

    # Check the title contains "Google"
    assert "Google" in page.title()

    # Take a screenshot as proof
    page.screenshot(path="screenshot.png")

    print("Test 1 passed!")


def test_search_on_wikipedia(page):
    # Go to Wikipedia
    page.goto("https://en.wikipedia.org/wiki/Main_Page")

    # Check the page title
    assert "Wikipedia" in page.title()

    # Use the first search box by its aria-label (as suggested by the error!)
    page.get_by_role("searchbox", name="Search Wikipedia").fill("Playwright automation")

    # Press Enter to search
    page.keyboard.press("Enter")

    # Wait for page to load
    page.wait_for_load_state("networkidle")

    # Check results page loaded
    assert "Playwright" in page.title()

    # Take a screenshot
    page.screenshot(path="wiki_results.png")

    print("Test 2 passed!")