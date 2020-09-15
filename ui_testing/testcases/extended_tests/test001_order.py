from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.order_page import Order
from ui_testing.pages.orders_page import Orders
from ui_testing.pages.header_page import Header
from api_testing.apis.orders_api import OrdersAPI
from ui_testing.pages.analysis_page import AllAnalysesPage
from api_testing.apis.test_unit_api import TestUnitAPI
from api_testing.apis.contacts_api import ContactsAPI
from api_testing.apis.test_plan_api import TestPlanAPI
from api_testing.apis.general_utilities_api import GeneralUtilitiesAPI
from api_testing.apis.base_api import BaseAPI
import random
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
        self.info('go to Modules Configurations')
        self.header_page.get_modules_config_page()
        self.header_page.disable_article_option()
        self.header_page.sleep_tiny()
        self.order_page.get_orders_page()

    def tearDown(self):
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
            test_units=[created_testunit[1]['name']], with_article=False, check_testunits_testplans=True)

        self.info('asserting article field is not displayed in new order page')
        fields = self.base_selenium.get_table_head_elements(element='order:suborder_table')
        fields_text = [f.text for f in fields]
        self.assertNotIn('Article: *', fields_text)
        self.info('asserting All displayed testunits are loaded correctly according to '
                  'selected material type {}'.format(formatted_material['text']))
        testunit_materials = []
        for testunit in testunits:
            testunit_info = self.test_unit_api.get_testunit_with_quicksearch(quickSearchText=testunit)
            if testunit_info is not None:
                for tu in testunit_info:
                    testunit_materials.append(tu['materialTypes'][0])
                self.assertTrue(any(material in ['All', formatted_material['text']] for material in testunit_materials))

        self.info('asserting All displayed testplans are loaded correctly according to '
                  'selected material type {}'.format(formatted_material['text']))
        testplan_materials = []
        for testplan in testplans:
            testplan_info = self.test_plan_api.get_testplan_with_quicksearch(quickSearchText=testplan)
            if testplan_info is not None:
                for tp in testplan_info:
                    testplan_materials.append(tp['materialTypes'][0])
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
        self.info('create order from an existing one')
        order_no = self.order_page.create_existing_order_with_auto_fill()
        self.assertFalse(self.base_selenium.check_element_is_exist(element='order:article'))
        old_materialtype = self.order_page.get_material_type()
        material_type = random.choice(GeneralUtilitiesAPI().
                                      get_material_types_without_duplicate(old_materialtype))
        self.info('switch to material type {}'.format(material_type))
        self.order_page.set_material_type(material_type=material_type)
        self.assertEqual(self.base_selenium.get_value(element='order:test_unit'), None)
        self.assertEqual(self.base_selenium.get_value(element='order:test_plan'), None)
        testunits = self.base_selenium.get_drop_down_suggestion_list(element='order:test_unit',
                                                                     item_text=' ')
        testplans = self.base_selenium.get_drop_down_suggestion_list(element='order:test_plan',
                                                                     item_text=' ')
        testplan_materials = []
        testunit_materials = []
        for testunit in testunits:
            testunit_info = self.test_unit_api.get_testunit_with_quicksearch(quickSearchText=testunit)
            if testunit_info is not None:
                for tu in testunit_info:
                    testunit_materials.append(tu['materialTypes'][0])
                self.assertTrue(any(material in ['All', material_type] for material in testunit_materials))

        self.info(
            'asserting All displayed testplans are loaded correctly according to selected material type {}'.format(
                material_type))
        for testplan in testplans:
            if testplan is not None:
                testplan_info = TestPlanAPI().get_testplan_with_quicksearch(quickSearchText=testplan)
                if len(testplan_info) != 0:
                    for tp in testplan_info:
                        testplan_materials.append(tp['materialTypes'][0])
                    self.assertTrue(any(material in ['All', material_type] for material in testplan_materials))

        self.order_page.set_test_unit()
        self.order_page.set_test_plan()
        self.order_page.save(save_btn='order:save_btn')
        self.info('assert order is created successfully')
        self.orders_page.get_orders_page()
        self.orders_page.filter_by_order_no(filter_text=order_no)
        results = self.order_page.result_table()[0].text
        self.assertIn(order_no.replace("'", ""), results.replace("'", ""))