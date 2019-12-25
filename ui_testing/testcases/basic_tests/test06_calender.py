from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized


class CalenderTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.base_selenium.LOGGER.info('click on calender')

    @parameterized.expand(['contacts', 'articles', 'testUnits', 'testPlans'])
    def test001_open_calender(self, type):
        """
        Calendar: Make sure when you press on the calendar,
        the calendar open successfully

        LIMS-6359

        Calendar: When I press on the calendar, it should
        redirect me to the correct analysis

        LIMS-6218
        """
        page_name = "{}" + type
        url = page_name.format(self.base_selenium.url)
        self.base_selenium.get(url)
        self.base_selenium.LOGGER.info('click on calender')
        self.calender_page.get_calender()
        self.base_selenium.LOGGER.info(self.base_selenium.check_element_is_exist(element='calender:calender_title'))
        assert self.base_selenium.check_element_is_exist(element='calender:calender_title') == True
        self.base_selenium.click(element='calender:open_analysis')
        self.calender_page.sleep_small()

    def test002_navigate_calender(self):
        """
        Calendar: Make sure that you can navigate between months successfully

        LIMS-6376
        """
        self.base_selenium.LOGGER.info('click on calender')
        self.calender_page.get_calender()
        months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
                  "NOVEMBER", "DECEMBER"]
        prev_month = self.calender_page.prev_month()
        current = self.calender_page.current_month()
        nxt_month = self.calender_page.nxt_month()
        assert current in months
        assert prev_month in months
        assert nxt_month in months
        current_index = months.index(current)
        if current_index == 0:
            assert months.index(prev_month) == 11
            assert months.index(nxt_month) == 1
        elif current_index == 11:
            assert months.index(nxt_month) == 0
            assert months.index(prev_month) == 10
        else:
            assert months.index(prev_month) == current_index - 1
            assert months.index(nxt_month) == current_index + 1

    def test003_hover_test_units_analysis(self):
        """
        Calendar: Make sure when you hover on any test unit results,
        all the test unit name inside it appear on the right hand side
        LIMS-6377
        """
        # open calender
        self.base_selenium.LOGGER.info('click on calender')
        self.calender_page.get_calender()
        # make sure Test Units Analysis Overview is selected
        calender_overview= self.calender_page.which_overview()
        if "Analysis" in calender_overview:
            self.calender_page.switch_overview()
            self.base_selenium.LOGGER.info('switched to Test Unit Overview')
        else:
            self.base_selenium.LOGGER.info('Already on Test Unit Overview')


