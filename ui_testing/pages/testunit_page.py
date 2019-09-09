from ui_testing.pages.testunits_page import TstUnits


class TstUnit(TstUnits):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")

    def set_testunit_name(self, name=''):
        self.base_selenium.set_text(element='test_unit:testunit_name', value=name)

    def save_and_create_new_version (self, confirm=True):
        self.save(save_btn='general:save_and_complete')
        self.sleep_small()
        self.confirm_popup(force=confirm)
        self.sleep_small()
