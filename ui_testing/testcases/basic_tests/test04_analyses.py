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


    def test001_export_analyses_sheet(self):
        """
        New: Orders: XSLX Approach: user can download all data in table view with the same order with table view
        LIMS-3274
        :return:
        """
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

    def test002_archive_analysis(self):
        
        analysis_row = self.analyses_page.result_table()[0]
        self.analyses_page.click_check_box(source=analysis_row)
        analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=analysis_row)
        analysis_numbers_list = analysis_data['Analysis No.'].split(',')
        self.base_selenium.LOGGER.info(
            ' + Archiveing analysis with number : {}'.format(analysis_data['Analysis No.']))
        analysis_archived = self.analyses_page.archive_selected_analysis(
            check_pop_up=True)
        self.base_selenium.LOGGER.info(' + {} '.format(analysis_archived))

        if analysis_archived:
            self.base_selenium.LOGGER.info(
                ' + Analysis number : {} archived successfully'.format(analysis_data['Analysis No.']))
            self.base_selenium.LOGGER.info(
                ' + Assert analysis numbers : {} is not active'.format(analysis_numbers_list))
            has_active_analysis = self.analyses_page.search_if_analysis_exist(
                analysis_numbers_list)
            self.base_selenium.LOGGER.info(
                ' + Has activated analysis? : {}.'.format(has_active_analysis))
            self.assertFalse(has_active_analysis)

    def test003_restore_archived_analyses(self):
        
        self.base_selenium.LOGGER.info(' + Get Archived analyses ')
        self.analyses_page.get_archived_items()
        self.base_selenium.LOGGER.info(' + Select Row ')
        selected_analysis_data = self.analyses_page.result_table()[0]
        analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(row=selected_analysis_data)
        self.analyses_page.click_check_box(source=selected_analysis_data)

        self.base_selenium.LOGGER.info(' + Restore Selected Row ')
        self.analyses_page.restore_selected_items()
        self.base_selenium.LOGGER.info(' + Get Active analyses')
        self.analyses_page.get_active_items()
        record = self.analyses_page.search(value=analysis_data['Analysis No.'])[0]
        record_data = self.base_selenium.get_row_cells_dict_related_to_header(row=record)
        self.base_selenium.LOGGER.info(' + Analysis with number =  {} restored successfully?'.format(
        analysis_data['Analysis No.']))
        self.assertEqual(record_data['Analysis No.'].replace("'",''), analysis_data['Analysis No.'].replace("'",''))

    def test004_deleted_archived_analysis(self):
        
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