from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.articles_page import Articles
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.testunit_page import TstUnit
from ui_testing.pages.login_page import Login
from ui_testing.pages.order_page import Order
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.orders_api import OrdersAPI
from api_testing.apis.users_api import UsersAPI
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.article_api import ArticleAPI
from unittest import skip
from parameterized import parameterized
import random


class TestPlansTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.test_plan = TstPlan()
        self.test_plan_api = TestPlanAPI()
        self.article_api = ArticleAPI()
        self.set_authorization(auth=self.article_api.AUTHORIZATION_RESPONSE)
        self.test_plan.get_test_plans_page()

    def test001_test_plan_delete_testunit(self):
        """
        Testing deleting a test unit from test-plan create or update step two
        It deletes the first test unit in the chosen test plan and saves this,
        then refreshes the page and checks if the deletion was done correctly.

        LIMS-3504
        """
        self.info("get random completed test plan")
        random_completed_test_plan = random.choice(self.test_plan_api.get_completed_testplans())
        self.info("navigate to the test-plan No. {} edit page".format(random_completed_test_plan['number']))
        self.test_plan.get_test_plan_edit_page_by_id(random_completed_test_plan['id'])
        self.info("navigate to the testunits selection tab")
        self.test_plan.navigate_to_testunits_selection_page()
        old_testunits = self.test_plan.get_all_testunits_in_testplan()
        deleted_test_unit = (old_testunits[0])[0]
        self.info("delete the first testunit with name {}".format(deleted_test_unit))
        self.test_plan.delete_the_first_testunit_from_the_tableview()
        self.info("save the changes and refresh to make sure test unit deleted")
        self.test_plan.save_and_confirm_popup()
        self.test_plan.navigate_to_testunits_selection_page()
        all_testunits = self.test_plan.get_all_testunits_in_testplan()
        self.info('Checking if the changes were saved successfully')
        deleted_test_unit_found = self.test_plan.check_if_deleted_testunit_is_available(
            all_testunits=all_testunits, deleted_test_unit=deleted_test_unit)
        self.assertFalse(deleted_test_unit_found)

    @parameterized.expand(['InProgress', 'Completed'])
    def test002_test_plan_edit_status(self, status):
        """
        Creation Approach: when the status converted from completed to completed, new version created
        when the status converted from In-Progress to completed, no new version created

        LIMS-3502
        LIMS-3501
        """
        testplan = random.choice(self.test_plan_api.get_testplans_with_status(status=status))
        self.info('Navigate to edit page of test plan: {} with version: {}'.
                  format(testplan['testPlanName'], testplan['version']))
        self.test_plan.get_test_plan_edit_page_by_id(testplan['id'])
        self.info('Going to step 2 to add test unit to this test plan')
        self.info("select test unit of same material type of test plan and has values to complete test plan")
        test_unit = TestUnitAPI().get_test_unit_name_with_value_with_material_type(
            material_type=testplan['materialType'])
        self.test_plan.sleep_tiny()
        self.test_plan.set_test_unit(test_unit=test_unit['name'])
        if status == 'InProgress':
            self.info('Saving and completing the test plan')
            self.test_plan.save(save_btn='test_plan:save_and_complete', sleep=True)
        else:
            self.info('Saving and confirm pop up')
            self.test_plan.save_and_confirm_popup()

        self.info("go back to the active table and get test plan to check its version and status")
        self.test_plan.get_test_plans_page()
        new_test_plan_version, test_plan_row_data_status = \
            self.test_plan.get_testplan_version_and_status(search_text=testplan['testPlanName'])

        if status == 'InProgress':
            self.assertEqual(int(new_test_plan_version), testplan['version'])
        else:
            self.assertGreater(int(new_test_plan_version), int(testplan['version']))

        self.assertEqual(test_plan_row_data_status, 'Completed')

    def test003_archive_test_plan_one_record(self):
        """
        Archive one record

        LIMS-3506 Case 1
        """
        table = self.base_selenium.find_element('general:table')
        thead = table.find_elements_by_tag_name('thead')
        self.info(len(thead))
        self.info(thead[0].text)
        self.info('>>>>>>>')
        self.info(self.base_selenium.driver.find_element_by_id('testPlanName').text)


        self.info('choosing a random test plan table row')
        selected_test_plan = self.test_plan.select_random_table_row()
        self.assertTrue(selected_test_plan)
        self.info(f'selected_test_plan : {selected_test_plan}')
        testplan_number = selected_test_plan['Test Plan No.']
        self.info('Archive the selected item and navigating to the archived items table')
        self.test_plan.archive_selected_items()
        self.test_plan.get_archived_items()
        archived_row = self.test_plan.search(testplan_number)
        self.info('Checking if test plan number: {} is archived correctly'.format(testplan_number))
        self.assertIn(selected_test_plan['Test Plan Name'], archived_row[0].text)
        self.info('Test plan number: {} is archived correctly'.format(testplan_number))

    # def test004_restore_test_plan_one_record(self):
    #     """
    #      Restore one record
    #
    #      LIMS-3506 Case 1
    #     """
    #     self.info("Navigate to archived test plan table")
    #     self.test_plan.get_archived_items()
    #     self.info('Choosing a random testplan table row')
    #     self.test_plan.sleep_tiny()
    #     selected_test_plan = self.test_plan.select_random_table_row()
    #     self.assertTrue(selected_test_plan)
    #     testplan_number = selected_test_plan['Test Plan No.']
    #     self.info('select Testplan number: {} to be restored'.format(testplan_number))
    #     self.info('Restoring the selected item then navigating to the active items table')
    #     self.test_plan.restore_selected_items()
    #     self.test_plan.get_active_items()
    #     self.test_plan.filter_by_testplan_number(filter_text=testplan_number)
    #     restored_row = self.test_plan.result_table()
    #     self.info('Checking if testplan number: {} is restored correctly'.format(testplan_number))
    #     self.assertIn(selected_test_plan['Test Plan Name'], restored_row[0].text)
    #     self.info('Testplan number: {} is restored correctly'.format(testplan_number))
    #
    # def test005_archive_test_plan_multiple_records(self):
    #     """
    #     Archive multiple records
    #
    #     LIMS-3506 Case 2
    #     """
    #     self.info('Choosing random multiple test plans table rows')
    #     self.test_plan.sleep_small()
    #     rows_data, rows = self.test_plan.select_random_multiple_table_rows()
    #     self.assertTrue(rows_data)
    #     testplans_numbers = [row['Test Plan No.'] for row in rows_data]
    #     self.info('Testplan numbers: {} will be archived'.format(testplans_numbers))
    #     self.info('Archiving the selected items and navigating to the archived items table')
    #     self.test_plan.archive_selected_items()
    #     self.test_plan.sleep_small()
    #     self.info('Checking if testplans are archived correctly')
    #     self.test_plan.get_archived_items()
    #     archived_rows = self.test_plan.filter_multiple_rows_by_testplans_numbers(testplans_numbers)
    #     self.assertIsNotNone(archived_rows)
    #     self.assertEqual(len(archived_rows), len(testplans_numbers))
    #     self.info('Testplan numbers: {} are archived correctly'.format(testplans_numbers))
    #
    # def test006_restore_test_plan_multiple_records(self):
    #     """
    #     Rstore multiple records
    #
    #     LIMS-3506 Case 2
    #     """
    #     self.info("Navigate to archived test plan table")
    #     self.test_plan.get_archived_items()
    #     self.info('Choosing random multiple testplans table rows')
    #     self.test_plan.sleep_tiny()
    #     rows_data, rows = self.test_plan.select_random_multiple_table_rows()
    #     self.assertTrue(rows_data)
    #     testplans_numbers = [row['Test Plan No.'] for row in rows_data]
    #     self.info('Restore Testplans with numbers: {}'.format(testplans_numbers))
    #     self.test_plan.restore_selected_items()
    #     self.test_plan.sleep_small()
    #     self.info('Navigate to active table and make sure testplans restored')
    #     self.test_plan.get_active_items()
    #     restored_rows = self.test_plan.filter_multiple_rows_by_testplans_numbers(testplans_numbers)
    #     self.assertIsNotNone(restored_rows)
    #     self.assertEqual(len(restored_rows), len(testplans_numbers))
    #     self.info('Testplan numbers: {} are restored correctly'.format(testplans_numbers))

    #@skip('https://modeso.atlassian.net/browse/LIMS-6403')
    @skip('https://modeso.atlassian.net/browse/LIMSA-180')
    def test007_exporting_test_plan_one_record(self):
        """
        Exporting one record

        LIMS-3508 Case 1
        """
        self.info('Choosing a random testplan table row')
        row = self.test_plan.get_random_table_row('test_plans:test_plans_table')
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        testplan_number = row_data['Test Plan No.']
        self.info('Testplan number: {} will be exported'.format(testplan_number))
        self.info('Selecting the test plan row')
        self.test_plan.click_check_box(source=row)
        self.info('download XSLX sheet of selected test plan')
        self.test_plan.download_xslx_sheet()
        row_data_list = list(row_data.values())
        self.info('Comparing the testplan no. {} '.format(testplan_number))
        values = self.test_plan.sheet.iloc[0].values
        fixed_sheet_row_data = self.fix_data_format(values)
        fixed_row_data_list = self.fix_data_format(row_data_list)
        self.assertCountEqual(fixed_sheet_row_data, fixed_row_data_list)

    #@skip('https://modeso.atlassian.net/browse/LIMS-6403')
    @skip('https://modeso.atlassian.net/browse/LIMSA-180')
    def test008_exporting_test_plan_multiple_records(self):
        """
        Exporting multiple records

        LIMS-3508 Case 2
        """
        self.info('Choosing random multiple testplans table rows')
        rows = self.test_plan.select_random_multiple_table_rows(element='test_plans:test_plans_table')
        testplans_numbers = []
        for row in rows[0]:
            testplans_numbers.append(row['Test Plan No.'])
        self.info('Testplans numbers: {} will be exported'.format(testplans_numbers))

        self.test_plan.download_xslx_sheet()

        row_data_list = []
        for row_data in rows:
            row_data_list.append(list(row_data.values()))

        self.info('Comparing the testplan no. {} '.format(testplans_numbers))
        row_data_list = sorted(row_data_list, key=lambda x: x[1], reverse=True)

        for index in range(len(row_data_list)):
            fixed_row_data = self.fix_data_format(row_data_list[index])
            values = self.test_plan.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                if item != '' and item != '-':
                    self.assertIn(item, fixed_sheet_row_data)

    def test009_test_plan_duplicate(self):
        """
        Duplicate a test plan

        LIMS-3679
        """
        self.info('Choosing a random testplan table row')
        testPlan = random.choice(self.test_plan_api.get_completed_testplans())
        testunits = self.test_plan_api.get_testunits_in_testplan(id=testPlan['id'])
        self.info("select test plan {}".format(testPlan['testPlanName']))
        row = self.test_plan.search(testPlan['testPlanName'])
        self.test_plan.click_check_box(source=row[0])
        self.info('Duplicating testplan number: {}'.format(testPlan['number']))
        self.test_plan.duplicate_selected_item()
        duplicated_test_plan_number = self.test_plan.duplicate_testplan(change=['name'])
        self.info('testplan duplicated with number: {}'.format(duplicated_test_plan_number))
        self.info('get duplicated test plan data and child table data')
        duplicated_testplan_data, duplicated_testplan_childtable_data = \
            self.test_plan.get_specific_testplan_data_and_childtable_data(
                filter_by='number', filter_text=duplicated_test_plan_number)
        duplicated_test_units = []
        for testunit in duplicated_testplan_childtable_data:
            duplicated_test_units.append(testunit['Test Unit Name'])

        self.info('Asserting that the data is duplicated correctly')
        self.assertEqual(testPlan['materialType'], duplicated_testplan_data['Material Type'])
        self.assertEqual(testPlan['article'][0], duplicated_testplan_data['Article Name'])
        self.assertEqual(testPlan['articleNo'][0], duplicated_testplan_data['Article No.'])
        for testunit in testunits:
            self.assertIn(testunit['name'], duplicated_test_units)

    def test010_test_plan_completed_to_inprogress(self):
        """
        When the testplan status is converted from completed to in progress a new version is created

        LIMS-3503
        """
        self.info('get random completed test plan')
        completed_testplan = random.choice(self.test_plan_api.get_completed_testplans())
        self.assertTrue(completed_testplan)
        self.info('Navigating to edit page of testplan: {} with version: {}'.
                  format(completed_testplan['testPlanName'], completed_testplan['version']))
        self.test_plan.get_test_plan_edit_page_by_id(completed_testplan['id'])
        self.info('Going to step 2 to remove all the test units from it')
        self.test_plan.navigate_to_testunits_selection_page()
        self.test_plan.delete_all_testunits()
        self.test_plan.save_and_confirm_popup()

        self.info("go back to active table")
        self.test_plan.get_test_plans_page()

        self.info('Getting the currently changed testplan to check its status and version')
        inprogress_testplan_version, testplan_row_data_status = \
            self.test_plan.get_testplan_version_and_status(search_text=completed_testplan['testPlanName'])

        self.assertEqual(completed_testplan['version'] + 1, int(inprogress_testplan_version))
        self.assertEqual(testplan_row_data_status, 'In Progress')

    @parameterized.expand(['same', 'All'])
    def test011_create_testplans_same_name_article_materialtype(self, same):
        """
        LIMS-3499
        Testing the creation of two testplans with the same name, material type
        and article, this shouldn't happen

        LIMS-3500
        New: Test plan: Creation Approach: I can't create two test plans
        with the same name & same materiel type & one with any article
        and the other one all
        """
        self.info(" get random test plan with article != 'all")
        testplans = self.test_plan_api.get_all_test_plans_json(limit=10)
        self.assertTrue(testplans)
        testplans_list = [testplan for testplan in testplans if testplan['article'] != ['all']]
        first_testplan = random.choice(testplans_list)
        self.info("selected random test plan {}".format(first_testplan))
        self.info("create another testplan with the same data")
        if "same" == same:
            article_name = first_testplan['article'][0]
        else:
            article_name = 'All'

        self.test_plan.create_new_test_plan(name=first_testplan['testPlanName'],
                                            material_type=first_testplan['materialType'],
                                            article=article_name)
        self.info('Waiting for the error message')
        validation_result = self.base_selenium.wait_element(element='general:oh_snap_msg')
        self.info('Assert the error message')
        self.assertTrue(validation_result)

    def test012_create_testplans_same_name_different_materialtype(self):
        """
        Testing the creation of two testplans with the same name, but different material type
        and article. It should be created successfully.

        LIMS-3498
        """
        self.info(" get random test plan with article != 'all")
        testplans = self.test_plan_api.get_all_test_plans_json(limit=10)
        self.assertTrue(testplans)
        testplans_list = [testplan for testplan in testplans if testplan['article'] != ['all']]
        first_testplan = random.choice(testplans_list)
        self.info("selected random test plan {}".format(first_testplan))
        self.info('Create another testplan with the same name, but with different material type and article name')
        second_testplan_name = self.test_plan.create_new_test_plan(name=first_testplan['testPlanName'])
        self.info('New testplan is created successfully with name: {}, article name: {} and material type: {}'.format(
                second_testplan_name, self.test_plan.article, self.test_plan.material_type))

        self.assertEqual(first_testplan['testPlanName'], second_testplan_name)
        data = self.test_plan.search(second_testplan_name)
        self.assertGreaterEqual(len(data), 2)

    #@skip('https://modeso.atlassian.net/browse/LIMS-6405')
    def test013_delete_used_testplan(self):
        """
        If a testplan is used, it can't be deleted

        LIMS-3509
        """
        self.info("get random order with test plan")
        random_order, suborders, index = OrdersAPI().get_order_with_field_name(field='testPlans', no_of_field=1)
        self.info("selected order no {} has testplan name {}".format(suborders[index]['orderNo'],
                                                                     suborders[index]['testPlans'][0]))
        self.info('Testplan name: {} will be archived'.format(suborders[index]['testPlans'][0]))
        testplan_deleted = \
            self.test_plan.delete_selected_item_from_active_table_and_from_archived_table(
                item_name=suborders[index]['testPlans'][0])

        self.info("check for the error popup that this testplan is used and can't be deleted")
        self.assertFalse(testplan_deleted)

    def test014_archived_testplan_shouldnot_appear_in_order(self):
        """
        In case a testplan is archived, it shouldn't appear when creating a new order

        LIMS-3708
        """
        self.info("Navigate to orders page")
        self.order_page = Order()
        self.order_page.get_orders_page()
        self.info("get random archived testplan")
        response, payload = self.test_plan_api.get_all_test_plans(deleted="1")
        self.assertEqual(response['status'], 1, payload)
        archived_test_plan = random.choice(response['testPlans'])
        self.info("archived test plan data {}".format(archived_test_plan))
        self.info("create a new order with material type and article of archived testplan")
        if archived_test_plan['article'] != ['all']:
            self.order_page.create_new_order(material_type=archived_test_plan['materialType'],
                                             article=archived_test_plan['article'][0],
                                             test_plans=[archived_test_plan['testPlanName']])
        else:
            self.order_page.create_new_order(material_type=archived_test_plan['materialType'],
                                             test_plans=[archived_test_plan['testPlanName']])

        order_data = self.order_page.get_suborder_data()
        self.info("get the first suborder's testplan and make sure it's an empty string")
        self.assertCountEqual(order_data['suborders'][0]['testplans'], [''])

    def test015_testunit_sub_super_scripts(self):
        """
        Create a testunit with sub/super scripts, use this testunit to create a testplan
        and check the sub/super scripts in the card view

        LIMS-5796
        """
        self.info("create test unit with sub and super scripts")
        response, payload = TestUnitAPI().create_qualitative_testunit(unit='mg[2]{o}')
        self.assertEqual(response['status'], 1, payload)
        self.info("created test unit data {}".format(payload))
        self.info("create test plan with same created test unit data")
        if payload['selectedMaterialTypes'][0]['text'] == 'All':
            self.test_plan.create_new_test_plan(test_unit=payload['name'], save=False)
        else:
            self.test_plan.create_new_test_plan(material_type=payload['selectedMaterialTypes'][0]['text'],
                                                test_unit=payload['name'], save=False)

        unit = self.base_selenium.find_element('test_plan:testunit_unit').text
        self.assertEqual(unit, 'mg2o')

    def test016_filter_by_testplan_number(self):
        """
        User can filter with testplan number

        LIMS-6473
        """
        self.info("select random test plan")
        random_testplan = random.choice(self.test_plan_api.get_all_test_plans_json())
        self.info("selected_test_plan No {}".format(random_testplan['number']))
        self.test_plan.filter_by_testplan_number(random_testplan['number'])
        testplan_found = self.test_plan.result_table()
        self.assertIn(str(random_testplan['number']), (testplan_found[0].text).replace("'", ""))
        self.info('Filtering by number was done successfully')

    def test017_filter_by_testplan_name(self):
        """
        User can filter with testplan name

        LIMS-6470
        """
        random_testplan = random.choice(self.test_plan_api.get_all_test_plans_json())
        testplans_found = self.test_plan.filter_by_element_and_get_results(
            'Testplan Name', 'test_plans:testplan_name_filter', random_testplan['testPlanName'], 'drop_down')
        self.info('Checking if the results were filtered successfully')
        results_found = True
        while results_found:
            for tp in testplans_found:
                if len(tp.text) > 0:
                    self.assertIn(str(random_testplan['testPlanName']), tp.text)
            if self.test_plan.is_next_page_button_enabled():
                self.base_selenium.click('general:next_page')
                self.test_plan.sleep_small()
                testplans_found = self.test_plan.result_table()
            else:
                results_found = False

        self.info('Filtering by name was done successfully')

    @parameterized.expand(['Completed', 'In Progress'])
    def test018_filter_by_testplan_status(self, status):
        """
        User can filter with status

        LIMS-6474
        """
        testplans_found = \
            self.test_plan.filter_by_element_and_get_results('Status', 'test_plans:testplan_status_filter',
                                                             status, 'drop_down')

        if len(testplans_found):
            results_found = True
        else:
            self.info("filter failed or no elements with this status!")

        while results_found:
            for tp in testplans_found:
                if len(tp.text) > 0:
                    self.assertIn(status, tp.text)
                    if status == "In Progress":
                        self.assertNotIn('Completed', tp.text)
                    else:
                        self.assertNotIn('In Progress', tp.text)

            if self.test_plan.is_next_page_button_enabled():
                self.info('Navigating to the next page')
                self.base_selenium.click('general:next_page')
                self.test_plan.sleep_tiny()
                testplans_found = self.test_plan.result_table()
            else:
                results_found = False

        self.info('Filtering by status was done successfully')

    def test019_filter_by_testplan_changed_by(self):
        """
        User can filter with changed by field

        LIMS-6475
        """
        self.login_page = Login()
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.login_page.logout()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.test_plan.get_test_plans_page()

        testplan_name = self.test_plan.create_new_test_plan()

        self.info('New testplan is created successfully with name: {}'.format(testplan_name))

        self.test_plan.set_all_configure_table_columns_to_specific_value(value=True)

        testplan_found = self.test_plan.filter_by_element_and_get_results(
            'Changed By', 'test_plans:testplan_changed_by_filter', payload['username'], 'drop_down')
        self.assertEqual(len(testplan_found), 2)
        self.assertIn(payload['username'], testplan_found[0].text)
        self.assertIn(testplan_name, testplan_found[0].text)

    @parameterized.expand(['ok', 'cancel'])
    def test020_create_approach_overview_button(self, ok):
        """
        Master data: Create: Overview button Approach: Make sure
        after I press on the overview button, it redirects me to the active table

        LIMS-6203
        """
        self.info("click on create test plan button")
        self.test_plan.click_create_test_plan_button()
        self.info("click on Overview, this will display an alert to the user")
        self.test_plan.click_overview()
        # switch to the alert
        if 'ok' == ok:
            self.info("confirm pop-up")
            self.test_plan.confirm_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))
            self.info('clicking on Overview confirmed')
        else:
            self.info("cancel pop-up")
            self.test_plan.cancel_overview_pop_up()
            self.assertEqual(self.base_selenium.get_url(), '{}testPlans/add'.format(self.base_selenium.url))
            self.info('clicking on Overview cancelled')

    def test021_edit_approach_overview_button(self):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table

        LIMS-6202
        """
        testplan = random.choice(self.test_plan_api.get_all_test_plans_json())
        self.info('Navigate to edit page of test plan: {} '.format(testplan['testPlanName']))
        self.test_plan.get_test_plan_edit_page_by_id(testplan['id'])
        testplans_url = self.base_selenium.get_url()
        self.info('testplans_url : {}'.format(testplans_url))
        self.info('click on Overview, it will redirect you to test plans page')
        self.test_plan.click_overview()
        self.test_plan.sleep_tiny()
        self.assertEqual(self.base_selenium.get_url(), '{}testPlans'.format(self.base_selenium.url))
        self.info('clicking on Overview confirmed')

    def test022_testplans_search_then_navigate(self):
        """
        Search Approach: Make sure that you can search then navigate to any other page

        LIMS-6201
        """
        testplan = random.choice(self.test_plan_api.get_all_test_plans_json())
        search_results = self.test_plan.search(testplan['testPlanName'])
        self.assertGreater(len(search_results), 1, " * There is no search results for it, Report a bug.")
        for search_result in search_results:
            search_data = self.base_selenium.get_row_cells_dict_related_to_header(search_result)
            if search_data['Test Plan Name'] == testplan['testPlanName']:
                break
        else:
            self.assertTrue(False, " * There is no search results for it, Report a bug.")
        self.assertEqual(testplan['testPlanName'], search_data['Test Plan Name'])
        # Navigate to articles page
        self.info('navigate to articles page')
        Articles().get_articles_page()
        self.assertEqual(self.base_selenium.get_url(), '{}articles'.format(self.base_selenium.url))

    def test023_hide_all_table_configurations(self):
        """
        Table configuration: Make sure that you can't hide all the fields from the table configuration
        LIMS-6288
        """
        assert (self.test_plan.deselect_all_configurations(), False)

    def test024_test_unit_update_version_in_testplan(self):
        """
        Test plan: Test unit Approach: In case I update category & iteration of
        test unit that used in test plan with new version, when  go to test plan
        to add the same test unit , I found category & iteration updated

        LIMS-3703
        """
        self.test_unit_page = TstUnit()
        self.info("select random test unit to create the test plan with it")
        testunits, payload = TestUnitAPI().get_all_test_units(limited=20, filter='{"materialTypes":"all"}')
        testunit = random.choice(testunits['testUnits'])
        self.info('A random test unit is chosen, its name: {}, category: {} and number of iterations: {}'.format(
            testunit['name'], testunit['categoryName'], testunit['iterations']))

        self.info("create the first testplan")
        first_testplan_name, payload1 = self.test_plan_api.create_testplan()
        self.info('First test plan create with name: {}'.format(payload1['testPlan']['text']))

        self.info("go to testplan edit to get the number of iterations and test unit category")
        first_testplan_testunit_category, first_testplan_testunit_iteration =\
            self.test_plan.get_testunit_category_iterations(payload1['testPlan']['text'], testunit['name'])

        self.info("go to test units' active table and search for this test unit")
        self.test_unit_page.get_test_units_page()
        self.info('Navigating to test unit {} edit page'.format(testunit['name']))
        self.test_unit_page.search(value=testunit['name'])
        self.test_unit_page.open_edit_page(row=self.test_unit_page.result_table()[0])

        new_iteration = str(int(first_testplan_testunit_iteration) + 1)
        self.info("update the iteration and category")
        new_category = self.test_unit_page.set_category('')
        self.test_unit_page.set_testunit_iteration(new_iteration)
        self.info("press save and complete to create a new version")
        self.test_unit_page.save_and_create_new_version()

        self.info(" go back to test plans active table")
        self.test_plan.get_test_plans_page()

        self.info(" create new testplan with this testunit after creating the new version")
        second_testplan_name, payload2 = self.test_plan_api.create_testplan()
        self.info('Second test plan create with name: {}'.format(payload2['testPlan']['text']))

        self.info("check the iteration and category to be the same as the new version")
        self.info("go to testplan edit to get the number of iterations and testunit category")
        second_testplan_testunit_category, second_testplan_testunit_iteration = \
            self.test_plan.get_testunit_category_iterations(payload2['testPlan']['text'], testunit['name'])

        self.info('Asserting that the category of the test unit in the first testplan is not '
                  'equal the category of the test unit in the second testplan')
        self.assertNotEqual(first_testplan_testunit_category, second_testplan_testunit_category)
        self.info('Asserting that the iterations of the test unit in the first testplan is not '
                  'equal the iterations of the test unit in the second testplan')
        self.assertNotEqual(first_testplan_testunit_iteration, second_testplan_testunit_iteration)
        self.info('Asserting that the category of the test unit in the second testplan is the '
                  'same as the updated category')
        self.assertEqual(second_testplan_testunit_category, new_category)
        self.info('Asserting that the iterations of the test unit in the second testplan is the '
                  'same as the updated iterations')
        self.assertEqual(second_testplan_testunit_iteration, new_iteration)
