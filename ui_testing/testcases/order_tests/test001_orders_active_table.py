from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.order_page import Order
from ui_testing.pages.order_page import SubOrders
from ui_testing.pages.orders_page import Orders
from ui_testing.pages.login_page import Login
from api_testing.apis.orders_api import OrdersAPI
from ui_testing.pages.analysis_page import AllAnalysesPage
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.users_api import UsersAPI
from parameterized import parameterized
from unittest import skip
from random import randint
import random, re
from nose.plugins.attrib import attr


class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.contacts_api = ContactsAPI()
        self.test_unit_api = TestUnitAPI()
        self.set_authorization(auth=self.contacts_api.AUTHORIZATION_RESPONSE)
        self.order_page.get_orders_page()
        self.test_unit_api.set_name_configuration_name_only()
        self.orders_api.set_configuration()

    @parameterized.expand(['order', 'sub_order'])
    def test001_options_icon_items(self, order):
        """
         orders :Make sure that when user click on options of order or suborder,
         it displays Four options: (Duplicate, COA, Mail, Archive)

         LIMS-5367
         LIMS-5360
        """
        self.info('select random order')
        random_row = self.orders_page.get_random_table_row(table_element='general:table')
        if order == 'sub_order':
            self.info('open child table')
            self.orders_page.open_child_table(source=random_row)
            self.info('get child table records')
            table_records = self.orders_page.result_table(element='general:table_child')
        else:
            table_records = self.orders_page.result_table(element='general:table')
        self.info('get values in options menu')
        values = self.orders_page.get_suborder_options(table_records[0]).split('\n')
        self.assertEqual(values, ['Duplicate', 'CoA', 'Mail', 'Archive'])

    def test002_edit_icon_of_main_order(self):
        """
         Make Sure that when user click on edit icon it will be redirect to the first step
         of the merged page that has the order data(Order Table with Add).

         LIMS-5371
        """
        self.info('choose random order and click on edit button')
        self.orders_page.sleep_tiny()
        order_data = self.orders_page.get_random_order()
        order_no = self.order_page.get_order_no()
        self.assertTrue(self.base_selenium.wait_element(element='orders:edit order header'))
        self.assertEqual(order_no, order_data['Order No.'])

    def test003_check_orders_active_table_list_menu(self):
        """
          [Orders][Active table] Make sure that list menu will contain
          (COA,Archive , XSLX - Archived - Configurations) Only

          LIMS-5358
        """
        options = ['Duplicate', 'CoA', 'Archive', 'XSLX', 'Archived', 'Configurations']
        list = self.orders_page.get_right_menu_options()
        self.assertCountEqual(list, options)

    def test004_archive_main_order(self):
        """"
        User can archive a main order

        LIMS-6516
        """
        self.info('choosing a random order table row')
        selected_order = self.orders_page.select_random_table_row()
        self.assertTrue(selected_order)
        self.info('selected order : {}'.format(selected_order))
        order_number = selected_order['Order No.'].replace("'", "")
        self.info('Archive the selected item and navigating to the archived items table')
        self.orders_page.archive_selected_items()
        self.orders_page.get_archived_items()
        self.orders_page.filter_by_order_no(order_number)
        self.assertEqual(len(self.orders_page.result_table()-1), 1)
        self.info('Checking if order number: {} is archived correctly'.format(order_number))
        order_data = self.orders_page.get_the_latest_row_data()
        self.assertEqual(order_number, order_data['Order No.'].replace("'", ""))
        self.info('Order number: {} is archived correctly'.format(order_number))

    def test005_archive_multiple_orders(self):
        """
        Orders: Archive Approach: Make sure that you can select multiple records
        and then archive them at the same time

        LIMS-5364
        """
        self.info("select multiple orders and archive them")
        orders_data, rows = self.order_page.select_random_multiple_table_rows(element='orders:orders_table')
        self.assertTrue(self.orders_page.archive_selected_orders(check_pop_up=True))
        self.info("Navigate to archived orders table")
        self.orders_page.get_archived_items()
        for i in range(len(orders_data)):
            order_no = orders_data[i]['Order No.']
            self.info('asserting order with order number {} is successfully archived'.format(order_no))
            self.orders_page.filter_by_order_no(order_no)
            self.assertEqual(len(self.order_page.result_table())-1, 1)
            result_data = self.orders_page.get_the_latest_row_data()
            self.assertIn(order_no.replace("'", ""), result_data['Order No.'].replace("'", ""))

    def test006_archive_main_order_reflect_on_analysis(self):
        """
        New: Orders Form: Archive main order: Make sure when the user archive main order,
        the analysis corresponding to it will be archived also
        LIMS-6873
        """
        self.info("create order with multiple suborders using api")
        response, payload = self.orders_api.create_order_with_multiple_suborders()
        self.assertEqual(response['status'], 1)
        order_no = response['order']['orderNo']
        order_id = response['order']['mainOrderId']
        suborders = self.orders_api.get_suborder_by_order_id(order_id)[0]['orders']
        number_of_suborders = len(suborders)
        analysis_no_list = [suborder['analysis'][0] for suborder in suborders]
        self.info(" Archive order with number : {}".format(order_no))
        self.orders_page.filter_by_order_no(order_no)
        self.assertEqual(len(self.orders_page.result_table()) - 1, 1)
        self.assertTrue(self.orders_page.archive_main_order_from_order_option())
        self.info("Navigate to archived orders' table and filter by analysis no")
        self.orders_page.get_archived_items()
        self.orders_page.filter_by_analysis_number(analysis_no_list[0])
        self.assertTrue(self.orders_page.is_order_in_table(value=order_no))
        child_data = self.orders_page.get_child_table_data()
        result_analysis = [suborder['Analysis No.'].replace("'", "") for suborder in child_data]
        self.assertCountEqual(result_analysis, analysis_no_list)

    def test007_restore_archived_order(self):
        """
         Orders: Restore Approach: User can restore any order from the archived table

         LIMS-5361
        """
        self.info("create order with multiple suborders using api")
        response, payload = self.orders_api.create_order_with_multiple_suborders()
        self.assertEqual(response['status'], 1)
        order_no = response['order']['orderNo']
        order_id = response['order']['mainOrderId']
        suborders = self.orders_api.get_suborder_by_order_id(order_id)[0]['orders']
        number_of_suborders = len(suborders)
        analysis_numbers = [suborder['analysis'][0] for suborder in suborders]
        self.info("archive order no {} using api".format(order_no))
        archive_response, _ = self.orders_api.archive_main_order(order_id)
        self.assertEqual(archive_response['message'], 'archive_success')
        self.info("Navigate to archived orders table")
        self.orders_page.get_archived_items()
        self.orders_page.filter_by_order_no(order_no)
        self.info("restore order no {}".format(order_no))
        row = self.orders_page.result_table()[0]
        self.orders_page.click_check_box(row)
        self.orders_page.restore_selected_items()
        self.info('Navigate to orders active table')
        self.orders_page.sleep_tiny()
        self.orders_page.get_active_items()
        self.orders_page.filter_by_order_no(order_no)
        self.assertEqual(len(self.orders_page.result_table() - 1), 1)
        self.info('Checking if order number: {} is archived correctly'.format(order_no))
        order_data = self.orders_page.get_the_latest_row_data()
        self.assertEqual(order_no, order_data['Order No.'].replace("'", ""))
        self.info('assert that all suborders restored')
        child_data = self.orders_page.get_child_table_data(open_child=True)
        restored_analysis_numbers = [item['Analysis No.'].replace("'", "") for item in child_data]
        self.assertEqual(len(child_data), number_of_suborders)
        self.info('asserting restored suborders are correct')
        self.assertCountEqual(analysis_numbers, restored_analysis_numbers)

    def test008_delete_main_order(self):
        """
        New: Order without/with article: Deleting of orders
        The user can hard delete any archived order

        LIMS-3257
        """
        response, payload = self.orders_api.get_all_orders(deleted=1)
        self.assertEqual(response['status'], 1, 'No archived orders')
        random_order = random.choice(response['orders'])
        suborders_response, _ = self.orders_api.get_suborder_of_archived_order(random_order['id'])
        self.assertEqual(suborders_response['status'], 1)
        suborders_data = suborders_response['orders']
        analysis_no_list = [suborder['analysis'][0] for suborder in suborders_data]
        self.info('Navigate to archived table')
        self.orders_page.get_archived_items()
        self.info('Delete order with data {}'.format(random_order['orderNo']))
        self.orders_page.filter_by_order_no(random_order['orderNo'])
        row = self.orders_page.result_table()[0]
        self.orders_page.click_check_box(row)
        self.order_page.delete_selected_item()
        self.orders_page.confirm_popup()
        self.info('filter by order no {} to make sure no result found'.format(random_order['orderNo']))
        self.orders_page.filter_by_order_no(random_order['orderNo'])
        deleted_order = self.orders_page.result_table()[0]
        self.assertTrue(deleted_order.get_attribute("textContent"), 'No data available in table')
        self.info('Navigate analysis page and assert analysis no {} not found'.format(analysis_no_list))
        self.orders_page.navigate_to_analysis_active_table()
        for analysis in analysis_no_list:
            self.analyses_page.filter_by_analysis_number(analysis)
            self.analyses_page.close_filter_menu()
            deleted_analysis = self.analyses_page.result_table()[0]
            self.assertTrue(deleted_analysis.get_attribute("textContent"), 'No data available in table')

    def test009_delete_multiple_orders(self):
        """
        Orders: Make sure that you can't delete multiple orders records at the same time
        LIMS-6854
        """
        self.info("navigate to archived items' table")
        self.orders_page.get_archived_items()
        self.orders_page.select_random_multiple_table_rows()
        self.orders_page.delete_selected_item(confirm_pop_up=False)
        confirm_edit = self.base_selenium.check_element_is_exist(element="general:cant_delete_message")
        confirm_edit_message = self.base_selenium.get_text(element="general:confirmation_pop_up")
        self.assertTrue(confirm_edit)
        self.assertIn('You cannot do this action on more than one record', confirm_edit_message)

    # @skip("https://modeso.atlassian.net/browse/LIMSA-281")
    # @skip("https://modeso.atlassian.net/browse/LIMSA-280")
    def test010_archive_sub_order(self):
        """
        orders :Make sure that by clicking on Archive from Suborder options a confirmation popup will appear
        and user can Archive this suborder with its corresponding analysis
        LIMS-3739
        LIMS-5369
        """
        self.info('select random order')
        random_row = self.orders_page.get_random_table_row(table_element='general:table')
        self.info('open child table')
        self.orders_page.open_child_table(source=random_row)
        self.info('archive suborder from orders active table')
        child_table_records = self.orders_page.result_table(element='general:table_child')
        sub_orders = self.orders_page.get_table_data(table_element='general:table_child')
        selected_sub_order = randint(0, len(sub_orders) - 1)
        analysis_no = sub_orders[selected_sub_order]['Analysis No.']
        self.orders_page.open_row_options(row=child_table_records[selected_sub_order])
        self.base_selenium.click(element='orders:suborder_archive')
        self.assertTrue(self.base_selenium.check_element_is_exist(element='general:confirmation_pop_up'))
        self.orders_page.confirm_popup()
        self.orders_page.get_archived_items()
        self.info('make sure that suborder is archived')
        self.orders_page.filter_by_analysis_number(analysis_no)
        self.orders_page.open_child_table(source=self.orders_page.result_table()[0])
        results = self.order_page.result_table(element='general:table_child')[0].text
        self.assertIn(analysis_no.replace("'", ""), results.replace("'", ""))

    def test011_restore_archived_sub_orders(self):
        """
        I can restore any sub order successfully
        LIMS-4374
        """
        self.info("create order with multiple suborders using api")
        response, payload = self.orders_api.create_order_with_multiple_suborders()
        self.assertEqual(response['status'], 1)
        order_no = response['order']['orderNo']
        order_id = response['order']['mainOrderId']
        suborders = self.orders_api.get_suborder_by_order_id(order_id)[0]['orders']
        self.info("archive order no {} using api".format(order_no))
        archive_response, _ = self.orders_api.archive_main_order(order_id)
        self.assertEqual(archive_response['message'], 'archive_success')
        self.info("Navigate to archived orders table")
        self.orders_page.get_archived_items()
        self.orders_page.filter_by_order_no(order_no)
        random_index = randint(0, len(suborders) - 1)
        suborders_data = self.order_page.get_child_table_data()
        self.assertEqual(len(suborders_data), len(suborders))
        self.info("Restore suborder with analysis No {}".format(suborders_data[random_index]['Analysis No.']))
        self.order_page.restore_table_suborder(index=random_index)
        self.info('Navigate to orders active table')
        self.orders_page.sleep_tiny()
        self.orders_page.get_active_items()
        self.orders_page.filter_by_order_no(order_no)
        self.info('assert that only one suborder restored')
        child_data = self.orders_page.get_child_table_data(open_child=False)
        self.assertEqual(len(child_data), 1)
        self.assertEqual(suborders_data[random_index]['Analysis No.'].replace("'", ""),
                         child_data[0]['Analysis No.'].replace("'", ""))

    def test012_delete_suborder(self):
        """
         Delete sub order Approach: In case I have main order with multiple sub orders,
         make sure you can delete one of them
         LIMS-6853
        """
        self.info('get random order with multiple suborders')
        order = self.orders_api.get_order_with_multiple_sub_orders()
        self.order_page.search(order['orderNo'])
        self.info('archive first suborder')
        suborder_data = self.order_page.get_child_table_data()[0]
        self.order_page.archive_sub_order_from_active_table()
        self.orders_page.delete_sub_order(analysis_no=suborder_data['Analysis No.'])

        self.info('Navigate to order page to make sure that suborder is deleted and main order still active')
        self.order_page.get_orders_page()
        self.order_page.search(order['orderNo'])
        suborders_after_delete = self.order_page.get_child_table_data()
        self.assertNotIn(suborder_data['Analysis No.'], suborders_after_delete)
        self.assertGreater(len(suborder_data), 0)

        self.info('Navigate to Analysis page to make sure that analysis related to deleted suborder not found')
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.apply_filter_scenario(filter_element='analysis_page:analysis_no_filter',
                                                 filter_text=suborder_data['Analysis No.'], field_type='text')
        self.assertEqual(len(self.order_page.result_table()), 1)

    def test013_order_of_test_units_in_analysis(self):
        """
        Orders: Ordering test units: Test units in the analysis section should display
        in the same order as in the order section
        LIMS-7415
        """
        self.info('create new order with 3 test units')
        response, payload = self.orders_api.create_order_with_test_units(3)
        self.info('get test units of order')
        order_testunits = [test_unit['name'] for test_unit in payload[0]['testUnits']]
        self.info('navigate to analysis tab')
        self.orders_page.navigate_to_analysis_active_table()
        self.info('filter by order number')
        self.analyses_page.filter_by_order_no(payload[0]['orderNoWithYear'])
        self.info('get child table data')
        table_data = self.analyses_page.get_child_table_data()
        analysis_testunits = [test_unit['Test Unit'] for test_unit in table_data]
        self.assertCountEqual(order_testunits, analysis_testunits)

    def test014_cancel_archive_reflect_on_anlaysis(self):
        """
        [Archiving][MainOrder]Make sure that if user cancel archive order,
        No order or suborders or analysis of the order will be archived
        LIMS-5404
        """
        self.info('create order with 3 suborders')
        import ipdb;ipdb.set_trace()
        response, payload = self.orders_api.create_order_with_multiple_suborders(no_suborders=3)
        self.assertEqual(response['status'], 1)
        suborders_data, _ = self.orders_api.get_suborder_by_order_id()
        suborders = suborders_data['orders']
        self.assertEqual(3, len(suborders))
        analysis_no = [suborder['analysis'][0] for suborder in suborders]
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        self.info('click on arhcive then cancel popup')
        self.orders_page.archive_main_order_from_order_option(check_pop_up=True, confirm=False)
        table_records = self.orders_page.result_table(element='general:table')
        self.assertEqual(1, len(table_records) - 1)
        self.info('go to archived orders')
        self.orders_page.get_archived_items()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        self.assertEqual(len(self.order_page.result_table()) - 1, 0)
        for i in range(0, len(analysis_no) - 1):
            self.base_selenium.refresh()
            self.orders_page.get_archived_items()
            self.orders_page.filter_by_analysis_number(filter_text=analysis_no[i])
            self.assertEqual(len(self.order_page.result_table()) - 1, 0)

    @parameterized.expand(['True', 'False'])
    # @skip('https://modeso.atlassian.net/browse/LIMSA-267')
    def test015_order_search(self, small_letters):
        """
        New: Orders: Search Approach: User can search by any field & each field should display with yellow color

        LIMS-3492
        LIMS-3061
        """
        response, payload = self.orders_api.get_all_orders(limit=5)
        self.assertEqual(response['status'], 1)
        random_order = random.choice(response['orders'])
        self.info('{}'.format(random_order['orderNo']))
        rows = self.orders_page.search(random_order['orderNo'])[0]
        row_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows)
        for column in row_data:
            search_by = row_data[column].split(',')[0]
            if re.findall(r'\d{1,}.\d{1,}.\d{4}', row_data[column]) or row_data[column] == '' \
                    or column == 'Time Difference' or row_data[column] == '-':
                continue
            elif column == 'Analysis Results':
                search_by = row_data[column].split(' (')[0]

            row_data[column] = row_data[column].split(',')[0]
            self.info('search for {} : {}'.format(column, row_data[column]))
            if small_letters == 'True':
                search_results = self.order_page.search(search_by)
            else:
                search_results = self.order_page.search(search_by.upper())

            self.assertGreater(
                len(search_results), 1, " * There is no search results for it, Report a bug.")
            for search_result in search_results:
                search_data = self.base_selenium.get_row_cells_dict_related_to_header(
                    search_result)
                if search_data[column].replace("'", '').split(',')[0] == \
                        row_data[column].replace("'", '').split(',')[0]:
                    break
            self.assertEqual(row_data[column].replace("'", '').split(',')[0],
                             search_data[column].replace("'", '').split(',')[0])

    @parameterized.expand(['2020', '20'])
    def test016_search_by_year(self, search_text):
        """
        Search: Orders: Make sure that you can search by all the year format
        ( with year in case year after or before & without year )

        LIMS-7427
        """
        self.order_page.filter_by_order_no(search_text)
        results = self.orders_page.result_table()
        orders = [item.text.split('\n')[0] for item in results if item.text.split('\n')[0] != '']
        self.assertTrue(orders)
        for order in orders:
            self.assertIn(search_text, order.replace("'", ""))

    def test017_filter_configuration_fields(self):
        """
          Orders: Make sure that user can filter order TestUnit that exist
          on order only(TestUnit in Analysis not Included)

          LIMS-5379

          Orders: Filter Approach: Make sure that the user can filter from the
          default filter ( with status & dynamic fields )

          LIMS-5486
        """
        self.info("open filter menu")
        self.orders_page.open_filter_menu()
        self.info("open filter configuration")
        found_fields = self.orders_page.list_filter_feilds()
        self.info("fields in filter are {}".format(found_fields))
        required_fields = ['Analysis Results', 'Test Units', 'Material Type', 'Analysis No.',
                           'Departments', 'Test Plans', 'Changed By', 'Created On', 'Shipment Date',
                           'Test Date', 'Contact Name', 'Article Name', 'Order No.',
                           'Forwarding', 'Status']

        self.assertGreaterEqual(len(found_fields), len(required_fields))
        for field in required_fields:
            self.assertIn(field, found_fields)

    @parameterized.expand(['materialType', 'article', 'testPlans', 'testUnit'])
    def test018_filter_by_any_fields(self, key):
        """
        New: Orders: Filter Approach: I can filter by any field in the table view

        LIMS-3495
        """
        self.info('select random order using api')
        response, payload = self.orders_api.create_new_order()
        filter_dict = self.order_page.order_filters_element(key=key, payload=payload[0])
        self.info('filter by {} with value {}'.format(key, filter_dict[key]['value']))
        self.orders_page.apply_filter_scenario(
            filter_element=filter_dict[key]['element'],
            filter_text=filter_dict[key]['value'],
            field_type=filter_dict[key]['type'])
        self.base_selenium.scroll()
        self.orders_page.close_filter_menu()
        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for i in range(len(results) - 1):
            results = self.order_page.result_table()
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if filter_dict[key]['value'] in suborder[filter_dict[key]['result_key']].split(',\n'):
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.close_child_table(source=results[i])

    def test019_filter_by_analysis_no(self):
        """
        New: Orders: Filter Approach: I can filter by analysis No

        LIMS-3495
        """
        self.info('select random order using api')
        random_order = random.choice(self.orders_api.get_all_orders_json())
        analysis_no = self.orders_api.get_suborder_by_order_id(random_order['orderId'])[0]['orders'][0]['analysis'][0]
        filter_element = self.order_page.order_filters_element(key='analysis')
        self.info('filter by analysis No {}'.format(analysis_no))
        self.orders_page.filter_by_analysis_number(analysis_no)
        self.base_selenium.scroll()
        self.orders_page.close_filter_menu()
        self.assertEqual(len(self.order_page.result_table()), 2)
        self.orders_page.sleep_tiny()
        suborders = self.orders_page.get_child_table_data()
        key_found = False
        for suborder in suborders:
            if analysis_no == suborder[filter_element['result_key']].replace("'", ""):
                key_found = True
                break
        self.assertTrue(key_found)

    def test020_filter_by_order_No(self):
        """
        I can filter by any order No.

        LIMS-3495

        Filter: Order number format: In case the order number displayed with full year, I can filter by it

        LIMS-7426
        """
        self.info('select random order using api')
        orders, _ = self.orders_api.get_all_orders()
        order = random.choice(orders['orders'])
        self.assertIn('-2020', order['orderNo'], 'selected order with format {}'.format(order['orderNo']))
        self.info('filter by order No. {}'.format(order['orderNo']))
        self.orders_page.filter_by_order_no(order['orderNo'])
        result_order = self.orders_page.result_table()
        self.assertEqual(len(self.order_page.result_table())-1, 1)
        order_data = self.orders_page.get_the_latest_row_data()
        self.assertIn(order['orderNo'], order_data['Order No.'].replace("'", ""))
        self.assertIn('-2020', result_order[0].text.replace("'", ""))

    def test021_filter_by_status(self):
        """
        I can filter by status

        LIMS-3495
        """
        self.info("filter by status: Open")
        self.orders_page.apply_filter_scenario(filter_element='orders:status_filter',
                                               filter_text='Open', field_type='drop_down')

        self.info('get random suborder from result table to check that filter works')
        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        suborders = self.orders_page.get_child_table_data(index=randint(0, len(results) - 1))
        filter_key_found = False
        for suborder in suborders:
            if suborder['Status'] == 'Open':
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)

    def test022_filter_by_analysis_result(self):
        """
        I can filter by Analysis result

        LIMS-3495
        """
        self.info("filter by analysis_result: Conform")
        self.orders_page.apply_filter_scenario(filter_element='orders:analysis_result_filter',
                                               filter_text='Not Recieved', field_type='drop_down')
        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        self.info('get random suborder from result table to check that filter works')
        suborders = self.orders_page.get_child_table_data(index=randint(0, len(results) - 1))
        filter_key_found = False
        for suborder in suborders:
            if suborder['Analysis Results'].split(' (')[0] == 'Not Recieved':
                filter_key_found = True
                break

        self.assertTrue(filter_key_found)

    def test023_filter_by_contact(self):
        """
        New: Orders: Filter Approach: I can filter by contact

        LIMS-3495
        """
        self.info('get contact of random order')
        contact = self.orders_api.get_random_contact_in_order()
        self.info('filter by contact {}'.format(contact))
        self.orders_page.apply_filter_scenario(filter_element='orders:contact_filter',
                                               filter_text=contact, field_type='drop_down')
        self.orders_page.sleep_tiny()
        results = self.orders_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for result in results:
            if result.text:
                self.assertIn(contact, result.text)

    def test024_filter_by_department(self):
        """
        I can filter by department

        LIMS-3495
        """
        self.info('get create order with department')
        api, payload = self.orders_api.create_order_with_department()
        self.assertEqual(api['status'], 1)
        department = payload[0]['departments'][0]['text']
        self.info('filter by department value {}'.format(department))
        self.orders_page.apply_filter_scenario(filter_element='orders:departments_filter',
                                               filter_text=department, field_type='text')

        results = self.order_page.result_table()
        self.assertGreater(len(results), 1)
        for i in range(len(results) - 1):
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if department in suborder['Departments'].split(',\n'):
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.open_child_table(source=results[i])

    @parameterized.expand(['testDate', 'shipmentDate', 'createdAt'])
    # @skip("https://modeso.atlassian.net/browse/LIMSA-279")
    def test025_filter_by_date(self, key):
        """
         I can filter by testDate, shipmentDate, or createdAt fields

         LIMS-3495
        """
        orders, _ = self.orders_api.get_all_orders(limit=20)
        order = random.choice(orders['orders'])
        suborder, _ = self.orders_api.get_suborder_by_order_id(id=order['id'])
        date_list = suborder['orders'][0][key].split('T')[0].split('-')
        date_list.reverse()
        filter_value = "{}.{}.{}".format(date_list[0], date_list[1], date_list[2])
        filter_element = self.order_page.order_filters_element(key=key)
        self.orders_page.filter_by_date(first_filter_element=filter_element['element'][0],
                                        first_filter_text=filter_value,
                                        second_filter_element=filter_element['element'][1],
                                        second_filter_text=filter_value)
        self.assertGreater(len(self.order_page.result_table()), 1)
        suborders = self.orders_page.get_child_table_data()
        filter_key_found = False
        for suborder in suborders:
            if suborder[filter_element['result_key']] == filter_value:
                filter_key_found = True
                break
        self.assertTrue(filter_key_found)

    @attr(series=True)
    def test026_filter_by_changed_by(self):
        """
        New: Orders: Filter Approach: I can filter by changed by

        LIMS-3495
        """
        response, contact = self.contacts_api.create_contact()
        self.assertEqual(response['status'], 1)
        contact_list = [contact['name']]
        testplan = TestPlanAPI().create_completed_testplan_random_data()
        self.login_page = Login()
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.orders_page.sleep_tiny()
        self.login_page.logout()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.info("Navigate to orders page and create new order")
        self.orders_page.get_orders_page()
        self.orders_page.sleep_small()
        order_no = SubOrders().create_new_order(contacts=contact_list,
                                                material_type=testplan['materialType'][0]['text'],
                                                article=testplan['selectedArticles'][0]['text'],
                                                test_plans=[testplan['testPlan']['text']])
        self.orders_page.sleep_tiny()
        self.orders_page.get_orders_page()
        self.orders_page.sleep_small()
        self.info('filter by with user {}'.format(payload['username']))
        self.orders_page.apply_filter_scenario(
            filter_element='orders:changed_by',
            filter_text=payload['username'])

        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for i in range(len(results) - 1):
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if payload['username'] == suborder['Changed By']:
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.close_child_table(source=results[i])

    @skip("https://modeso.atlassian.net/browse/LIMSA-205")
    def test064_download_suborder_sheet_for_single_order(self):
        """
        Export order child table

        LIMS-8085- single order case
        """
        self.info('select random order')
        random_row = self.orders_page.get_random_table_row(table_element='general:table')
        self.orders_page.click_check_box(source=random_row)
        random_row_data = self.base_selenium.get_row_cells_dict_related_to_header(random_row)
        self.orders_page.open_child_table(source=random_row)
        child_table_data = self.order_page.get_table_data()
        order_data_list = []
        order_dict = {}
        for sub_order in child_table_data:
            order_dict.update(random_row_data)
            order_dict.update(sub_order)
            order_data_list.append(order_dict)
            order_dict = {}

        #formatted_orders = self.orders_page.match_format_to_sheet_format(order_data_list)
        self.order_page.download_xslx_sheet()
        for index in range(len(formatted_orders)):
            self.info('Comparing the order no {} '.format(formatted_orders[index][0]))
            values = self.order_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.reformat_data(values)
            self.assertCountEqual(fixed_sheet_row_data, formatted_orders[index],
                                  f"{str(fixed_sheet_row_data)} : {str(formatted_orders[index])}")
            for item in formatted_orders[index]:
                self.assertIn(item, fixed_sheet_row_data)

    @skip('need to be re-implemented to include child table data')
    def test065_export_order_sheet(self):
        """
        New: Orders: XSLX Approach: user can download all data in table view with the same order with table view

        LIMS-3274
        """
        self.info(' * Download XSLX sheet')
        self.order_page.select_all_records()
        self.order_page.download_xslx_sheet()
        rows_data = self.order_page.get_table_rows_data()
        for index in range(len(rows_data) - 1):
            self.info(
                ' * Comparing the order no. {} '.format(index + 1))
            fixed_row_data = self.fix_data_format(rows_data[index].split('\n'))
            values = self.order_page.sheet.iloc[index].values
            fixed_sheet_row_data = self.fix_data_format(values)
            for item in fixed_row_data:
                if item != " ":
                    self.assertIn(item, fixed_sheet_row_data)

    def test099_year_format_in_suborder_sheet(self):
        """
         Analysis number format: In case the analysis number displayed with full year,
         this should reflect on the export file

         LIMS-7424

         Order number format: In case the order number displayed with full year,
         this should reflect on the export file

         LIMS-7423
        """
        self.info('select random order')
        order = random.choice(self.orders_api.get_all_orders_json())
        order_no = order['orderNo']
        self.assertIn('-2020', order_no)
        response, _ = self.orders_api.get_suborder_by_order_id(order['orderId'])
        self.assertEqual(response['status'], 1)
        analysis_no = response['orders'][0]['analysis'][0]
        self.assertIn('-2020', analysis_no)
        self.orders_page.filter_by_order_no(order_no)
        row = self.orders_page.result_table()[0]
        self.assertTrue(row)
        self.orders_page.click_check_box(source=row)
        self.order_page.download_xslx_sheet()
        self.info('Comparing the downloaded  order ')
        values = self.order_page.sheet.iloc[0].values
        fixed_sheet_row_data = self.reformat_data(values)
        self.assertIn(order_no, fixed_sheet_row_data)
        self.assertIn(analysis_no, fixed_sheet_row_data)

    def test066_create_order_then_overview(self):
        """
        Orders: Create: In case of clicking on the overview button after clicking create new order
        check it redirects to the active table

        LIMS-6204
        """
        self.order_page.click_create_order_button()
        self.order_page.sleep_tiny()
        self.order_page.click_overview()
        self.info('asserting correct redirection to orders active table ')
        self.info('Active table url is {} , current url is {}'.format(
            self.orders_page.orders_url, self.base_selenium.get_url()))
        self.assertEqual(self.orders_page.orders_url, self.base_selenium.get_url())

    @parameterized.expand(['update_a_field', 'no_updates'])
    def test104_edit_order_page_then_overview(self, edit_case):
        """
        Orders: Popup should appear when editing then clicking on overview without saving <All data will be lost>
        LIMS-6814

        Orders: No popup should appear when clicking on overview without changing anything
        LIMS-6821
        """
        random_order = random.choice(self.orders_api.get_all_orders_json())
        self.info('edit order with No {}'.format(random_order['orderNo']))
        self.order_page.filter_by_order_no(random_order['orderNo'])
        row = self.orders_page.result_table()[0]
        self.order_page.open_edit_page(row=row)
        if edit_case == 'update_a_field':
            self.info('update the contact field')
            self.order_page.set_contacts(remove_old=True)
        self.order_page.click_overview()
        if edit_case == 'update_a_field':
            self.assertIn('All data will be lost', self.order_page.get_confirmation_pop_up_text())
            self.assertTrue(self.order_page.confirm_popup(check_only=True))
        else:
            self.assertFalse(self.order_page.confirm_popup(check_only=True))
            self.info('asserting redirection to active table')
            self.assertEqual(self.order_page.orders_url, self.base_selenium.get_url())

    @parameterized.expand(['10', '20', '25', '50', '100'])
    @attr(series=True)
    def test067_testing_table_pagination(self, pagination_limit):
        """
        Orders: Active table: Pagination Approach; Make sure that I can set the pagination
        to display 10/20/25/50/100 records in each page

        LIMS-6199
        """
        self.order_page.set_page_limit(limit=pagination_limit)
        table_info = self.order_page.get_table_info_data()
        self.info('get current table records count')
        table_records_count = str(len(self.order_page.result_table()) - 1)

        self.info('table records count is {}, and it should be {}'.
                  format(table_records_count, table_info['page_limit']))
        self.assertEqual(table_records_count, table_info['page_limit'])

        self.info('current page limit is {}, and it should be {}'.
                  format(table_info['pagination_limit'], pagination_limit))
        self.assertEqual(table_info['pagination_limit'], pagination_limit)

        if int(table_info['pagination_limit']) <= int((table_info['count']).replace(",", "")):
            self.assertEqual(table_info['pagination_limit'], table_records_count)