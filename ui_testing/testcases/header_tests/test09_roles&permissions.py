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

    def test001_archive_roles_and_permissions(self):
        """
        Roles & Permissions: Make sure that you can archive any role record
        LIMS-6400
        :return:
        """
        self.header_page.click_on_roles_permissions_button()
        selected_roles_and_permissions_data, _ = self.header_page.select_random_multiple_table_rows()
        self.header_page.archive_selected_roles_and_permissions()
        self.header_page.get_archived_roles_and_permissions()
        for role in selected_roles_and_permissions_data:
            role_name = role['Name']
            self.base_selenium.LOGGER.info(' + {} role should be activated.'.format(role_name))
            self.assertTrue(self.header_page.is_role_in_table(value=role_name))

    def test002_restore_roles_and_permissions(self):
        """
        Roles & Permissions: Make sure that you can restore any role record
        LIMS-6104
        :return:
            """
        self.header_page.click_on_roles_permissions_button()
        role_names = []
        self.header_page.get_archived_roles_and_permissions()
        selected_role_data, _ = self.header_page.select_random_multiple_table_rows()
        for role in selected_role_data:
            role_names.append(role['Name'])

        self.header_page.restore_selected_roles()
        self.header_page.get_active_roles()
        for role_name in role_names:
            self.assertTrue(self.header_page.is_role_in_table(value=role_name))

    @skip('https://modeso.atlassian.net/browse/LIMS-6384')
    def test003_search_roles_and_permissions(self):
        """
        Header: Roles & Permissions: Search Approach: Make sure that you can search by any field in the active table successfully
        LIMS-6083
        :return:
        """
        self.header_page.click_on_roles_permissions_button()
        row = self.header_page.get_random_role_row()
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        for column in row_data:
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '':
                continue
            self.base_selenium.LOGGER.info(' + search for {} : {}'.format(column, row_data[column]))
            search_results = self.header_page.search(row_data[column])
            self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
                if search_data[column] == row_data[column]:
                    break
            self.assertEqual(row_data[column], search_data[column])

    def test004_export_roles_and_permissions(self):
        """
        Roles & Permissions: Make sure you can export all the data in the active table & it should display in the same order
        LIMS-6107
        :return:
        """
        self.header_page.click_on_roles_permissions_button()
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