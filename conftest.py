
# import pytest
# from playwright.sync_api import sync_playwright

# @pytest.fixture(scope="session")
# def browser():
#     """
#     Launch a Chromium browser for the entire test session.
#     """
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)  # Set headless=True to run tests in the background
#         yield browser
#         browser.close()
        
# @pytest.fixture
# def page(browser):
#     """
#     Create a new page in a new browser context for each test.
#     Ensures test isolation.
#     """
#     context = browser.new_context()
#     page = context.new_page()
#     yield page
#     page.close()
#     context.close()


import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()
        

            
            
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return { 
        **browser_context_args,
        "viewport": { "width": 1920, "height": 1080 }
    }
    
@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()