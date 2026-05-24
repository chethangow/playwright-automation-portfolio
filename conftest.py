import pytest
import os

# Create screenshots folder if it doesn't exist
os.makedirs("screenshots", exist_ok=True)
os.makedirs("videos", exist_ok=True)

# ─── VIDEO RECORDING SETUP ───
# This tells Playwright to record video for every test
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_video_size": {
            "width": 1280,
            "height": 720
        }
    }

# ─── AUTO SCREENSHOT ON FAILURE ───
# This runs after every test automatically
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only take screenshot when test FAILS
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # Save screenshot with test name
            screenshot_name = f"screenshots/FAILED_{item.name}.png"
            page.screenshot(path=screenshot_name)
            print(f"\n📸 Failure screenshot saved → {screenshot_name}")