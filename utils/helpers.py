# Reusable helper functions
import os
from datetime import datetime

def take_screenshot(page, name):
    """Take screenshot with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"screenshots/{name}_{timestamp}.png"
    page.screenshot(path=path, full_page=True)
    print(f"✓ Screenshot saved: {path}")
    return path

def take_full_page_screenshot(page, name):
    """Take full page screenshot"""
    path = f"screenshots/{name}_full.png"
    page.screenshot(path=path, full_page=True)
    return path

def clear_screenshots():
    """Delete all screenshots"""
    folder = "screenshots"
    for file in os.listdir(folder):
        if file.endswith(".png"):
            os.remove(os.path.join(folder, file))
    print("✓ Screenshots cleared")