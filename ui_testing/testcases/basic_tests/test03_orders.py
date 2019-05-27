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


    @parameterized.expand(['cancel'])
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
            self.article_page.cancel(force=True)

        self.base_selenium.get(url=order_url, sleep=self.base_selenium.TIME_MEDIUM)

        if 'save' == save:
            self.assertEqual(new_no, self.order_page.get_no())
        else:
            self.assertEqual(current_no, self.order_page.get_no())

    @parameterized.expand(['save'])
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
