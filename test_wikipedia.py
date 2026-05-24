from playwright.sync_api import Page

def test_wikipedia_python_search(page: Page):
    # Step 1: Go to Wikipedia
    page.goto("https://en.wikipedia.org/wiki/Main_Page")
    assert "Wikipedia" in page.title()
    print("✓ Wikipedia loaded")

    # Step 2: Search for Python programming
    page.get_by_role("searchbox", name="Search Wikipedia").click()
    page.get_by_role("combobox", name="Search Wikipedia").fill("Python programming")
    page.get_by_role("combobox", name="Search Wikipedia").press("Enter")
    print("✓ Search done")

    # Step 3: Click the Python article
    page.get_by_role("link", name="Python (programming language)", exact=True).click()
    page.wait_for_load_state("networkidle")
    assert "Python" in page.title()
    print("✓ Python article opened")

    # Step 4: Click History of Python
    page.get_by_role("link", name="History of Python").click()
    page.wait_for_load_state("networkidle")
    assert "History" in page.title()
    print("✓ History page opened")

    # Step 5: Screenshot as proof
    page.screenshot(path="python_wiki.png")
    print("✓ Screenshot saved!")