import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class AITestGenerator:

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def generate_test_cases(self, website_url, page_description):
        message = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"""
                Generate 5 Playwright Python test cases for:
                Website: {website_url}
                Description: {page_description}
                Rules:
                1. Use pytest format
                2. Use page: Page as parameter
                3. Include assertions
                4. Include page.screenshot()
                5. Return ONLY Python code
                6. Each test must start with def test_
                """
            }]
        )
        return message.content[0].text

    def generate_edge_cases(self, feature_description):
        message = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""
                Generate 5 edge case test scenarios for:
                Feature: {feature_description}
                Format each as:
                Test Name: ...
                Steps: ...
                Expected Result: ...
                Priority: High/Medium/Low
                """
            }]
        )
        return message.content[0].text

    def analyze_test_failure(self, error_message, test_code):
        message = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": f"""
                This Playwright test failed:
                ERROR: {error_message}
                CODE: {test_code}
                1. Explain why it failed
                2. Provide fixed code
                3. Explain what you changed
                """
            }]
        )
        return message.content[0].text