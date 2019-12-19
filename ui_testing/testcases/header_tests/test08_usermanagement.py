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

    def test006_delete_user(self):
        """
        User management : Delete Approach: Make sure that you an delete any record successfully
        LIMS-6381
        :return:
            """
        self.header_page.click_on_user_management_button()
        self.header_page.get_archived_users()
        user_row =self.header_page.get_random_table_row('user_management:user_table')
        self.order_page.click_check_box(source=user_row)
        user_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=user_row)
        self.header_page.click_on_user_right_menu()
        self.header_page.click_on_delete_button()
        user_deleted = self.header_page.click_on_the_confirm_message()
        self.base_selenium.LOGGER.info(' + {} '.format(user_deleted))
        # In case the user record is deleted
        if user_deleted:
         self.base_selenium.LOGGER.info(
                ' + user number : {} deleted successfully'.format(user_data['User No.']))
         self.assertEqual(self.base_selenium.get_text(element='user_management:alert_confirmation'), 'Successfully deleted')
        else:
         self.base_selenium.LOGGER.info(
                ' + pop up will appear that this item related to some data : {}'.format(user_data))
         self.assertFalse(self.header_page.confirm_popup())


