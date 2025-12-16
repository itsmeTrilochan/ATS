import pytest
from playwright.sync_api import sync_playwright, Page

@pytest.fixture(scope="session")
def credentials():
    """Provide login credentials and base URL"""
    return {
        "base_url": "http://192.168.101.143:3000/sign-in",
        "email": "admin@omega.com",
        "password": "omega@123"
    }

@pytest.fixture(scope="session")
def browser():
    """Launch browser once per session"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()  # Playwright stops automatically here

@pytest.fixture()
def page(browser):
    """Create a new page with fresh context"""
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture()
def login_page(page: Page, credentials):
    """Perform login and return logged-in page"""
    page.goto(credentials["base_url"])
    page.get_by_role("textbox", name="Email address").fill(credentials["email"])
    page.get_by_role("textbox", name="Password").fill(credentials["password"])
    page.get_by_role("checkbox", name="Remember me").check()
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_selector("button:has-text('User Management')")
    return page
