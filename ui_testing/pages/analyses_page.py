from ui_testing.pages.base_pages import BasePages


class Analyses(BasePages):
    def __init__(self):
        super().__init__()
        self.analysis_url = "{}analysis".format(self.base_selenium.url)

    def get_analyses_page(self):
        self.base_selenium.LOGGER.info(' + Get analyses page.')
        self.base_selenium.get(url=self.analysis_url)
        self.sleep_small()

    def search_by_number_and_archive(self, analysis_numbers_list):
        for analysis_number in analysis_numbers_list:
            rows = self.search(analysis_number)
            if len(rows) > 0:
                self.click_check_box(source=rows[0])
                self.archive_selected_items()
                self.clear_text('general:search')

    def search_if_analysis_exist(self, analysis_numbers_list):
        for analysis_number in analysis_numbers_list:
            rows = self.search(analysis_number)
            if len(rows) > 1:
                return True
        return False

    def filter_by_analysis_number(self, filter_text):
        self.base_selenium.LOGGER.info(' + Filter by analysis number : {}'.format(filter_text))
        self.filter_by(filter_element='analysis:analysis_no_filter', filter_text=filter_text, field_type='text')
        self.filter_apply()
        
    def analysis_filter(self, field_name, value=''):
        if field_name == 'analysis_no':
            self.filter_by_analysis_number(filter_text=value)
            
    def get_random_analysis(self):
        self.base_selenium.LOGGER.info(' + Get random analysis.')
        row = self.get_random_analysis_row()
        analysis_dict = self.base_selenium.get_row_cells_dict_related_to_header(row=row)
        self.get_random_x(row=row)
        return analysis_dict

    def get_random_analysis_row(self):
        return self.get_random_table_row(table_element='analyses:analyses_table')

    def archive_selected_analysis(self, check_pop_up=False):
        self.base_selenium.scroll()
        self.base_selenium.click(element='orders:right_menu')
        self.base_selenium.click(element='orders:archive')
        self.confirm_popup()
        if check_pop_up:
            if self.base_selenium.wait_element(element='general:confirmation_pop_up'):
                return False
        return True
