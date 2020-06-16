from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from random import choice


class NGSelect:
    def __init__(self, driver: Chrome, ng_select={}):
        """

        :param driver: The web driver instance
        :param ng_select: {"method": "", "value": ""}
        """
        self.driver = driver
        self.ng_select_element = ng_select

    def ng_select(self):
        return self.driver.find_element(getattr(By, self.ng_select_element["method"]), self.ng_select_element["value"])

    @property
    def ng_drop_down(self):
        return self.driver.find_element_by_tag_name('ng-dropdown-panel')

    @property
    def ng_drop_down_options(self):
        return self.ng_drop_down.find_elements_by_css_selector("[role='option']")

    @property
    def ng_drop_down_options_text(self):
        return [option.text for option in self.ng_drop_down_options if len(option.text) > 0]

    @property
    def ng_drop_down_unique_options_text(self):
        return list(set(self.ng_drop_down_options_text))

    @property
    def ng_input(self):
        return self.ng_select.find_element_by_tag_name('input')

    @property
    def ng_values(self):
        return [value for value in self.ng_select.find_elements_by_class_name('ng-value')]

    @property
    def ng_values_text(self):
        return [value.find_element_by_class_name('ng-value-label').text for value in self.ng_values]

    @property
    def is_drop_down_disabled(self):
        if 'ng-select-disabled' in self.ng_drop_down.get_attribute(attribute='class'):
            return True
        else:
            return False

    @property
    def is_ng_single_option(self):
        if 'ng-select-single' in self.ng_select.get_attribute('class'):
            return True
        else:
            return False

    @property
    def is_ng_multiple_options(self):
        if 'ng-select-multiple' in self.ng_select.get_attribute('class'):
            return True
        else:
            return False

    @property
    def is_there_selected_option(self):
        return len(self.ng_values) > 0

    def ng_input_set_text(self, text):
        self.ng_input.clear()
        self.ng_input.send_keys(text)

    def is_option_text_existing(self, text):
        self.ng_input_set_text(text)
        return text in self.ng_drop_down_options_text

    def select_option_by_text(self, text):
        if self.is_drop_down_disabled:
            raise Exception(f"Unable to select {text} in disabled drop down menu.")

        if self.is_option_text_existing(text):
            self.ng_drop_down.find_element_by_xpath(f'//span[contains(text(), "{text}")]').click()
            return text
        else:
            raise Exception(f"There is no {text} option in this drop down menu.")

    def select_random_option(self):
        text = choice(self.ng_drop_down_options_text)
        self.select_option_by_text(text=text)
        return text

    def select_unique_random_option(self):
        text = choice(self.ng_drop_down_unique_options_text)
        self.select_option_by_text(text=text)
        return text

    def clear_single_option(self):
        if self.is_there_selected_option:
            self.ng_select.find_element_by_class_name('ng-clear-wrapper').click()

    def clear_multiple_option_by_text(self, text):
        for value in self.ng_values:
            if text in value.text:
                value.find_element_by_class_name('ng-value-icon').click()
                break

    def clear_all_multiple_option(self):
        for value in self.ng_values:
            value.find_element_by_class_name('ng-value-icon').click()

    def get_ng_drop_down_suggest_list(self, text):
        self.ng_input_set_text(text)
        return self.ng_drop_down_options_text
