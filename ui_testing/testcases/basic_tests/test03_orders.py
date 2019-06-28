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
    def test003_cancel_button_edit_departments(self, save):
        """
        Orders: department Approach: In case I update the department then press on save button ( the department updated successfully )
        & when I press on cancel button ( this department not updated )


        LIMS-4765
        LIMS-4765
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

