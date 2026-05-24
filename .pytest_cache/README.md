# Playwright Automation Testing Portfolio

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.59-green)
![Tests](https://img.shields.io/badge/Tests-61-brightgreen)

A professional browser automation framework built with Python + Playwright.

## Tech Stack
- Python 3.14
- Playwright 1.59
- Pytest
- Allure Reports
- GitHub Actions CI/CD

## What is Tested
- Google homepage verification
- Wikipedia search automation
- SauceDemo full e-commerce journey
- Flipkart real website automation
- REST API testing
- Cross browser testing Chrome Firefox Safari

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### Run all tests
```bash
pytest tests/ -v
```

### Run smoke tests only
```bash
pytest tests/smoke/ -v
```

### Run with HTML report
```bash
pytest tests/ -v --html=reports/report.html
```

### Run on all browsers
```bash
pytest tests/ --browser chromium --browser firefox --browser webkit
```

## Test Results
| Test Suite | Tests | Status |
|------------|-------|--------|
| Smoke Tests | 3 | ✅ Passing |
| E2E Tests | 50+ | ✅ Passing |
| API Tests | 10 | ✅ Passing |
| Cross Browser | 12 | ✅ Passing |
| Data Driven | 18 | ✅ Passing |
| Total | 61 | ✅ Passing |

## Project Structure

## Author
Chethan Gowda S - QA Automation Engineer