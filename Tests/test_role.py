import pytest
from playwright.sync_api import Page, expect
from faker import Faker

fake = Faker()


class TestLogin:
    """Test suite for login and user creation"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page

    # ---------------- CREATE USER TEST ----------------
    def test_create_user(self, login_page: Page):
        page = login_page  # already logged in

        # Navigate to User Management
        page.get_by_role("button", name="User Management").click()
        expect(page.get_by_role("heading", name="User Management")).to_be_visible()

        page.get_by_role("link", name="Role").click()
        page.get_by_role("link", name="Create").click()

        # -------- Faker Data --------
        role_name = fake.job()
        role_description = fake.sentence(nb_words=8)

        # Fill role details
        page.fill("#name", role_name)
        page.fill("#description", role_description)

        # -------- Select Application Permissions --------
        page.get_by_text("Application", exact=True).wait_for(state="visible")
        permissions = ["create", "delete", "read", "update", "manage-offer", "move-stage"]
        for permission in permissions:
            checkbox = page.locator(
                f"text=Application >> .. >> text={permission} >> .. >> input[type='checkbox']"
            ).first
            if checkbox.is_visible():
                checkbox.check()

        # -------- Select Evaluation Permissions --------
        page.get_by_text("Evaluation", exact=True).wait_for(state="visible")
        permissions = ["read", "submit"]
        for permission in permissions:
            checkbox = page.locator(
                f"text=Evaluation >> .. >> text={permission} >> .. >> input[type='checkbox']"
            ).first
            if checkbox.is_visible():
                checkbox.check()

        # -------- Select Interview Permissions --------
        page.get_by_text("Interview", exact=True).wait_for(state="visible")
        permissions = ["read", "schedule", "update"]
        for permission in permissions:
            checkbox = page.locator(
                f"text=Interview >> .. >> text={permission} >> .. >> input[type='checkbox']"
            ).first
            if checkbox.is_visible():
                checkbox.check()

        # -------- Select Job Permissions --------
        page.get_by_text("Job", exact=True).wait_for(state="visible")
        permissions = ["create", "delete", "publish", "read", "unpublish", "update"]
        for permission in permissions:
            checkbox = page.locator(
                f"text=Job >> .. >> text={permission} >> .. >> input[type='checkbox']"
            ).first
            if checkbox.is_visible():
                checkbox.check()

        # Submit
        page.get_by_role("button", name="Create Role").click()
