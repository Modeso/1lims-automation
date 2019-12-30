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

    @parameterized.expand(['save_btn', 'cancel'])
    def test011_update_user_email_with_save_cancel_btn(self, save):
        """
        User management: I can update user email with save & cancel button
        LIMS-6397
        :return:
        """
        self.header_page.click_on_user_management_button()
        # open random user in the edit mode
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + user_url : {}'.format(user_url))
        self.order_page.sleep_tiny()
        current_email = self.header_page.get_user_email()
        self.header_page.set_user_email((self.header_page.generate_random_email()))
        new_email = self.header_page.get_user_email()
        if 'save_btn' == save:
            self.header_page.save(save_btn='user_management:save_btn')
        else:
            self.header_page.cancel(force=True)

        self.base_selenium.get(
            url=user_url, sleep=self.base_selenium.TIME_MEDIUM)

        user_email = self.header_page.get_user_email()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_email) == {} (user_email)'.format(new_email, user_email))
            self.assertEqual(new_email, user_email)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_email) == {} (user_email)'.format(current_email, user_email))
            self.assertEqual(current_email, user_email)

    def test012_validation_user_name_email_fields(self):
        """
        Header: User management: Make sure when the user update name & email then press on save button,
        red border display and he can't save
        LIMS-6121
        :return:
        """
        # from the create mode it will redirect me to the active table
        self.header_page.click_on_user_management_button()
        self.header_page.get_random_user()
        self.header_page.clear_user_name()
        self.header_page.clear_user_email()
        self.header_page.save(save_btn='user_management:save_btn')
        self.base_selenium.LOGGER.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.base_selenium.LOGGER.info('Assert error msg')
        self.assertEqual(validation_result, True)

