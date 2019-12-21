from ui_testing.testcases.base_test import BaseTest
import time

class CalenderTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.base_selenium.LOGGER.info(self.base_selenium.check_element_is_exist(element='calender:get_calender'))


    def test001_click_on_calnder(self):
        self.base_selenium.LOGGER.info('click on calender')
        self.base_selenium.click(element='calender:get_calender')
        time.sleep(25)
        self.base_selenium.LOGGER.info(self.base_selenium.check_element_is_exist(element='calender:calender_title'))
        time.sleep(15)

