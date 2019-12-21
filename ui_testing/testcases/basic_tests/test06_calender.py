from ui_testing.testcases.base_test import BaseTest
import time
from parameterized import parameterized

class CalenderTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.base_selenium.LOGGER.info(self.base_selenium.check_element_is_exist(element='calender:get_calender'))

    def test001_click_on_calender(self):
        """
        Calendar: Make sure when you press on the calendar,
        the calendar open successfully

        LIMS-6359
        """
        self.base_selenium.LOGGER.info('click on calender')
        self.base_selenium.click(element='calender:get_calender')
        time.sleep(5)
        self.base_selenium.LOGGER.info(self.base_selenium.check_element_is_exist(element='calender:calender_title'))
        assert self.base_selenium.check_element_is_exist(element='calender:calender_title')==True

    @parameterized.expand(['contacts', 'articles','testUnits','testPlans'])
    def test002_open_calender(self,type):
        """
        Calendar: Make sure when you press on the calendar,
        the calendar open successfully

        LIMS-6359
        """
        page_name= "{}"+ type
        url=page_name.format(self.base_selenium.url)
        self.base_selenium.get(url)
        time.sleep(5)
        self.base_selenium.LOGGER.info('click on calender')
        self.base_selenium.click(element='calender:get_calender')
        time.sleep(5)
        assert self.base_selenium.check_element_is_exist(element='calender:calender_title')==True

    def test003_navigate_calender(self):
        """
        Calendar: Make sure that you can navigate between months successfully
        LIMS-6376
        """
        self.base_selenium.LOGGER.info('click on calender')
        self.base_selenium.click(element='calender:get_calender')
        time.sleep(5)
        assert self.base_selenium.check_element_is_exist(element='calender:calender_title')==True
        self.base_selenium.click(element='calender:prev')
        month1=self.base_selenium.get_text(element='calender:month')
        self.base_selenium.LOGGER.info(month1)
        time.sleep(5)
        self.base_selenium.click(element='calender:nxt')
        month2 = self.base_selenium.get_text(element='calender:month')
        self.base_selenium.LOGGER.info(month2)
        time.sleep(5)
        assert month1!=month2


