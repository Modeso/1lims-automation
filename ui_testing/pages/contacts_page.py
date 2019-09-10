from ui_testing.pages.base_pages import BasePages
from random import randint


class Contacts(BasePages):
    def __init__(self):
        super().__init__()
        self.contacts_url = "{}contacts".format(self.base_selenium.url)

    def get_contacts_page(self):
        self.base_selenium.get(url=self.contacts_url)
        self.sleep_small()

    def get_contact_with_departments(self):
        self.base_selenium.LOGGER.info('Get contacts page')
        self.get_contacts_page()
        
        self.base_selenium.LOGGER.info('Get all the contacts records to get value with departmens')
        rows=self.result_table() 
        for row in rows:
            row_data = self.base_selenium.get_row_cells_dict_related_to_header(row)
            if row_data['Departments']:
                return row_data['Contact Name']

        return {}