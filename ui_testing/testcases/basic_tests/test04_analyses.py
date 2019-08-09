import re
from unittest import skip
from parameterized import parameterized
from ui_testing.testcases.base_test import BaseTest
from random import randint
import time


class AnalysesTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(
            username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.analyses_page.get_analyses_page()


    def test003_deleted_archived_analysis(self):
        """
        I can delete any analysis record successfully 
        Make sure you can’t delete more then one record at the same time 

        LIMS-5037
        """
        self.analyses_page.get_archived_items()
        analysis_row = self.analyses_page.result_table()[0]
        self.analyses_page.click_check_box(source=analysis_row)

        analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=analysis_row)
        analysis_numbers_list = analysis_data['Analysis No.'].split(',')

        self.base_selenium.LOGGER.info(
            ' + Delete analysis has number = {}'.format(analysis_data['Analysis No.']))
        self.analyses_page.delete_selected_item()
        self.assertFalse(self.analyses_page.confirm_popup())

        self.base_selenium.LOGGER.info(
            ' + Is analysis number {} deleted successfully?'.format(analysis_numbers_list))
        has_active_analysis = self.analyses_page.search_if_analysis_exist(
            analysis_numbers_list)
        self.base_selenium.LOGGER.info(' + {} '.format(has_active_analysis))
        self.assertFalse(has_active_analysis)
