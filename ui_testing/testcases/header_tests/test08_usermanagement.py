from ui_testing.testcases.base_test import BaseTest
from parameterized import parameterized
import re
from unittest import skip
import time

class HeaderTestCases(BaseTest):

    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.header_page.click_on_header_button()

    def test001_archive_user_management(self):
        """
        User management: Make sure that you can archive any record
        LIMS-6379
        :return:
        """
        self.header_page.click_on_user_management_button()
        selected_user_management_data, _ = self.header_page.select_random_multiple_table_rows()
        self.header_page.archive_selected_users()
        self.header_page.get_archived_users()
        for user in selected_user_management_data:
            user_name = user['Name']
            self.base_selenium.LOGGER.info(' + {} user should be activated.'.format(user_name))
            self.assertTrue(self.header_page.is_user_in_table(value=user_name))

    def test002_restore_user(self):
        """
        User management: Restore Approach: Make sure that you can restore any record successfully
        LIMS-6380
        :return:
            """
        self.header_page.click_on_user_management_button()
        user_names = []
        self.header_page.get_archived_users()
        selected_user_data, _ = self.header_page.select_random_multiple_table_rows()
        for user in selected_user_data:
            user_names.append(user['Name'])

        self.header_page.restore_selected_user()
        self.header_page.get_active_users()
        for user_name in user_names:
            self.assertTrue(self.header_page.is_user_in_table(value=user_name))

    @skip('https://modeso.atlassian.net/browse/LIMS-6384')
    def test003_user_search(self):
        """
        Header:  User management:  Search Approach: Make sure that you can search by any field in the active table successfully
        LIMS-6082
        :return:
        """
        self.header_page.click_on_user_management_button()
        row = self.header_page.get_random_user_row()
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

    def test005_delete_user(self):
        """
        User management : Delete Approach: Make sure that you an delete any record successfully
        if this user not used in other entities
        LIMS-6381
        :return:
            """
        self.header_page.click_on_user_management_button()
        # create new user
        random_user_name = self.generate_random_string()
        created_user =self.header_page.create_new_user(user_name=random_user_name,
                                         user_email=(self.header_page.generate_random_email()),
                                         user_role='Admin', user_password='1',
                                         user_confirm_password='1')
        result = self.header_page.search(value=random_user_name)
        self.assertTrue(result, created_user)
        self.header_page.select_all_records()
        self.header_page.archive_selected_users()
        self.header_page.get_archived_users()
        self.base_selenium.LOGGER.info('make sure that that the user record navigate to the archive table')
        result = self.header_page.search(value=random_user_name)
        self.assertTrue(result, created_user)
        self.header_page.select_all_records()
        self.header_page.click_on_user_right_menu()
        self.header_page.click_on_delete_button()
        self.header_page.confirm_popup()
        result = self.header_page.search(value=random_user_name)
        self.base_selenium.LOGGER.info('deleted successfully')
        self.assertTrue(result, 'No records found')

    def test006_create_new_user(self):
        """
        Header: User management Approach:  Make sure that I can create new user successfully
        LIMS-6000
        :return:
        """
        self.header_page.click_on_user_management_button()
        #create new user
        random_user_name = self.generate_random_string()
        user_data= self.header_page.create_new_user(user_name = random_user_name, user_email=(self.header_page.generate_random_email()), user_role='',
                                         user_password='1', user_confirm_password='1')

        #make sure when you search you will find it
        result = self.header_page.search(value=random_user_name)
        self.assertTrue(result, user_data)


    def test007_overview_btn_from_create_edit_mode(self):
        """
        User Management: Overview button Approach: Make sure after you press on the overview button,
        it will redirect me to the active table
        LIMS-6396
        :return:
        """
        # from the create mode it will redirect me to the active table
        self.header_page.click_on_user_management_button()
        self.header_page.click_create_new_user()
        self.header_page.click_on_overview_btn()
        self.base_selenium.LOGGER.info('it will redirect me to the active table')
        self.header_page.get_users_page()
        self.assertEqual(self.base_selenium.get_url(), '{}users'.format(self.base_selenium.url))

        # from the edit mode it will redirect me to the active table
        self.header_page.get_random_user()
        self.header_page.click_on_overview_btn()
        self.base_selenium.LOGGER.info('it will redirect me to the active table')
        self.header_page.get_users_page()
        self.assertEqual(self.base_selenium.get_url(), '{}users'.format(self.base_selenium.url))

    @parameterized.expand(['save_btn', 'cancel'])
    def test008_update_user_name_with_save_cancel_btn(self, save):
        """
        User managemen: User management: I can update user name with save & cancel button
        LIMS-6395
        :return:
        """
        self.header_page.click_on_user_management_button()
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + user_url : {}'.format(user_url))
        self.order_page.sleep_tiny()
        #
        current_name = self.header_page.get_user_name()
        self.header_page.set_user_name(self.generate_random_string())
        new_name = self.header_page.get_user_name()
        if 'save_btn' == save:
            self.header_page.save(save_btn='user_management:save_btn')
        else:
            self.header_page.cancel(force=True)

        self.base_selenium.get(
            url=user_url, sleep=self.base_selenium.TIME_MEDIUM)

        user_name = self.header_page.get_user_name()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_name) == {} (user_name)'.format(new_name, user_name))
            self.assertEqual(new_name, user_name)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_name) == {} (user_name)'.format(current_name, user_name))
            self.assertEqual(current_name, user_name)

    @parameterized.expand(['save_btn', 'cancel'])
    def test009_update_user_role_with_save_cancel_btn(self, save):
        """
        User management: I can update user role with save & cancel button
        LIMS-6398
        :return:
        """
        self.header_page.click_on_user_management_button()
        # open random user in the edit mode
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + user_url : {}'.format(user_url))
        self.order_page.sleep_tiny()
        current_role = self.header_page.get_user_role()
        self.header_page.set_user_role()
        new_role = self.header_page.get_user_role()
        if 'save_btn' == save:
            self.header_page.save(save_btn='user_management:save_btn')
        else:
            self.header_page.cancel(force=True)

        self.base_selenium.get(
            url=user_url, sleep=self.base_selenium.TIME_MEDIUM)

        user_role = self.header_page.get_user_role()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (new_role) == {} (user_role)'.format(new_role, user_role))
            self.assertEqual(new_role, user_role)
        else:
            self.base_selenium.LOGGER.info(
                ' + Assert {} (current_role) == {} (user_role)'.format(current_role, user_role))
            self.assertEqual(current_role, user_role)

    @parameterized.expand(['save_btn', 'cancel'])
    def test010_update_user_email_with_save_cancel_btn(self, save):
        """
        User management: I can update user email with save & cancel button
        LIMS-6397
        :return:
        """
        self.header_page.click_on_user_management_button()
        # open random user in the edit mode
        self.header_page.get_random_user()
        user_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info(' + user_url : {}'.format(user_url))
        self.order_page.sleep_tiny()
        current_email = self.header_page.get_user_email()
        self.header_page.set_user_email((self.header_page.generate_random_email()))
        new_email = self.header_page.get_user_email()
        if 'save_btn' == save:
            self.header_page.save(save_btn='user_management:save_btn')
        else:
            self.header_page.cancel(force=True)

            self.base_selenium.get(
                url=user_url, sleep=self.base_selenium.TIME_MEDIUM)

        user_email = self.header_page.get_user_email()
        if 'save_btn' == save:
            self.base_selenium.LOGGER.info(
                    ' + Assert {} (new_email) == {} (user_email)'.format(new_email, user_email))
            self.assertEqual(new_email, user_email)
        else:
            self.base_selenium.LOGGER.info(
                    ' + Assert {} (current_email) == {} (user_email)'.format(current_email, user_email))
            self.assertEqual(current_email, user_email)

    def test011_validation_user_name_email_fields(self):
        """
        Header: User management: Make sure when the user update name & email then press on save button,
        red border display and he can't save
        LIMS-6121
        :return:
            """
        # from the create mode it will redirect me to the active table
        self.header_page.click_on_user_management_button()
        self.header_page.get_random_user()
        self.header_page.clear_user_name()
        self.header_page.clear_user_email()
        self.header_page.save(save_btn='user_management:save_btn')
        self.base_selenium.LOGGER.info('Waiting for error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.base_selenium.LOGGER.info('Assert error msg')
        self.assertEqual(validation_result, True)

    def test012_delete_user_not_used_in_other_entity(self):
        """
        User management: Make sure that you can't delete any user record If this record used in other entity
        LIMS-6407
        :return:
        """
        self.header_page.click_on_user_management_button()
        # create new user with random data
        user_random_name = self.generate_random_string()
        self.header_page.create_new_user(user_name=user_random_name,
                                         user_email=(self.header_page.generate_random_email()),
                                         user_role='Admin', user_password='1',
                                         user_confirm_password='1')

        self.base_selenium.LOGGER.info(
            'search to make sure that the user created '.format(user_random_name))
        created_user = self.header_page.search(user_random_name)[0]
        user_data = self.base_selenium.get_row_cells_dict_related_to_header(row=created_user)

        self.header_page.click_on_header_button()
        self.header_page.click_on_logout_button()

        # use this user in any other entity so you can login with it
        self.header_page.login_with_created_user(username=user_random_name, password='1')

        # make sure that I can login with the user that I created it
        time.sleep(15)
        self.assertIn('dashboard', self.login_page.base_selenium.get_url())

        self.header_page.click_on_header_button()
        self.header_page.click_on_user_management_button()

        self.base_selenium.LOGGER.info(
            'search to make sure after I login the user found in the active tabele '
                .format(user_random_name))
        self.header_page.search(value=user_random_name)

        self.header_page.select_all_records()
        # navigate to the archived table to delete it
        self.header_page.archive_selected_users()
        self.header_page.get_archived_users()

        self.header_page.select_all_records()
        self.header_page.click_on_user_right_menu()

        # make sure when you press on the delete button. message appear to confirm thaT I want to delete
        self.header_page.click_on_delete_button()
        self.header_page.confirm_popup()
        self.base_selenium.LOGGER.info(
            'message will appear this user related to some data & cant delete it')
        self.header_page.confirm_popup()

        self.base_selenium.LOGGER.info(
            'search to make sure this user found in the active table '.format(user_random_name))
        result = self.header_page.search(value=user_random_name)
        self.assertTrue(result, user_data)

    def test013_filter_by_user_name(self):
        """
        User management Approach: I can filter by user name successfully
        LIMS-6002
        :return:
        """
        self.header_page.click_on_user_management_button()
        random_user_name = self.generate_random_string()
        self.header_page.create_new_user(user_name=random_user_name, user_email=(self.header_page.generate_random_email()),
                                         user_role='', user_password='1', user_confirm_password='1')
        self.header_page.click_on_filter_view()

        user_filter = self.header_page.filter_user_by(filter_element='user_management:filter_name',
                                                      filter_text=random_user_name)
        result_user = self.header_page.result_table()[0]
        self.assertTrue(result_user, user_filter)
        self.header_page.filter_reset_btn()

    def test014_filter_by_email(self):
        """
        User management Approach: I can filter by user email successfully
        LIMS-6442
        :return:
        """
        self.header_page.click_on_user_management_button()
        random_user_name = self.generate_random_string()
        random_email = self.header_page.generate_random_email()
        self.header_page.create_new_user(user_name=random_user_name, user_email=random_email,
                                         user_role='', user_password='1', user_confirm_password='1')

        self.header_page.click_on_filter_view()

        user_filter = self.header_page.filter_user_by(filter_element='user_management:filter_email',
                                                      filter_text=random_email)

        result_user = self.header_page.result_table()[0]
        self.assertTrue(result_user, user_filter)
        self.header_page.filter_reset_btn()

    def test015_filter_by_role(self):
        """
        User management Approach: I can filter by user role successfully
        LIMS-6443
        :return:
        """
        self.header_page.click_on_user_management_button()
        random_user_name = self.generate_random_string()

        self.header_page.create_new_user(user_name=random_user_name, user_email=(self.header_page.generate_random_email()),
                                         user_role='Admin', user_password='1', user_confirm_password='1')


        self.header_page.click_on_filter_view()

        self.header_page.set_user_role(user_role='Admin')
        user_role = self.header_page.get_user_role()

        user_filter = self.header_page.filter_user_by(filter_element='user_management:filter_role',
                                                      filter_text=user_role)

        result_user = self.header_page.result_table()[0]
        self.assertTrue(result_user, user_filter)
        self.header_page.filter_reset_btn()



