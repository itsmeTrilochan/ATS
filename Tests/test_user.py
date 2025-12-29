import pytest
from playwright.sync_api import expect
from faker import Faker
from pathlib import Path

fake = Faker()


class TestLogin:
    """Test suite for login and user creation"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page

    # ---------------- CREATE USER TEST ----------------
    def test_create_user(self, login_page):
        page = login_page  # already logged in

        # Navigate to User Management
        page.get_by_role("button", name="User Management").click()
        expect(page.get_by_role("heading", name="User Management")).to_be_visible()

        page.get_by_role("link", name="Users").click()
        page.get_by_role("link", name="Create").click()

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
        page.get_by_role("textbox", name="Username").fill(username)
        page.get_by_role("textbox", name="Email").fill(email)
        page.get_by_role("textbox", name="Phone").fill(phone)
        page.get_by_role("textbox", name="Password").fill(password)

        # Upload image
        # file_path = Path("tests/assets/download.png")
        # # page.locator("input[type='file']").set_input_files(file_path)
        # page.locator("input[type='file']").set_input_files(str(file_path))
        
        # file_path = Path("C:\Users\Omega\Desktop\test images\download.png")
        file_path = Path("C:\\Users\\Omega\\Desktop\\test images\\download.png")

      

        page.locator("input[type='file']").set_input_files(str(file_path))


        # Select roles
        page.select_option(
        "#roleIds",
        [
        "019b4552-0010-7b88-8881-bd5c76fb34e4"
       ]
)
        expect(page.get_by_text("Image uploaded successfully")).to_be_visible()


        # Submit form
        page.get_by_role("button", name="Create User").click()

        # Final assertion
        expect(page.get_by_text("User created")).to_be_visible()
