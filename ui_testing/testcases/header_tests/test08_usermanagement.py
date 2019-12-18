from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip

class HeaderTestCases(BaseTest):
    def setUp(self):
            super().setUp()
            self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
            self.base_selenium.wait_until_page_url_has(text='dashboard')
            self.header_page.click_on_header_button()

    def test002_restore_user(self):
        """
        User management: Restore Approach: Make sure that you can restore any record successfully
        LIMS-6380
        :return:
            """
        self.header_page.click_on_user_management_button()
        user_names = []
        self.header_page.get_archived_users()
        selected_user_data, _ = self.header_page.select_random_multiple_table_rows()
        for user in selected_user_data:
            user_names.append(user['Name'])

        self.header_page.restore_selected_user()
        self.header_page.get_active_users()
        for user_name in user_names:
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=user_name))


