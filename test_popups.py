from playwright.sync_api import Page
import os

# ─── TEST 1: Handle Browser ALERT ───
def test_handle_alert(page: Page):

    # Go to a page that has alert dialogs
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("networkidle")
    print("✓ Page loaded")

    # STEP 1: Register listener BEFORE triggering alert
    # This automatically clicks OK on any alert
    page.on("dialog", lambda dialog: (
        print(f"✓ Alert caught! Message: {dialog.message}"),
        dialog.accept()
    ))

    # STEP 2: Click button that triggers alert
    page.get_by_role("button", name="Click for JS Alert").click()
    page.wait_for_timeout(1000)

    # STEP 3: Verify result message appeared
    result = page.locator("#result").text_content()
    assert "You successfully clicked an alert" in result
    print(f"✓ Alert handled! Result: {result}")

    page.screenshot(path="screenshots/alert_handled.png")


# ─── TEST 2: Handle Browser CONFIRM ───
def test_handle_confirm(page: Page):

    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("networkidle")

    # Accept confirm dialog (click OK)
    page.on("dialog", lambda dialog: (
        print(f"✓ Confirm caught! Message: {dialog.message}"),
        dialog.accept()
    ))

    page.get_by_role("button", name="Click for JS Confirm").click()
    page.wait_for_timeout(1000)

    result = page.locator("#result").text_content()
    assert "Ok" in result
    print(f"✓ Confirm accepted! Result: {result}")

    page.screenshot(path="screenshots/confirm_handled.png")


# ─── TEST 3: Dismiss CONFIRM dialog (click Cancel) ───
def test_dismiss_confirm(page: Page):

    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    page.wait_for_load_state("networkidle")

    # Dismiss confirm dialog (click Cancel)
    page.on("dialog", lambda dialog: (
        print(f"✓ Confirm caught! Dismissing..."),
        dialog.dismiss()
    ))

    page.get_by_role("button", name="Click for JS Confirm").click()
    page.wait_for_timeout(1000)

    result = page.locator("#result").text_content()
    assert "Cancel" in result
    print(f"✓ Confirm dismissed! Result: {result}")

    page.screenshot(path="screenshots/confirm_dismissed.png")


# ─── TEST 4: Handle HTML Modal Popup ───
def test_handle_html_modal(page: Page):

    # This site has a real HTML modal popup
    page.goto("https://the-internet.herokuapp.com/entry_ad")
    page.wait_for_load_state("networkidle")
    print("✓ Page loaded")

    # Wait for modal to appear
    page.wait_for_selector(".modal-title", timeout=5000)
    print("✓ Modal appeared!")

    # Read the modal title
    modal_title = page.locator(".modal-title").text_content()
    print(f"✓ Modal title: {modal_title}")

    # Screenshot with modal open
    page.screenshot(path="screenshots/modal_open.png")
    print("✓ Screenshot: modal open")

    # Close the modal by clicking X button
    page.locator(".modal-footer p").click()
    page.wait_for_timeout(500)

    # Verify modal is gone
    assert page.locator(".modal-title").is_hidden()
    print("✓ Modal closed successfully!")

    page.screenshot(path="screenshots/modal_closed.png")
    print("✓ Screenshot: modal closed")


# ─── TEST 5: Handle New Tab / Popup Window ───
def test_handle_new_tab(page: Page):

    page.goto("https://the-internet.herokuapp.com/windows")
    page.wait_for_load_state("networkidle")
    print("✓ Page loaded")

    # STEP 1: Tell Playwright to expect a new tab
    # Then click the link — order matters!
    with page.expect_popup() as new_tab_info:
        page.get_by_role("link", name="Click Here").click()

    # STEP 2: Get control of the new tab
    new_tab = new_tab_info.value
    new_tab.wait_for_load_state("networkidle")
    print(f"✓ New tab opened! URL: {new_tab.url}")

    # STEP 3: Do things in the new tab
    heading = new_tab.locator("h3").text_content()
    print(f"✓ New tab heading: {heading}")
    assert "New Window" in heading

    new_tab.screenshot(path="screenshots/new_tab.png")
    print("✓ Screenshot of new tab saved")

    # STEP 4: Close new tab and go back to original
    new_tab.close()
    print(f"✓ Back to original tab: {page.url}")

    page.screenshot(path="screenshots/back_to_original.png")


# ─── TEST 6: Handle File Download ───
def test_handle_download(page: Page):

    page.goto("https://the-internet.herokuapp.com/download")
    page.wait_for_load_state("networkidle")
    print("✓ Page loaded")

    # Create downloads folder
    os.makedirs("downloads", exist_ok=True)

    # STEP 1: Tell Playwright to expect a download
    with page.expect_download() as download_info:
        # Click first file link
        page.locator(".example a").first.click()

    # STEP 2: Get download object
    download = download_info.value
    print(f"✓ Download started: {download.suggested_filename}")

    # STEP 3: Save to our downloads folder
    save_path = f"downloads/{download.suggested_filename}"
    download.save_as(save_path)

    # STEP 4: Verify file was saved
    assert os.path.exists(save_path)
    print(f"✓ File saved to: {save_path}")

    page.screenshot(path="screenshots/download_done.png")