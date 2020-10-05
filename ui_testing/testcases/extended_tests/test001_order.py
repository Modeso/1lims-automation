from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from ui_testing.pages.header_page import Header
from ui_testing.pages.login_page import Login
from api_testing.apis.orders_api import OrdersAPI
from ui_testing.pages.analysis_page import AllAnalysesPage
from ui_testing.pages.analysis_page import SingleAnalysisPage
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from ui_testing.pages.my_profile_page import MyProfile
from api_testing.apis.users_api import UsersAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from api_testing.apis.base_api import BaseAPI
from parameterized import parameterized
from datetime import date
from nose.plugins.attrib import attr


class OrdersWithoutArticleTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.contacts_api = ContactsAPI()
        self.test_unit_api = TestUnitAPI()
        self.test_plan_api = TestPlanAPI()
        self.general_utilities = GeneralUtilitiesAPI()
        self.set_authorization(auth=BaseAPI().AUTHORIZATION_RESPONSE)
        self.test_unit_api.set_name_configuration_name_only()
        self.orders_api.set_configuration()
        self.header_page = Header()
        article_enabled = self.general_utilities.is_article_enabled()
        if article_enabled:
            self.info('go to Modules Configurations')
            self.header_page.get_modules_config_page()
            self.header_page.disable_article_option()
        self.header_page.sleep_tiny()
        self.order_page.get_orders_page()

    def tearDown(self):
        article_enabled = self.general_utilities.is_article_enabled()
        if not article_enabled:
            self.header_page.get_modules_config_page()
            self.header_page.disable_article_option()
        return super().tearDown()

    @attr(series=True)
    def test001_create_order_without_article(self):
        """
        orders without articles: check that user can create order without article

        LIMS-3253
        """
        created_testplan = TestPlanAPI().create_completed_testplan_random_data()
        self.assertTrue(created_testplan)
        formatted_material = created_testplan['materialType'][0]
        created_testunit = self.test_unit_api.create_qualitative_testunit(selectedMaterialTypes=[formatted_material])
        self.info('asserting article is not found in orders active table configuration')
        child_table_header = self.orders_page.navigate_to_child_table_configuration()
        self.assertNotIn('Article Name', child_table_header)
        self.orders_page.open_child_table(self.orders_page.result_table()[0])
        header_row = self.base_selenium.get_table_head_elements(element='general:table_child')
        displayed_headers = [h.text for h in header_row]
        self.info('asserting article is not displayed in orders table')
        self.assertNotIn('Article Name', displayed_headers)
        order_no, testunits, testplans = self.order_page.create_new_order(
            material_type=formatted_material['text'], test_plans=[created_testplan['testPlan']['text']],
            test_units=[created_testunit[1]['name']], article=None, check_testunits_testplans=True)

        self.info('asserting article field is not displayed in new order page')
        fields = self.base_selenium.get_table_head_elements(element='order:suborder_table')
        fields_text = [f.text for f in fields]
        self.assertNotIn('Article: *', fields_text)

        self.info('asserting All displayed testunits are loaded correctly according to '
                  'selected material type {}'.format(formatted_material['text']))
        testunit_materials = self.test_unit_api.get_testunits_material_types(testunits)
        self.assertTrue(any(material in ['All', formatted_material['text']] for material in testunit_materials))

        self.info('asserting All displayed testplans are loaded correctly according to '
                  'selected material type {}'.format(formatted_material['text']))
        testplan_materials = self.test_plan_api.get_testplans_material_types(testplans)
        self.assertTrue(any(material in ['All', formatted_material['text']] for material in testplan_materials))

        self.order_page.sleep_tiny()
        self.order_page.get_orders_page()
        self.order_page.sleep_tiny()
        self.order_page.filter_by_order_no(filter_text=order_no)
        latest_order_data = \
            self.base_selenium.get_row_cells_dict_related_to_header(row=self.order_page.result_table()[0])
        self.info('asserting the order is successfully created')
        self.assertEqual(order_no.replace("'", ""), latest_order_data['Order No.'].replace("'", ""))

    @attr(series=True)
    def test002_create__order_from_existing_order_without_article(self):
        """
         Orders without articles: when creating a new order from existing order,
         all data should be loaded, without article

         LIMS-3254
        """
        created_testplan = TestPlanAPI().create_completed_testplan_random_data()
        self.assertTrue(created_testplan)
        formatted_material = created_testplan['materialType'][0]
        created_testunit = self.test_unit_api.create_qualitative_testunit(selectedMaterialTypes=[formatted_material])
        material_type = formatted_material['text']
        self.info('create order from an existing one')
        self.orders_page.sleep_tiny()
        order_no = self.order_page.create_existing_order_with_auto_fill()
        self.assertFalse(self.base_selenium.check_element_is_exist(element='order:article'))
        self.info('switch to material type {}'.format(material_type))
        self.order_page.set_material_type(material_type=material_type)
        self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)
        self.assertEqual(self.base_selenium.get_value(element='order:test_plan'), None)
        testunits = self.base_selenium.get_drop_down_suggestion_list(element='order:test_unit',
                                                                     item_text=' ')
        testplans = self.base_selenium.get_drop_down_suggestion_list(element='order:test_plan',
                                                                     item_text=' ')

        self.info('asserting All displayed testunits are loaded correctly according to '
                  'selected material type {}'.format(material_type))
        testunit_materials = self.test_unit_api.get_testunits_material_types(testunits)
        self.assertTrue(any(material in ['All', material_type] for material in testunit_materials))

        self.info('asserting All displayed testplans are loaded correctly according to '
                  'selected material type {}'.format(material_type))
        testplan_materials = self.test_plan_api.get_testplans_material_types(testplans)
        self.assertTrue(any(material in ['All', material_type] for material in testplan_materials))

        self.order_page.set_test_unit(created_testunit[1]['name'])
        self.order_page.set_test_plan(created_testplan['testPlan']['text'])
        self.order_page.save(save_btn='order:save_btn')
        self.info('assert order is created successfully')
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        results = self.order_page.result_table()[0].text
        self.assertIn(order_no.replace("'", ""), results.replace("'", ""))


class OrdersExtendedTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.order_page = Order()
        self.orders_api = OrdersAPI()
        self.orders_page = Orders()
        self.analyses_page = AllAnalysesPage()
        self.contacts_api = ContactsAPI()
        self.test_unit_api = TestUnitAPI()
        self.test_plan_api = TestPlanAPI()
        self.general_utilities = GeneralUtilitiesAPI()
        self.header_page = Header()
        self.my_profile_page = MyProfile()
        self.set_authorization(auth=BaseAPI().AUTHORIZATION_RESPONSE)
        self.test_unit_api.set_name_configuration_name_only()
        self.orders_api.set_configuration()
        self.order_page.get_orders_page()
        self.selected_language = 'EN'

    def tearDown(self):
        if self.selected_language == 'DE':
            self.my_profile_page.get_my_profile_page()
            self.my_profile_page.chang_lang(lang='EN')
        return super().tearDown()

    @parameterized.expand(['EN', 'DE'])
    @attr(series=True)
    def test003_new_fields_are_displayed_in_order_child_table(self, lang):
        """
        Orders : child table: check that new fields of "Forwarding" , "Report sent by", "validation date" and
        "validation by"have been added to order's child table in both EN and DE

        LIMS-7714
        LIMS-7715
        """
        if lang == 'EN':
            required_headers = ['Forwarding', 'Report sent by', 'Validation by', 'Validation date']
        else:
            self.selected_language = 'DE'
            self.my_profile_page.get_my_profile_page()
            self.my_profile_page.chang_lang(lang='DE')
            self.orders_page.get_orders_page()
            required_headers = ['Versand', 'Bericht Versand duch', 'Probenfreigabe Datum', 'Probenfreigabe durch']

        self.orders_page.open_child_table(self.orders_page.result_table()[0])
        header_row = self.base_selenium.get_table_head_elements(element='general:table_child')
        displayed_child_headers = [h.text for h in header_row]
        displayed_Configuration_headers = self.orders_page.navigate_to_child_table_configuration()
        for header in required_headers:
            self.info('asserting {} is displayed '.format(header))
            self.assertIn(header, displayed_child_headers)
            self.assertIn(header, displayed_Configuration_headers)

    @attr(series=True)
    def test004_check_validation_date_validation_by(self):
        """
         Orders: Validation date & Validation by : check that when user update the validation date &
         the validation by, the update should reflect on order's child table

         LIMS-7729
        """
        today = date.today()
        current_date = today.strftime("%d.%m.%Y")
        self.info('Calling the users api to create a new user with username')
        response, payload = UsersAPI().create_new_user()
        self.assertEqual(response['status'], 1, payload)
        self.single_analysis_page = SingleAnalysisPage()
        self.login_page = Login()
        self.info("create new order and update its validation option to be conform")
        order_response, order_payload = self.orders_api.create_new_order()
        self.assertEqual(order_response['status'], 1, order_payload)
        order_no = order_payload[0]['orderNo']
        self.info('edit order with No {}'.format(order_no))
        self.orders_page.get_order_edit_page_by_id(order_response['order']['mainOrderId'])
        self.order_page.sleep_small()
        self.info('navigate to analysis tab')
        self.order_page.navigate_to_analysis_tab()
        self.single_analysis_page.set_testunit_values()
        self.info('change validation options to conform')
        self.single_analysis_page.change_validation_options(text='Conform')
        self.order_page.get_orders_page()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        suborders_data = self.order_page.get_child_table_data(index=0)
        self.info('assert validation by is set correctly')
        self.assertEqual(suborders_data[0]['Validation by'], self.base_selenium.username)
        self.assertEqual(suborders_data[0]['Validation date'], current_date)
        self.info('go to analysis table and assert validation by and validation options'
                  ' are set correctly as in order active table')
        self.orders_page.navigate_to_analysis_active_table()
        self.analyses_page.filter_by_analysis_number(suborders_data[0]['Analysis No.'])
        analysis_data = self.analyses_page.get_the_latest_row_data()
        self.assertEqual(suborders_data[0]['Validation by'], analysis_data['Validation by'])
        self.assertEqual(suborders_data[0]['Validation date'], analysis_data['Validation date'])
        self.info("Logout then login again using new user {}".format(payload['username']))
        self.login_page.logout()
        self.login_page.login(username=payload['username'], password=payload['password'])
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.orders_page.get_order_edit_page_by_id(order_response['order']['mainOrderId'])
        self.info('change validation options so validation by is changed to {}', payload['username'])
        self.order_page.navigate_to_analysis_tab()
        self.single_analysis_page.change_validation_options(text='Approved')
        self.orders_page.get_orders_page()
        self.orders_page.navigate_to_order_active_table()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        suborders_after = self.order_page.get_child_table_data(index=0)
        self.assertEqual(suborders_after[0]['Validation by'], payload['username'])
        self.assertEqual(suborders_after[0]['Validation date'], current_date)

    @attr(series=True)
    def test075_enter_long_method_should_be_in_multiple_lines_in_order_form(self):
        """
        In case you select the method to display and you entered long text in it,
        the method should display into multiple lines in the order form

        LIMS-6663
        """
        self.test_units_page = TstUnits()
        self.orders_page.sleep_tiny()
        self.test_units_page.get_test_units_page()
        self.orders_page.sleep_tiny()
        self.test_units_page.open_configurations()
        self.orders_page.sleep_tiny()
        self.test_units_page.open_testunit_name_configurations_options()
        self.test_units_page.select_option_to_view_search_with(view_search_options=['Method'])
        self.info(' create test unit with long method text ')
        api, payload = TestUnitAPI().create_test_unit_with_long_text()
        self.assertEqual(api['status'], 1, payload)
        self.info('go to orders page')
        self.order_page.get_orders_page()
        self.info('create new order with the test unit of long method text')
        self.suborder_table.create_new_order(save=False, material_type='Raw Material')
        self.suborder_table.set_test_units(test_units=[payload['method']], remove_old=True)
        self.orders_page.save(save_btn='order:save_btn')
        self.info('assert method text appears in multiple lines')
        self.order_page.get_table_with_add()
        multiple_lines_properties = self.suborder_table.get_testunit_multiple_line_properties()
        self.assertEquals(multiple_lines_properties['textOverflow'], 'clip')
        self.assertEquals(multiple_lines_properties['lineBreak'], 'auto')

    @attr(series=True)
    @parameterized.expand(['Name', 'Method', 'Unit', 'No'])
    def test076_search_with_test_unit_name_method(self, search_by):
        """
        Orders:Test unit search approach
        allow user to search with test unit name in the drop down list of the order form
        LIMS-6664
        allow user to search with test unit method in the drop down list of order form
        LIMS-6666
        allow user to search with test unit type in the drop down list of order form
        LIMS-6668
        allow user to search with test unit number in the drop down list of order form
        LIMS-6665

        """
        self.test_units_page = TstUnits()
        response, payload = TestUnitAPI().create_quantitative_testunit(unit="RandomUnit")
        self.assertEqual(response['status'], 1)
        self.test_units_page.get_test_units_page()
        self.orders_page.sleep_tiny()
        self.test_units_page.open_configurations()
        self.orders_page.sleep_tiny()
        self.test_units_page.open_testunit_name_configurations_options()
        self.test_units_page.select_option_to_view_search_with(view_search_options=[search_by])
        self.order_page.get_orders_page()

        if search_by == 'Name':
            testunit_search = payload['name']
        elif search_by == 'Method':
            testunit_search = payload['method']
        elif search_by == 'Unit':
            testunit_search = payload['unit']
        elif search_by == 'No':
            testunit_search = str(payload['number'])

        testunits = self.suborder_table.create_new_order_get_test_unit_suggetion_list(test_unit_name=testunit_search)

        self.info('checking {} field only is displayed'.format(search_by))
        self.assertGreater(len(testunits), 0)

    @parameterized.expand(['Quantitative', 'Qualitative', 'Quantitative MiBi'])
    @attr(series=True)
    def test077_test_unit_with_sub_and_super_unit_name_appears_in_unit_field_drop_down(self, type):
        """
        New: Test unit: Export: In case the unit field with sub & super,
        allow this to display in the unit field drop down list in the analysis form

        LIMS-6675
        """
        self.test_unit_api = TestUnitAPI()
        self.test_unit_api.set_name_configuration()
        if type == 'Quantitative':
            self.info('Create new Quantitative testunit')
            response, payload = self.test_unit_api.create_quantitative_testunit(unit='m[g]{o}')
        elif type == 'Qualitative':
            self.info('Create new Qualitative testunit')
            response, payload = self.test_unit_api.create_qualitative_testunit(unit='m[g]{o}')
        else:
            self.info('Create new Quantitative MiBi testunit')
            response, payload = self.test_unit_api.create_mibi_testunit(unit='m[g]{o}')

        self.assertEqual(response['status'], 1, 'test unit not created {}'.format(payload))
        self.info('go to orders page')
        self.order_page.get_orders_page()
        unit = self.suborder_table.create_new_order_get_test_unit_suggetion_list(
            material_type='', test_unit_name='m[g]{o}')
        self.assertIn("m[g]{o}", unit)

    @parameterized.expand(['sub_script', 'super_script'])
    @attr(series=True)
    def test078_filter_testunit_by_scripts(self, value):
        """
         Make sure that user can filter by sub & super scripts in the filter drop down list

         LIMS-7447
         LIMS-7444
        """
        self.test_unit_api = TestUnitAPI()
        self.test_unit_api.set_name_configuration()
        if value == 'sub_script':
            api, testunit = self.test_unit_api.create_qualitative_testunit(unit='14[158]')
        else:
            api, testunit = self.test_unit_api.create_qualitative_testunit(unit='15{158}')
        self.assertEqual(api['status'], 1)
        unit = testunit['unit']
        self.orders_page.get_orders_page()
        self.order_page.sleep_small()
        self.base_selenium.scroll(False)
        self.orders_page.apply_filter_scenario(filter_element='orders:test_units_filter',
                                               filter_text=unit, field_type='drop_down')
        self.assertIsNotNone(
            self.base_selenium.is_text_included_in_drop_down_items(
                element='orders:test_units_filter', item_text=unit))

        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for i in range(len(results) - 1):
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if unit in suborder['Test Units']:
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.open_child_table(source=results[i])

    @parameterized.expand(['Name', 'No', 'Name:No'])
    @attr(series=True)
    def test095_change_contact_config(self, search_by):
        '''
         Orders: Contact configuration approach: In case the user
         configures the contact field to display name & number this action
         should reflect on the order active table
         LIMS-6632
        :param search_by:
        :return:
        '''
        self.contacts_page = Contacts()
        self.info('get random contact')
        contacts_response, _ = ContactsAPI().get_all_contacts(limit=10)
        self.assertEqual(contacts_response['status'], 1)
        payload = random.choice(contacts_response['contacts'])
        self.orders_page.open_order_config()
        self.info('change contact view by options')
        self.contacts_page.open_contact_configurations_options()
        if search_by == 'Name':
            search_text = payload['name']
            result = payload['name']
            search_by = [search_by]
        elif search_by == 'No':
            search_text = 'No: ' + str(payload['companyNo'])
            result = str(payload['companyNo'])
            search_by = [search_by]
        elif search_by == 'Name:No':
            search_text = payload['name'] + ' No: ' + str(payload['companyNo'])
            search_by = search_by.split(':')
            result = payload['name']

        self.contacts_page.select_option_to_view_search_with(view_search_options=search_by)
        self.info('go to order active table')
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_contact(filter_text=result)
        rows = self.orders_page.result_table()
        order_data = self.base_selenium.get_row_cells_dict_related_to_header(row=rows[0])
        self.info('assert contact appear in format {}'.format(search_by))
        self.assertEqual(order_data['Contact Name'], search_text)

    @parameterized.expand([('Name', 'Type'),
                           ('Unit', 'No'),
                           ('Quantification Limit', '')])
    @attr(series=True)
    def test097_test_unit_name_allow_user_to_filter_with_selected_two_options_order(self, search_view_option1,
                                                                                    search_view_option2):
        """
         Orders: Filter test unit Approach: Allow the search criteria in
         the drop down list in the filter section to be same as in the form

         LIMS-7411
        """
        self.test_units_page = TstUnits()
        self.test_units_page.get_test_units_page()
        self.test_units_page.open_configurations()
        self.test_units_page.open_testunit_name_configurations_options()
        self.test_units_page.select_option_to_view_search_with(
            view_search_options=[search_view_option1, search_view_option2])

        upperLimit = self.generate_random_number(lower=50, upper=100)
        lowerLimit = self.generate_random_number(lower=1, upper=49)
        self.info('Create new quantitative test unit with unit and quantification')
        response, payload = self.test_unit_api.create_quantitative_testunit(
            useSpec=False, useQuantification=True, quantificationUpperLimit=upperLimit,
            quantificationLowerLimit=lowerLimit, unit='m[g]{o}')
        self.assertEqual(response['status'], 1, payload)
        formated_tu, _ = TestUnitAPI().get_testunit_form_data(response['testUnit']['testUnitId'])
        test_unit = [{'id': formated_tu['testUnit']['id'], 'name': formated_tu['testUnit']['name']}]
        self.info('create new order created test unit number'.format(payload))
        res, order = self.orders_api.create_new_order(testUnits=test_unit)
        self.assertEqual(res['status'], 1, 'order not created with {}'.format(order))
        if search_view_option1 == 'Name' and search_view_option2 == 'Type':
            filter_text = payload['name']
        elif search_view_option1 == 'Unit' and search_view_option2 == 'No':
            filter_text = str(payload['number'])
        else:
            filter_text = str(payload['quantificationLowerLimit']) + '-' + str(payload['quantificationUpperLimit'])

        self.orders_page.get_orders_page()
        self.orders_page.sleep_tiny()
        self.orders_page.open_filter_menu()
        self.base_selenium.wait_element(element='orders:test_units_filter')
        self.orders_page.filter_by(filter_element='orders:test_units_filter', filter_text=filter_text)
        found_filter_text = self.base_selenium.get_text('orders:test_units_filter').replace("\n×", "")
        if search_view_option1 == 'Name' and search_view_option2 == 'Type':
            self.assertEqual(found_filter_text, payload['name'] + ': Quantitative')
        elif search_view_option1 == 'Unit' and search_view_option2 == 'No':
            self.assertEqual(found_filter_text, 'm[g]{o}: ' + str(payload['number']))
        else:
            self.assertEqual(found_filter_text, filter_text)

        self.orders_page.filter_apply()
        self.orders_page.sleep_tiny()
        results = self.order_page.result_table()
        self.assertGreaterEqual(len(results), 1)
        for i in range(len(results) - 1):
            suborders = self.orders_page.get_child_table_data(index=i)
            key_found = False
            for suborder in suborders:
                if payload['name'] == suborder['Test Units']:
                    key_found = True
                    break
            self.assertTrue(key_found)
            # close child table
            self.orders_page.close_child_table(source=results[i])



