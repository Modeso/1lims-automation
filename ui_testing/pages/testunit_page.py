from ui_testing.pages.testunits_page import TstUnits


class TstUnit(TstUnits):
    def get_no(self):
        return self.base_selenium.get_value(element="test_plan:no")


    def set_upper_limit(self, value=''):
        self.base_selenium.set_text(element='test_unit:upperLimitField', value=value)

    def press_save(self):
        self.save(save_btn='general:saveWithId')
        