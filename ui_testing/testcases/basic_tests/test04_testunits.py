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

    def test006_search_by_archived_testunit (self):
        """
        Archived test units shouldn't display in the test plan step two & also in the analysis step two.

        LIMS-3677
        """

        self.base_selenium.LOGGER.info('Generate new random name to make sure that this testunit will be archived')
        newRandomName = self.generate_random_string()

        self.base_selenium.LOGGER.info('filter by all to make sure that testunits will have material type all, to be added in any testplan')
        testunitsRecords = self.order_page.search(value='all')
        self.test_unit_page.get_random_x(row=testunitsRecords[0])

        self.base_selenium.LOGGER.info('Edit the name to be: {}'.format(newRandomName))
        self.test_unit_page.set_testunit_name(name=newRandomName)

        self.base_selenium.LOGGER.info('Save the new data')
        self.test_unit_page.saveAndCreateNewVersion()

        self.base_selenium.LOGGER.info('Get testunits page')
        self.test_unit_page.get_test_units_page()

        self.base_selenium.LOGGER.info('Search by the testunit name {} to archive'.format(newRandomName))
        results = self.test_unit_page.search(value=newRandomName)

        self.base_selenium.LOGGER.info('Archive the testunit')
        self.test_unit_page.select_random_multiple_table_rows()
        self.test_unit_page.archive_selected_test_units()

        self.base_selenium.LOGGER.info('Get testplans page')
        self.test_plan.get_test_plans_page()

        self.base_selenium.LOGGER.info('Get first record in testplans page')
        testplansRecords = self.test_plan.result_table()
        self.test_plan.get_random_x(row=testplansRecords[0])

        self.base_selenium.LOGGER.info('Set the new testunit')
        testUnitAdded = self.test_plan.set_test_unit(test_unit=newRandomName)

        self.base_selenium.LOGGER.info('+ Assert doesn testunit available in the testunits dropdown? : {}'.format(testUnitAdded))
        self.assertEqual(testUnitAdded, False)


