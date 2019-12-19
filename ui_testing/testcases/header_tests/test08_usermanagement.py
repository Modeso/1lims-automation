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

    def test005_create_new_user(self):
        """
        User management: Make sure you can export all the data in the active table & it should display in the same order

        LIMS-6101
        :return:
        """
        self.header_page.click_on_user_management_button()
        self.header_page.create_new_user(user_email='diana.mohamed@modeso.ch', user_role='', user_password='1')
