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
        Header: User management Approach:  Make sure that I can create new user successfully
        LIMS-6000
        :return:
        """
        self.header_page.click_on_user_management_button()
        self.header_page.create_new_user(user_email='diana.mohamed@modeso.ch', user_role='',
                                         user_password='1', user_confirm_password='1')
        user_text = self.header_page.search(value=self.header_page.user_name)[0].text
        self.assertIn(self.header_page.user_name, user_text)




