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


    def test001_export_analyses_sheet_approve_result(self):
        """
        Approved results should display in XSLX file.
        LIMS-3765
        """
        self.base_selenium.LOGGER.info('Filter by approved to make sure that the records has approved result')
        self.analyses_page.search(value='Approved')
        self.base_selenium.LOGGER.info(' * Download XSLX sheet')
        self.analyses_page.select_all_records()
        self.analyses_page.download_xslx_sheet()
        rows_data = self.analyses_page.get_table_rows_data()
        for index in range(len(rows_data) - 1):
            self.base_selenium.LOGGER.info(
                ' * Comparing the analysis no. {} '.format(index + 1))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.analyses_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            self.base_selenium.LOGGER.info('{}'.format(fixed_row_data))
            self.base_selenium.LOGGER.info('{}'.format(fixed_sheet_row_data))
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)
