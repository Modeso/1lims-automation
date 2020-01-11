from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip
import time

class HeaderTestCases(BaseTest):

    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.header_page.click_on_header_button()

    # islam this just to check that the draggable is working then if this method merged
    # we will apply the draggable test cases in the table configuration
    def test020_draggable(self):
        """
        :return:
        """
        self.header_page.click_on_user_management_button()
        self.base_page.draggable_configure_table(source_element='user_management:config_changed_by',
                                                     destination_element='user_management:config_name',
                                                     apply_button='user_management:apply',
                                                     configure_table_button='user_management:config')





