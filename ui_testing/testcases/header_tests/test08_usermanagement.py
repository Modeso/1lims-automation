from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip

class HeaderTestCases(BaseTest):
    def setUp(self):
            super().setUp()
            self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
            self.base_selenium.wait_until_page_url_has(text='dashboard')
            self.header_page.click_on_header_button()

    def test004_download_user_sheet(self):
        """
        User management: Make sure you can export all the data in the active table & it should display in the same order

        LIMS-6101
        :return:
        """
        self.header_page.click_on_user_management_button()
        self.base_selenium.LOGGER.info(' * Download XSLX sheet')
        self.header_page.download_xslx_sheet()
        rows_data = self.header_page.get_table_rows_data()
        for index in range(len(rows_data)):
            self.base_selenium.LOGGER.info(' * Comparing the user no. {} '.format(index))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.header_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)