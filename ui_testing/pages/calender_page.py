from ui_testing.pages.base_pages import BasePages


class Calender(BasePages):
    def __init__(self):
        super().__init__()

    def get_calender(self):
        self.base_selenium.click(element='calender:get_calender')
        self.sleep_tiny()

    def prev_month(self):
        self.base_selenium.click(element='calender:prev')
        self.sleep_tiny()
        return (self.base_selenium.get_text(element='calender:month').split(' ')[0])

    def nxt_month(self):
        self.base_selenium.click(element='calender:nxt')
        self.sleep_tiny()
        return (self.base_selenium.get_text(element='calender:month').split(' ')[0])

    def current_month(self):
        self.base_selenium.click(element='calender:current')
        self.sleep_tiny()
        return (self.base_selenium.get_text(element='calender:month').split(' ')[0])

    def close_calender(self):
        self.base_selenium.click(element='calender:close')
        self.sleep_tiny()
        return (self.base_selenium.get_text(element='calender:title'))





