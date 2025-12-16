import pytest
from playwright.sync_api import expect

class TestLogin:
    """Test suite for Omega ERP login functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        
        self.page = page

  
    # Valid Login
   
    def test_valid_login(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.get_by_role("textbox", name="Email address").fill(credentials["email"])
        self.page.get_by_role("textbox", name="Password").fill(credentials["password"])
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        # expect(self.page.get_by_role("button", name="Collapse sidebar")).to_be_visible()
        # expect(self.page.get_by_role("button", name="User Management")).to_be_visible()
        expect(self.page.get_by_role("button", name=f"A admin_omega {credentials['email']}")).to_be_visible()
        expect(self.page.get_by_text("Service List")).to_be_visible()

   
    # Invalid Logins
   
    def test_valid_email_invalid_password(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.get_by_role("textbox", name="Email address").fill(credentials["email"])
        self.page.get_by_role("textbox", name="Password").fill("wrongpass")
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("Invalid credentials")).to_be_visible()
        expect(self.page).to_have_url(credentials["base_url"])

    def test_invalid_email_valid_password(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.get_by_role("textbox", name="Email address").fill("wrong@user.com")
        self.page.get_by_role("textbox", name="Password").fill(credentials["password"])
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("User Not Found")).to_be_visible()
        expect(self.page).to_have_url(credentials["base_url"])

    def test_invalid_email_invalid_password(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.get_by_role("textbox", name="Email address").fill("wrong@user.com")
        self.page.get_by_role("textbox", name="Password").fill("wrongpass")
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("User Not Found")).to_be_visible()
        expect(self.page).to_have_url(credentials["base_url"])

    
    # Empty Fields
   
    def test_empty_email_password(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.get_by_role("textbox", name="Email address").fill("")
        self.page.get_by_role("textbox", name="Password").fill("")
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("Email is required")).to_be_visible()
        expect(self.page.get_by_text("Password is required")).to_be_visible()
        expect(self.page).to_have_url(credentials["base_url"])

    
    # Email / Password Variations
    
    def test_email_with_spaces(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.get_by_role("textbox", name="Email address").fill(f"  {credentials['email']}  ")
        self.page.get_by_role("textbox", name="Password").fill(credentials["password"])
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        # expect(self.page.get_by_role("button", name="User Management")).to_be_visible()

    def test_email_case_sensitivity(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.get_by_role("textbox", name="Email address").fill("Admin@Omega.com")
        self.page.get_by_role("textbox", name="Password").fill(credentials["password"])
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        # expect(self.page.get_by_role("button", name="User Management")).to_be_visible()

    def test_password_case_sensitivity(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.get_by_role("textbox", name="Email address").fill(credentials["email"])
        self.page.get_by_role("textbox", name="Password").fill("OMEGA@123")  # wrong case
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("Invalid credentials")).to_be_visible()
        expect(self.page).to_have_url(credentials["base_url"])

    
    # Forgot Password
   
    def test_forget_password_link(self, credentials):
        self.page.goto(credentials["base_url"])
        self.page.locator(':text("Forgot password?")').click()
        expect(self.page).to_have_url(credentials["base_url"])
        self.page.locator('[name="email"]').fill(credentials["email"])
        self.page.locator('button:has-text("Send Reset Link")').click()
        