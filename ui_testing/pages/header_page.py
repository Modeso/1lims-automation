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



    def create_new_user(self, user_role='', sleep=True, user_email='', user_password=''):
        self.base_selenium.LOGGER.info(' + Create new user.')
        self.base_selenium.click(element='user_management:create_user_button')
        time.sleep(self.base_selenium.TIME_SMALL)
        self.user_name = self.generate_random_text()
        self.set_user_name(user_name=self.user_name)
        self.set_user_email(user_email)
        self.set_user_role(user_role)
        self.user_role = self.get_user_role()
        self.set_user_password(user_password=self.user_password)
        self.set_user_confirm_password(user_confirm_password=self.set_user_confirm_password())

        self.save(sleep)


    def set_user_name(self, user_name):
        self.base_selenium.set_text(element="user_management:user_name", value=user_name)


    def set_user_email(self, user_email):
        self.base_selenium.set_text(element="user_management:user_email", value=user_email)

    def set_user_password(self, user_password):
        self.base_selenium.set_text(element="user_management:user_password", value=user_password)

    def set_user_confirm_password(self, user_confirm_password):
        self.base_selenium.set_text(element="user_management:user_confirm_password", value=user_confirm_password)

    def get_user_role(self):
        return self.base_selenium.get_text(element='user_management:user_role').split('\n')[0]

    def set_user_role(self, user_role='', random=False):
        if random:
            self.base_selenium.select_item_from_drop_down(element='user_management:user_role', avoid_duplicate=True)
            return self.get_user_role()
        else:
            self.base_selenium.select_item_from_drop_down(element='user_management:user_role', item_text=user_role)


