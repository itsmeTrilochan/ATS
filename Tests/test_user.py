import pytest
from playwright.sync_api import expect
from faker import Faker

fake = Faker()


class TestLogin:
    """Test suite for login and user creation"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page

    # ---------------- LOGIN TEST ----------------

    def test_login(self, credentials):
        self.page.goto(credentials["base_url"])

        self.page.get_by_role("textbox", name="Email address").fill(credentials["email"])
        self.page.get_by_role("textbox", name="Password").fill(credentials["password"])
        self.page.get_by_role("checkbox", name="Remember me").check()
        self.page.get_by_role("button", name="Sign in").click()

        # ✅ Assertion
        expect(self.page.get_by_role("button", name="User Management")).to_be_visible()

    # ---------------- CREATE USER TEST ----------------

    def test_create_user(self, login_page):
        self.page = login_page  # already logged in

        # Navigate to User Management
        self.page.get_by_role("button", name="User Management").click()
        expect(self.page.get_by_role("heading", name="User Management")).to_be_visible()

        self.page.get_by_role("link", name="Users").click()
        self.page.get_by_role("link", name="Create").click()

        # -------- Faker Data --------
        username = fake.name()
        email = fake.unique.email()
        phone = fake.msisdn()[:10]
        password = fake.password(
            length=10,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )

        # Fill form
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.get_by_role("textbox", name="Email").fill(email)
        self.page.get_by_role("textbox", name="Phone").fill(phone)
        self.page.get_by_role("textbox", name="Password").fill(password)

        # Upload image ✅
        self.page.locator("input[type='file']").set_input_files("download.png")

        # Select roles
        self.page.get_by_label("Roles").select_option([
            "8b46dbf6-a589-49f9-9885-26ec5256c866",
            "4065dd81-5405-4a26-9321-9e543d318161"
        ])

        # Submit form ✅
        self.page.get_by_role("button", name="Save").click()

        # ✅ Ass
