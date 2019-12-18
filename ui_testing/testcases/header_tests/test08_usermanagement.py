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

    def test001_archive_user_management(self):
        """
        User management: Make sure that you can archive any record
        LIMS-6379
        :return:
            """
        self.header_page.click_on_user_management_button()
        selected_user_management_data, _ = self.header_page.select_random_multiple_table_rows()
        self.header_page.archive_selected_users()
        self.header_page.get_archived_users()
        for user in selected_user_management_data:
            user_name = user['Name']
            self.base_selenium.LOGGER.info(' + {} user should be activated.'.format(user_name))
            self.assertTrue(self.header_page.is_user_in_table(value=user_name))


