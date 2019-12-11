from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re
import random


class TestPlansTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(
            username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.base_selenium.LOGGER.info('Getting the testplans page')
        self.test_plan.get_test_plans_page()

    def test001_test_plans_overview_link(self):
        """
        Test plans: Overview Approach: Make sure after I press on the overview button, it redirects me to the active table

        LIMS-6202
        :return:
        """
        # click on overview from create page
        self.test_plan.click_create_test_plan_button()  # click on create
        self.test_plan.click_overview_link()  # click on overview button
        # check if redirect to the right page
        current_page_name = self.test_plan.get_current_page_name()
        self.assertEqual(current_page_name, 'testPlans')
        self.test_plan.info('Overview visited from test plan create')

        # click on overview from edit page
        test_plan_row = self.test_plan.get_random_table_row('test_plans:test_plans_table') # get random row
        test_plan_row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=test_plan_row) # get its data
        test_plan_name = test_plan_row_data['Test Plan Name'] # get its name
        self.test_plan.get_test_plan_edit_page(test_plan_name) # open its edit page
        self.test_plan.click_overview_link(with_popup=False)  # click on overview button
        # check if redirect to the right page
        current_page_name = self.test_plan.get_current_page_name()
        self.assertEqual(current_page_name, 'testPlans')
        self.test_plan.info('Overview visited from test plan edit')
        return