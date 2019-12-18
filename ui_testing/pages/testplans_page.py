from ui_testing.pages.base_pages import BasePages
from random import randint


class TestPlans(BasePages):
    def __init__(self):
        super().__init__()
        self.test_plans_url = "{}testPlans".format(self.base_selenium.url)

    def get_test_plans_page(self):
        self.base_selenium.LOGGER.info(' + Get test plans page.')
        self.base_selenium.get(url=self.test_plans_url)
        self.sleep_small()

    def get_random_test_plans(self):
        row = self.get_random_table_row('test_plans:test_plans_table')
        self.open_edit_page(row=row)

    def click_create_test_plan_button(self):
        self.base_selenium.click(element='test_plans:new_test_plan')
        self.sleep_small()

    def get_test_plan_edit_page(self, name):
        test_plan = self.search(value=name)[0]
        self.open_edit_page(row=test_plan)

    def get_testunits_in_testplans(self, test_plan_name=''):
        self.base_selenium.LOGGER.info('Filter by testplan name {}'.format(test_plan_name))
        self.search(value=test_plan_name)
        new_testplan_testunits=self.get_child_table_data(index=0)

        testplan_testunits = []
        for testunit in new_testplan_testunits:
            testplan_testunits.append(testunit['Test Unit Name'])
    
        return testplan_testunits
    
    def click_overview_link(self, with_popup = True):
        self.base_selenium.click(element='test_plan:overview')
        if with_popup == True:
            self.confirm_popup()

    def get_current_page_name(self):
        current_page_url = self.base_selenium.get_url()
        current_page_name = current_page_url.split('/')[-1]  # get the last name in the url
        return current_page_name

