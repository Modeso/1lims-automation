from ui_testing.pages.testunits_page import TstUnits


class TstUnit(TstUnits):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")

    def set_testunit_name(self, name=''):
        self.base_selenium.set_text(element='test_unit:testunitName', value=name)

    def saveAndCreateNewVersion (self, confirm=True):
        self.save(save_btn='general:saveAndComplete')
        self.sleep_small()
        self.confirm_popup(force=confirm)
        self.sleep_small()
