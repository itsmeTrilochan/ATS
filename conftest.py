# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    """
    Launch a Chromium browser for the entire test session.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run tests in the background
        yield browser
        browser.close()
        
@pytest.fixture
def page(browser):
    """
    Create a new page in a new browser context for each test.
    Ensures test isolation.
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()
