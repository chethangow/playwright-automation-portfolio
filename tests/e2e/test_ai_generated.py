import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
))

import pytest
from playwright.sync_api import Page
from utils.ai_test_generator import AITestGenerator


@pytest.mark.skip(reason="Requires Anthropic API billing")
def test_ai_generates_test_cases():
    generator = AITestGenerator()
    print("\n🤖 Asking Claude to generate test cases...")
    test_cases = generator.generate_test_cases(
        website_url="https://www.saucedemo.com",
        page_description="E-commerce login page with username and password"
    )
    os.makedirs("ai_generated", exist_ok=True)
    with open("ai_generated/test_ai_login.py", "w") as f:
        f.write(test_cases)
    assert len(test_cases) > 100
    print("✓ AI successfully generated test cases!")


@pytest.mark.skip(reason="Requires Anthropic API billing")
def test_ai_generates_edge_cases():
    generator = AITestGenerator()
    print("\n🤖 Asking Claude to generate edge cases...")
    edge_cases = generator.generate_edge_cases(
        feature_description="Login form with email and password validation"
    )
    os.makedirs("ai_generated", exist_ok=True)
    with open("ai_generated/edge_cases.txt", "w") as f:
        f.write(edge_cases)
    assert len(edge_cases) > 100
    print("✓ AI successfully generated edge cases!")


@pytest.mark.skip(reason="Requires Anthropic API billing")
def test_ai_analyzes_failure():
    generator = AITestGenerator()
    failing_test = """
def test_login(page):
    page.goto("https://saucedemo.com")
    page.locator("#username").fill("standard_user")
    page.locator("#pwd").fill("secret_sauce")
    page.locator("#btn-login").click()
    assert "inventory" in page.url
"""
    error = "TimeoutError: Locator #username not found after 30000ms"
    analysis = generator.analyze_test_failure(
        error_message=error,
        test_code=failing_test
    )
    os.makedirs("ai_generated", exist_ok=True)
    with open("ai_generated/failure_analysis.txt", "w") as f:
        f.write(analysis)
    assert len(analysis) > 100
    print("✓ AI successfully analyzed the failure!")


def test_ai_guided_browser_test(page: Page):
    print("\n🤖 Running AI guided browser test...")
    page.goto("https://www.saucedemo.com")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.wait_for_load_state("networkidle")
    assert "inventory" in page.url
    page.screenshot(path="screenshots/ai_generated_test.png")
    print("✓ AI guided test completed!")