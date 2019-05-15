from ui_testing.testcses.base_test import Basetest
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TestPlan
from ui_testing.pages.order_page import Order
from ui_testing.pages.login_page import Login
from parameterized import parameterized
import re


class OrdersTestCases (Basetest)
   def setup (self):
     super().setup()
     self.login_page = Login()
     self.article_page = Article()
     self.testplan_page = TestPlan()
     self.order_page = Order()
     self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
     self.base_selenium.wait_until_page_url_has(text='dashbord')
     self.article_page.get_article_page()

     @parameterized.expand(['save', 'cancel'])
     def test003_cancel_button_edit_materail_type(self,save)

         """
                 New: Article: Save/Cancel button: After I edit no field then press on cancel button,
                 a pop up will appear that the data will be
                 
                 LIMS-4281
                 :return:
                 """

          self.article_page.get_random_article()
          article_url = self.base_selenium.get_url
          self.article_page.sleep_tiny()
          current_material_type = self.article_page.get_material_type()
          self.article_page.set_material_type(random=true)
          new_material_type = self.article_page.get_material_type()

             if'save' == save:
                 self.article_page.save()
             else:
                 self.article_page.cancel(force=True)

              self.base_selenium.get(url=article_url, sleep=5)

          if 'save' == save:
              self.assertEqual(new_materail_type, self.article_page.get_material_type())
          else
              self.assertEqual(current_materail_type, self.article_page.get_material_type())



