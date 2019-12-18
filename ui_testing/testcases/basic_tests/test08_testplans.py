from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re, random


class TestPlansTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_plan.get_test_plans_page()

    @parameterized.expand(['ok', 'cancel'])
    def test001_overview_while_create_test_plans(self,ok):
        """"
        Master data: Create: Overview button Approach: Make sure after
        I press on the overview button, it redirects me to the active table

        LIMS-6203
        """
        self.test_plan.click_create_test_plan_button()
        self.test_plan.sleep_tiny()

        # click on Overview, this will display an alert to the user
        self.base_selenium.LOGGER.info('click on Overview')
        self.base_selenium.click(element='test_plans:overview')
        self.test_plan.sleep_tiny()
        # switch to the alert
        if 'ok' == ok:
            self.base_selenium.click(element='test_plans:confirm_overview')
            self.test_plan.sleep_tiny()
            self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))
            self.base_selenium.LOGGER.info('clicking on Overview confirmed')
        else:
            self.base_selenium.click(element='test_plans:cancel_overview')
            self.test_plan.sleep_tiny()
            self.assertEqual(self.base_selenium.get_url(), '{}testPlans/add'.format(self.base_selenium.url))
            self.base_selenium.LOGGER.info('clicking on Overview cancelled')


