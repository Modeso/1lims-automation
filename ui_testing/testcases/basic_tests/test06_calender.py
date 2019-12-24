from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized


class CalenderTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.base_selenium.LOGGER.info('click on calender')
        self.calender_page.get_calender()

    @parameterized.expand(['contacts', 'articles', 'testUnits', 'testPlans'])
    def test001_open_calender(self, type):
        """
        Calendar: Make sure when you press on the calendar,
        the calendar open successfully

        LIMS-6359
        """
        page_name = "{}" + type
        url = page_name.format(self.base_selenium.url)
        self.base_selenium.get(url)
        self.base_selenium.LOGGER.info('click on calender')
        self.calender_page.get_calender()
        self.base_selenium.LOGGER.info(self.base_selenium.check_element_is_exist(element='calender:calender_title'))
        assert self.base_selenium.check_element_is_exist(element='calender:calender_title') == True

    def test002_navigate_calender(self):
        """
        Calendar: Make sure that you can navigate between months successfully
        LIMS-6376
        """
        month1 = self.calender_page.prev_month()
        self.base_selenium.LOGGER.info(month1)
        self.calender_page.sleep_tiny()
        month2 = self.calender_page.nxt_month()
        self.base_selenium.LOGGER.info(month2)
        self.calender_page.sleep_tiny()
        assert month1 != month2

    def test003_navigate_calender(self):
        """
        Calendar: Make sure that you can navigate between months successfully
        LIMS-6376
        """
        months = ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]
        current=self.calender_page.current_month().split(' ')[0]
        self.base_selenium.LOGGER.info(current)
        for a in months:
            if current==a:
                self.base_selenium.LOGGER.info("current month is ok")

