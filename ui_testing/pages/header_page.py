from ui_testing.pages.base_pages import BasePages
from random import randint
import time


class Header(BasePages):
    def __init__(self):
        super().__init__()
        self.base_selenium.wait_until_page_url_has(text='dashboard')

    def click_on_header_button(self):
        self.base_selenium.LOGGER.info('Press on the header button')
        self.base_selenium.click(element='header:header_button')
        self.sleep_small()

    def click_on_user_management_button(self):
        self.base_selenium.LOGGER.info('Press on the user management button')
        self.base_selenium.click(element='header:user_management_button')
        self.sleep_small()

    def archive_selected_users(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='user_management:right_menu')
        self.base_selenium.click(element='user_management:archive')
        self.confirm_popup()

    def get_archived_users(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='user_management:right_menu')
        self.base_selenium.click(element='user_management:archived')
        self.sleep_small()

    def is_user_in_table(self, value):
        """
            - get_archived_test_units then call me to check if the test unit has been archived.
            - get_active_test_units then call me to check if the test unit is active.
        :param value: search value
        :return:
        """
        results = self.search(value=value)
        if len(results) == 0:
            return False
        else:
            if value in results[0].text:
                return True
            else:
                return False

    def restore_selected_user(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='user_management:right_menu')
        self.base_selenium.click(element='user_management:restore')
        self.confirm_popup()

    def get_active_users(self):
        self.base_selenium.scroll()
        self.base_selenium.click(element='user_management:right_menu')
        self.base_selenium.click(element='user_management:active')
        self.sleep_small()

    def get_random_user_row(self):
        return self.get_random_table_row(table_element='user_management:user_table')

