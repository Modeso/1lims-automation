from ui_testing.testcases.base_test import BaseTest

class ContactsTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page.login(username=self.base_selenium.username, password=self.base_selenium.password)
        self.base_selenium.wait_until_page_url_has(text='dashboard')
        self.contacts_page.get_contacts_page()


    def test002_edit_approach_overview_button(self):
        """
        Edit: Overview Approach: Make sure after I press on
        the overview button, it redirects me to the active table
        LIMS-6202
        
        New: Contact: Cancel button: After I edit in any field 
        then press on cancel button, a pop up will appear that 
        the data will be lost 
        LIMS-3585
        """
        self.contacts_page.get_random_contact()
        contact_url = self.base_selenium.get_url()
        self.base_selenium.LOGGER.info('contact_url : {}'.format(contact_url))
        # click on Overview, it will redirect you to contacts' page
        self.base_selenium.LOGGER.info('click on Overview')
        self.base_page.click_overview()
        self.article_page.sleep_small()
        self.assertEqual(self.base_selenium.get_url(), '{}contacts'.format(self.base_selenium.url))
        self.base_selenium.LOGGER.info('clicking on Overview confirmed')




