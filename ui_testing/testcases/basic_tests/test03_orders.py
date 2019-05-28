from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.login_page import Login
from ui_testing.pages.article_page import Article
from ui_testing.pages.testplan_page import TstPlan
from ui_testing.pages.order_page import Order
from ui_testing.pages.analyses_page import Analyses


class OrdersTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = Login()
        self.article_page = Article()
        self.test_plan = TstPlan()
        self.order_page = Order()
        self.analyses_page = Analyses()
        self.login_page.login(
            username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.order_page.get_orders_page()

    def test01_archive_order(self):
        """
            New: Orders: Archive
            The user cannot archive an order unless all corresponding analysis are archived
            LIMS-3425
        :return:
        """
        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)

        analysis_number_value = self.order_page.get_row_cell_text_related_to_header(
            order_row, 'Analysis No.')
        analysis_numbers_list = analysis_number_value.split(',')
        order_deleted = self.order_page.archive_selected_orders(
            check_pop_up=True)

        if order_deleted:
            self.analyses_page.get_analyses_page()
            self.order_page.sleep_medium()
            has_active_analysis = self.analyses_page.search_if_analysis_not_deleted(
            analysis_numbers_list)
            self.assertEqual(has_active_analysis, False)

    def test02_archiveOrder_has_active_analysis(self):
        """
            New: Archive order has active analysis
            The user cannot archive an order unless all corresponding analysis are archived
            LIMS-4329
        :return:
        """
        order_row = self.order_page.get_random_order_row()
        self.order_page.click_check_box(source=order_row)

        analysis_number_value = self.order_page.get_row_cell_text_related_to_header(
            order_row, 'Analysis No.')
        analysis_numbers_list = analysis_number_value.split(',')
        order_deleted = self.order_page.archive_selected_orders(
            check_pop_up=True)


        if not order_deleted:
            self.analyses_page.get_analyses_page()
            self.order_page.sleep_medium()
            self.analyses_page.search_by_number_and_archive(
                analysis_numbers_list)
            self.order_page.get_orders_page()
            self.order_page.sleep_medium()
            rows = self.order_page.search(analysis_numbers_list[0])
            self.order_page.click_check_box(source=rows[0])
            self.order_page.archive_selected_orders()
            rows = self.order_page.result_table()
            self.assertEqual(len(rows), 1)
