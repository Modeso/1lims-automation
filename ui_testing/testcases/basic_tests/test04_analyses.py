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
            for item in fixed_row_data:
                self.assertIn(item, fixed_sheet_row_data)
    
    def searching_by_capital_small_letters(self):
        """
        For all modules, if you search for any element in the table view,
        with a small letter it should show all matching results even the ones in capital letter without changing
        the capital letters that match the search to small lettersFor all modules,
        if you search for any element in the table view, with a capital letter it should show all matching results
        even the ones in small letter without changing the small letters that match the search to capital letters

        LIMS-3061
        """

        material_type='Raw Material'
        small_letters='raw material'
        capital_letters='RAW MATERIAL'
        
        self.base_selenium.LOGGER.info('Search for raw material as a mtaerial tybe in capital and small\nmake sure that results are written correctly as Raw Material')

        records = self.analyses_page.search(value=small_letters)

        self.base_selenium.LOGGER.info('Getting the data of the records and make sure it is writtent as Raw Material')

        for index in range(len(records)-1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=records[index])

            if row_data['Material Type'] != material_type:
                self.base_selenium.LOGGER.info('+ Assert material type, table data is: {}, and should be: {}'.format(row_data['Material Type'], material_type))
            
            self.assertEqual(row_data['Material Type'], material_type)

        records = self.analyses_page.search(value=capital_letters)
        self.base_selenium.LOGGER.info('Getting the data of the records and make sure it is writtent as Raw Material')

        for index in range(len(records)-1):
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=records[index])

            if row_data['Material Type'] != material_type:
                self.base_selenium.LOGGER.info('+ Assert material type, table data is: {}, and should be: {}'.format(row_data['Material Type'], material_type))
            
            self.assertEqual(row_data['Material Type'], material_type)
