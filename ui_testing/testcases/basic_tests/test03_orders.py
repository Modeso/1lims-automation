from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.order_page import Order
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TestPlan
from parameterized import parameterized
import re


class OrdersTestCases(BaseTest):
   def setUp(self):
       super().setUp()
       self.login_page = Login()
       self.article_page = Article()
       self.test_plan = TestPlan()
       self.order_page = Order()
       self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
       self.base_selenium.wait_until_page_url_has(text='dashbord')
       self.order_page.get_order_page()

   @parameterized.expand(['save', 'cancel'])
   def test003_cancel_button_edit_material_type(self, save):
         """
         New: Orders: Cancel Button Approach: In case I update the material type field then press on cancel button
         message will appear ( data will be lost )
         LIMS-4281
         :return:
         """
         self.order_page.get_random_order()
         order_url = self.base_selenium.get_url()
         self.order_page.sleep_tiny()
         current_material_type = self.order_page.get_material_type()
         self.order_page.set_material_type(random=True)
         new_material_type = self.order_page.get_material_type()
         if 'save' == save:
             self.order_page.save()
         else:
             self.order_page.cancel(force=True)

         self.base_selenium.get(url=order_url, sleep=5)

         if 'save' == save:
             self.assertEqual(new_material_type, self.order_page.get_material_type())
         else:
             self.assertEqual(current_material_type, self.order_page.get_material_type())

