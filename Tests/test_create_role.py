import pytest
from playwright.sync_api import expect, Page
from faker import Faker
import os

fake = Faker()


class TestRoleManagement:
    """Test suite for role creation and management"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page

    # ---------------- LOGIN TEST ----------------

    # def test_login(self, credentials):
    #     self.page.goto(credentials["base_url"])

    #     self.page.get_by_role("textbox", name="Email address").fill(credentials["email"])
    #     self.page.get_by_role("textbox", name="Password").fill(credentials["password"])
    #     self.page.get_by_role("checkbox", name="Remember me").check()
    #     self.page.get_by_role("button", name="Sign in").click()

    #     # ✅ Assertion - wait for navigation to complete
    #     expect(self.page.get_by_role("button", name="User Management")).to_be_visible(timeout=10000)

    # # ---------------- CREATE ROLE TEST ----------------
    class TestLogin:
       
     def test_create_role(self, login_page):
        # """Test creating a new role with permissions"""
        self.page = login_page  # already logged in

        # Navigate to User Management > Roles
        self.page.get_by_role("button", name="User Management").click()
        expect(self.page.get_by_role("heading", name="User Management")).to_be_visible()

        self.page.get_by_role("link", name="Roles").click()
        
        # Click Create button (adjust selector based on actual page)
        self.page.get_by_role("link", name="Create").click()
        
        # Wait for Create New Role form to load
        # expect(self.page.get_by_role("heading", name="Create New Role")).to_be_visible()
        expect(self.page.get_by_text('Create New Role')).to_be_visible()

        # -------- Generate Faker Data --------
        role_name = f"Role_{fake.job().replace(' ', '_')}"
        description = fake.text(max_nb_chars=100)

        # Fill basic information
        self.page.get_by_placeholder("Enter role name").fill(role_name)
        self.page.get_by_placeholder("Enter description").fill(description)

        # -------- Select Permissions --------
        
    #     # Method 1: Select specific permissions by clicking checkboxes
    #     self._select_application_permissions()
    #     self._select_evaluation_permissions()
    #     self._select_interview_permissions()
    #     self._select_job_permissions()

    #     # Method 2: Or select all permissions at once
    #     # self.page.get_by_text("Select All Permissions").click()

    #     # Submit the form
    #     self.page.get_by_role("button", name="Save").click()

    #     # ✅ Verify role was created successfully
    #     expect(self.page.get_by_text("Role created successfully")).to_be_visible(timeout=10000)

    # # ---------------- HELPER METHODS FOR PERMISSION SELECTION ----------------

    def _select_application_permissions(self):
        """Select Application permissions"""
        # Wait for Application section to be visible
        self.page.get_by_text("Application", exact=True).wait_for(state="visible")
        
        # Select specific permissions - adjust based on requirements
        permissions = ["create", "delete", "read", "update", "manage-offer", "move-stage"]
        
        for permission in permissions:
            # Use more specific locator within Application section
            checkbox = self.page.locator(f"text=Application >> .. >> text={permission} >> .. >> input[type='checkbox']").first
            if checkbox.is_visible():
                checkbox.check()

    def _select_evaluation_permissions(self):
        """Select Evaluation permissions"""
        self.page.get_by_text("Evaluation", exact=True).wait_for(state="visible")
        
        permissions = ["read", "submit"]
        
        for permission in permissions:
            checkbox = self.page.locator(f"text=Evaluation >> .. >> text={permission} >> .. >> input[type='checkbox']").first
            if checkbox.is_visible():
                checkbox.check()

    def _select_interview_permissions(self):
        """Select Interview permissions"""
        self.page.get_by_text("Interview", exact=True).wait_for(state="visible")
        
        permissions = ["read", "schedule", "update"]
        
        for permission in permissions:
            checkbox = self.page.locator(f"text=Interview >> .. >> text={permission} >> .. >> input[type='checkbox']").first
            if checkbox.is_visible():
                checkbox.check()

    def _select_job_permissions(self):
        """Select Job permissions"""
        self.page.get_by_text("Job", exact=True).wait_for(state="visible")
        
        permissions = ["create", "delete", "publish", "read", "unpublish", "update"]
        
        for permission in permissions:
            checkbox = self.page.locator(f"text=Job >> .. >> text={permission} >> .. >> input[type='checkbox']").first
            if checkbox.is_visible():
                checkbox.check('timeout=10000')