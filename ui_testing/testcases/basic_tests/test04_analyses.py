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
    @parameterized.expand(['archive', 'restore'])
    def test002_archive_analysis(self, action):
        """
        In the analysis section, I can archive/restore any record successfully 
        I can archive or restore multiple records when I select them then press on restore/archive from the header 
        I can restore/archive one record from the options section

        LIMS-5035
        """
        
        if action == 'restore':
            self.base_selenium.LOGGER.info(' + Get Archived analyses ')
            self.analyses_page.get_archived_items()

        random_analysis_record = randint(1, 20)
        
        analysis_row = self.analyses_page.result_table()[random_analysis_record]

        self.analyses_page.click_check_box(source=analysis_row)
        analysis_data = self.base_selenium.get_row_cells_dict_related_to_header(
            row=analysis_row)
        analysis_numbers_list = analysis_data['Analysis No.'].split(',')

        if action == 'archive':
            self.base_selenium.LOGGER.info(
                ' + Archiveing analysis with number : {}'.format(analysis_data['Analysis No.']))
            analysis_record = self.analyses_page.archive_selected_analysis(
                check_pop_up=True)
                
            if analysis_record:
                self.base_selenium.LOGGER.info(
                    ' + Analysis number : {} archived successfully'.format(analysis_data['Analysis No.']))
                analysis_record = self.analyses_page.search(value=analysis_numbers_list[0])

                self.base_selenium.LOGGER.info('Analysis records with this number must be 0')
                self.assertEqual(len(analysis_record), 1)
                self.base_selenium.LOGGER.info(
                    ' + Assert analysis numbers : {} is not active'.format(analysis_numbers_list))
            else:
                self.base_selenium.LOGGER.info('Analysis couldn\'t be archived')

        elif action == 'restore':
            self.base_selenium.LOGGER.info(' + Restore Selected Row ')
            self.analyses_page.restore_selected_items()
            self.base_selenium.LOGGER.info(' + Get Active analyses')
            self.analyses_page.get_active_items()
            
            self.base_selenium.LOGGER.info('Making sure that analysis is now active successfully')
            record = self.analyses_page.search(value=analysis_data['Analysis No.'])[0]
            record_data = self.base_selenium.get_row_cells_dict_related_to_header(row=record)

            self.base_selenium.LOGGER.info(' + Analysis with number =  {} restored successfully?'.format(
            analysis_data['Analysis No.']))
            
            self.assertEqual(record_data['Analysis No.'].replace("'",''), analysis_data['Analysis No.'].replace("'",''))
