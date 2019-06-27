from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.order_page import Order
from parameterized import parameterized



class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.order_page = Order()
        self.test_plan = TstPlan()
        self.article_page = Article()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.order_page.get_orders_page()

    @parameterized.expand(['save', 'cancel'])
    def test001_cancel_button_edit_no(self, save):
        """
        New: Orders: Save/Cancel button: After I edit no field then press on cancel button,
        a pop up will appear that the data will be

        LIMS-5241
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        current_no = self.order_page.get_no()
        new_no = self.generate_random_string()
        self.order_page.set_no(new_no)
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_no, self.order_page.get_no())
        else:
            self.assertEqual(current_no, self.order_page.get_no())

    @parameterized.expand(['save','cancel'])
    def test002_cancel_button_edit_no(self, save):
        """
        New: Orders: I can update the order number successfully ( from the order view ) & In case I have order number
        with year then updated it , the new number that updated should be add with year

        LIMS-4335
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        current_no = self.order_page.get_no()
        new_no = self.generate_random_string()
        self.order_page.set_no(new_no)
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.article_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_no, self.order_page.get_no())
        else:
            self.assertEqual(current_no, self.order_page.get_no())



    @parameterized.expand([ 'save' , 'cancel'])     #done with date 19/6
    def test003_cancel_button_edit_contact(self, save):
        """
        Orders: In case I update the article then press on cancel button, a pop up should display with ( ok & cancel )
        buttons and when I press on cancel button, this update shouldn't submit

        LIMS-4613
        LIMS-4613
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        self.order_page.sleep_tiny()
        current_contact = self.order_page.get_contact()
        self.order_page.set_contact()
        new_contact = self.order_page.get_contact()
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=5)

        if 'save' == save:
            self.assertEqual(new_contact, self.order_page.get_contact())
        else:
            self.assertEqual(current_contact, self.order_page.get_contact())

    @parameterized.expand(['save', 'cancel'])    # done with date 19/6
    def test004_cancel_button_edit_departments(self, save):
        """
        Orders: In case I update the article then press on cancel button, a pop up should display with ( ok & cancel )
        buttons and when I press on cancel button, this update shouldn't submit

        LIMS-4613
        LIMS-4613
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        self.order_page.sleep_tiny()
        current_departments = self.order_page.get_departments()
        self.order_page.set_departments()
        new_departments = self.order_page.get_departments()
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=5)

        if 'save' == save:
            self.assertEqual(new_departments, self.order_page.get_departments())
        else:
            self.assertEqual(current_departments, self.order_page.get_departments())

    @parameterized.expand(['save','cancel'])
    def test005_cancel_button_edit_test_date(self, save):
        """
        New: Article: Save/Cancel button: After I edit material_type then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        #self.order_page.sleep_tiny()
        current_test_date = self.order_page.get_test_date()
        self.order_page.set_test_date()
        new_test_date = self.order_page.get_test_date()
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_test_date, self.order_page.get_test_date())
        else:
            self.assertEqual(current_test_date, self.order_page.get_test_date())

    @parameterized.expand(['save','cancel'])
    def test006_cancel_button_edit_shipment_date(self, save):
        """
        New: In case I delete the shipment date then press on save button, the action submitted successfully
        ( The shipment date deleted successfully because it is optional field )
        LIMS-3586
        LIMS-3576
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        self.order_page.sleep_tiny()
        current_shipment_date = self.order_page.get_shipment_date()
        self.order_page.set_shipment_date()
        new_shipment_date = self.order_page.get_shipment_date()
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_shipment_date, self.order_page.get_shipment_date())
        else:
            self.assertEqual(current_shipment_date, self.order_page.get_shipment_date())


    def test007_create_order_with_test_plan(self):
        """
                New: Articles: Creation Approach: I can create order with test plan successfully

                LIMS-3575
                :return:
                """
        self_order_page.create_new_order(order='', order_no='', materail_type='Raw Material', article='test', contact='contact', test_plan='', test_date='')

    def test008_create_order_with_test_plan(self):
        """
        New: Articles: Creation Approach: I can create order with test plan successfully

        LIMS-3575
        :return:
        """
        self.article_page.create_new_article(full_options=True, material_type='Raw Material')
        article_text = self.article_page.search(value=self.article_page.article_name)[0].text
        self.assertIn(self.article_page.article_unit, article_text)
        self.assertIn(self.article_page.article_comment, article_text)
        self.assertIn(self.article_page.article_material_type, article_text)


    @parameterized.expand(['save', 'cancel'])
    def test008_cancel_button_edit_shipment_date(self, save):
        """
        New: Article: Save/Cancel button: After I edit comment then press on cancel button,
        a pop up will appear that the data will be

        LIMS-3586
        LIMS-3576
        :return:
        """
        self.order_page.get_random_orders()
        order_url = self.base_selenium.get_url()
        current_shipment_date = self.order_page.get_shipment_date()
        new_shipment_date = self.generate_random_string()
        self.order_page.set_shipment_date(new_shipment_date)
        if 'save' == save:
            self.order_page.save(save_btn='order:save')
        else:
            self.order_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_shipment_date, self.order_page.get_shipment_date())
        else:
            self.assertEqual(current_shipment_date, self.order_page.get_shipment_date())
