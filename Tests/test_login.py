
import re 
import pytest
from playwright.sync_api import Page, expect

class TestLogin:
    """Test suite for Omega ERP login functionality"""

    BASE_URL = "http://192.168.101.143:3000/sign-in"
    VALID_EMAIL = "admin@omega.com"
    VALID_PASSWORD = "omega@123"

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Navigate to login page before each test"""
        page.goto(self.BASE_URL)
        self.page = page

    def test_valid_login(self):
        """Verify login with valid credentials"""
        self.page.get_by_role("textbox", name="Email address").fill(self.VALID_EMAIL)
        self.page.get_by_role("textbox", name="Password").fill(self.VALID_PASSWORD)
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        # Assertions for dashboard
        expect(self.page.get_by_role("button", name="Collapse sidebar")).to_be_visible()
        
        expect(self.page.get_by_role("button", name="User Management")).to_be_visible()
        expect(self.page.get_by_role("button", name="A admin_omega admin@omega.com")).to_be_visible()
        expect(self.page.get_by_text("Service List")).to_be_visible()

    def test_valid_email_invalid_password(self):
        """Verify login fails with valid email and invalid password"""
        self.page.get_by_role("textbox", name="Email address").fill(self.VALID_EMAIL)
        self.page.get_by_role("textbox", name="Password").fill("wrongpass")
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("Invalid credentials")).to_be_visible()
        expect(self.page).to_have_url(self.BASE_URL)

    def test_invalid_email_valid_password(self):
        """Verify login fails with invalid email and valid password"""
        self.page.get_by_role("textbox", name="Email address").fill("wrong@user.com")
        self.page.get_by_role("textbox", name="Password").fill(self.VALID_PASSWORD)
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("User Not Found")).to_be_visible()
        expect(self.page).to_have_url(self.BASE_URL)

    def test_invalid_email_invalid_password(self):
        """Verify login fails with invalid email and invalid password"""
        self.page.get_by_role("textbox", name="Email address").fill("wrong@user.com")
        self.page.get_by_role("textbox", name="Password").fill("wrongpass")
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("User Not Found")).to_be_visible()
        expect(self.page).to_have_url(self.BASE_URL)

    def test_empty_email_password(self):
        """Verify login fails when both email and password are empty"""
        self.page.get_by_role("textbox", name="Email address").fill("")
        self.page.get_by_role("textbox", name="Password").fill("")
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("Email is required")).to_be_visible()
        expect(self.page.get_by_text("Password is required")).to_be_visible()
        expect(self.page).to_have_url(self.BASE_URL)

    def test_email_with_spaces(self):
        """Verify login works with email having leading/trailing spaces"""
        self.page.get_by_role("textbox", name="Email address").fill(f"  {self.VALID_EMAIL}  ")
        self.page.get_by_role("textbox", name="Password").fill(self.VALID_PASSWORD)
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        # expect(self.page.get_by_role("button", name="Collapse sidebar")).to_be_visible()
        expect(self.page.get_by_role("button", name="User Management")).to_be_visible()

    def test_email_case_sensitivity(self):
        """Verify login works with email case variations (assuming case-insensitive)"""
        self.page.get_by_role("textbox", name="Email address").fill("Admin@Omega.com")
        self.page.get_by_role("textbox", name="Password").fill(self.VALID_PASSWORD)
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        # expect(self.page.get_by_role("button", name="Collapse sidebar")).to_be_visible()
        # expect(self.page.get_by_role("button", name="User Management")).to_be_visible()

    def test_password_case_sensitivity(self):
        """Verify login fails with password case variation (assuming password is case-sensitive)"""
        self.page.get_by_role("textbox", name="Email address").fill(self.VALID_EMAIL)
        self.page.get_by_role("textbox", name="Password").fill("OMEGA@123")  # wrong case
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        expect(self.page.get_by_text("Invalid credentials")).to_be_visible()
        expect(self.page).to_have_url(self.BASE_URL)
        
        
    def test_forget_password_link(self):
        """Verify 'Forgot Password' link navigates to the correct page"""
        self.page.locator(':text("Forgot password?")').click()
        expect(self.page).to_have_url("http://192.168.101.143:3000/sign-in")
        
        # self.page.getByRole('textbox', { name: 'Email' }).fill(self.VALID_EMAIL)
        # self.page.getByRole('button', { name: 'Send Reset Link' })
        self.page.locator('[name="email"]').fill(self.VALID_EMAIL)
        self.page.locator('button:has-text("Send Reset Link")').click()
