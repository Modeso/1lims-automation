from ui_testing.testcases.base_test import BaseTest
from unittest import skip
from parameterized import parameterized
import re


class TestUnitsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_unit_page.get_test_units_page()

    @skip('https://modeso.atlassian.net/browse/LIMS-5237')
    def test001_test_units_search(self):
        """
        New: Test units: Search Approach: I can search by any field in the table view

        LIMS-3674
        :return:
        """
        row= self.test_unit_page.get_random_test_units_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '':
                continue
            self.base_selenium.LOGGER.info(' + search for {} : {}'.format(column, row_data[column]))
            search_results = self.article_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    def test002_archive_test_units(self):
        """
        New: Test units: Archive Approach: I can archive any test unit successfully.

        LIMS-3670
        :return:
        """
        selected_test_units_data, _ = self.test_unit_page.select_random_multiple_table_rows()
        self.test_unit_page.archive_selected_test_units()
        self.test_unit_page.get_archived_test_units()
        for test_unit in selected_test_units_data:
            test_unit_name = test_unit['Test Unit Name']
            self.base_selenium.LOGGER.info(' + {} Test Unit should be activated.'.format(test_unit_name))
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=test_unit_name))

    def test003_restore_test_units(self):
        """
         New: Test units: Restore Approach: I can restore any test unit successfully.

        LIMS-5262
        :return:
        """
        test_unit_names = []
        self.test_unit_page.get_archived_test_units()
        selected_test_units_data, _ = self.test_unit_page.select_random_multiple_table_rows()
        for test_unit in selected_test_units_data:
            test_unit_names.append(test_unit['Test Unit Name'])

        self.test_unit_page.restore_selected_test_units()
        self.test_unit_page.get_active_test_units()
        for test_unit_name in test_unit_names:
            self.assertTrue(self.test_unit_page.is_test_unit_in_table(value=test_unit_name))


    def test005_quantative_mibi_not_entering_dash_in_upper_limit(self):

        """
        Upper limit Approach, user can't enter  in the upper limit

        LIMS-3768
        """

        self.base_selenium.LOGGER.info('Search by Quantitative MiBi')
        testUnitsResults = self.test_unit_page.search(value ='Quantitative MiBi')

        self.base_selenium.LOGGER.info('Selecting the first testunit')
        testunitsRecords = self.order_page.result_table()
        self.test_unit_page.get_random_x(row=testunitsRecords[0])

        self.base_selenium.LOGGER.info('set the upper limit with \'-\' in case of quantitative mibi')
        self.test_unit_page.set_upper_limit(value='-')
        self.test_unit_page.sleep_tiny()

        self.base_selenium.LOGGER.info('pressing save')
        self.test_unit_page.press_save()

        self.base_selenium.LOGGER.info('Waiting for error message to make sure that validation forbids adding - in the upper limit')
        validation_result =  self.base_selenium.wait_element(element='general:oh_snap_msg')

        
        self.base_selenium.LOGGER.info('+ Assert error msg which indicates that it does not allow to add - in upper limit has appeared? {}'.format(validation_result))
        self.assertEqual(validation_result, True)


