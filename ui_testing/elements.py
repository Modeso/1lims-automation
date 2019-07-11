elements = {
    'general': {'search': {'method': 'id',
                           'value': 'generalSearch'},
                'table': {'method': 'id',
                          'value': 'table'},
                'save': {'method': 'class_name',
                         'value': 'btn-primary',
                         'order': 0},
                'cancel': {'method': 'class_name',
                           'value': 'btn-secondary',
                           'order': 1},
                'confirmation_pop_up': {
                    'method': 'id',
                    'value': 'swal2-title'},

                'confirm_pop': {'method': 'class_name',
                                'value': 'btn-success',
                                'order': 0},
                'confirm_cancel': {'method': 'class_name',
                                   'value': 'btn-secondary',
                                   'order': 0},
                'cant_delete_message': {'method': 'id',
                                        'value': 'swal2-title'},
                'drop_down': {'method': 'class_name',
                              'value': 'ng-select',
                              'order': 0},
                'drop_down_options': {'method': 'class_name',
                                      'value': 'ng-option'},
                'drop_down_div': {'method': 'class_name',
                                  'value': 'ng-dropdown-panel-items',
                                  'order': 0},
                'input': {'method': 'tag_name',
                          'value': 'input',
                          'order': 0},
                'menu_filter_view': {'method': 'id',
                                     'value': 'custom-accordion-panel'},
                'filter': {'method': 'tag_name',
                           'value': 'span',
                           'order': 0},
                'ng_values': {'method': 'class_name',
                              'value': 'ng-value',
                              'order': -1},
                'cancel_span': {'method': 'tag_name',
                                'value': 'span',
                                'order': 0},
                'checkbox': {'method': 'class_name',
                             'value': 'm-checkbox',
                             'order': 0},
                'label': {'method': 'tag_name',
                          'value': 'label',
                          'order': 0},
                'right_menu': {'method': 'xpath',
                               'value': '//*[@id="custom-accordion-panel"]/div/a/i'},
                'archive': {'method': 'link_text',
                            'value': 'Archive'},
                'alert_confirmation': {'method': 'id',
                                       'value': 'noty_layout__topCenter'},
                'table_cells': {'method': 'tag_name',
                                'value': 'td',
                                'order': -1},
                'archived': {'method': 'link_text',
                             'value': 'Archived'},
                'restore': {'method': 'link_text',
                            'value': 'Restore'},
                'active': {'method': 'link_text',
                           'value': 'Active'},
                'delete': {'method': 'link_text',
                           'value': 'Delete'},
                'xslx': {'method': 'link_text',
                            'value': 'XSLX'},
                'table_info': {'method': 'id',
                               'value': 'table_info'}
                },
    'login': {
        'username': {'method': 'name',
                     'value': 'username',
                     'order': 0},
        'password': {'method': 'name',
                     'value': 'password',
                     'order': 0},
        'login_btn': {'method': 'id',
                      'value': 'm_login_signin_submit'},
        'refresh': {'method': 'xpath',
                    'value': '/html/body/div[3]/div/div[2]/div[2]/button'}
    },

    'articles': {
        'article_table': {'method': 'id',
                          'value': 'table'},
        'article_edit_button': {'method': 'tag_name',
                                'value': 'a',
                                'order': 2},
        'article_archive_button': {'method': 'tag_name',
                                   'value': 'a',
                                   'order': 0},
        'article_archive_dropdown': {'method': 'link_text',
                                     'value': 'Archive'},
        'confirm_archive': {'method': 'class_name',
                            'value': 'swal2-confirm',
                            'order': 0},
        'cancel_archive': {'method': 'class_name',
                           'value': 'swal2-cancel',
                           'order': 0},
        'new_article': {'method': 'link_text',
                        'value': 'New Article'},
        'archived': {'method': 'link_text',
                     'value': 'Archived'},
        'archive': {'method': 'link_text',
                    'value': 'Archive'},
        'active': {'method': 'link_text',
                   'value': 'Active'},
        'restore': {'method': 'link_text',
                    'value': 'Restore'},
        'delete': {'method': 'link_text',
                   'value': 'Delete'},
        'right_menu': {'method': 'xpath',
                       'value': '//*[@id="custom-accordion-panel"]/div/a/i'},
        'alert_confirmation': {'method': 'id',
                               'value': 'noty_layout__topCenter'}

    },
    'article': {
        'unit': {'method': 'id',
                 'value': 'unitfield'},
        'material_type': {'method': 'id',
                          'value': 'materialType'},
        'material_type_options': {'method': 'class_name',
                                  'value': 'ng-option'},
        'no': {'method': 'id',
               'value': 'Nofield'},
        'comment': {'method': 'id',
                    'value': 'comment'},
        'name': {'method': 'id',
                 'value': 'namefield'},

        'filter_test_plan': {'method': 'id',
                             'value': 'testPlansfield'},
        'filter_actions': {'method': 'class_name',
                           'value': 'actions',
                           'order': 0},
        'filter_apply_btn': {'method': 'class_name',
                             'value': 'btn-primary',
                             'order': 0},
        'filter_reset_btn': {'method': 'class_name',
                             'value': 'btn-secondary',
                             'order': 1},
        'related_article': {'method': 'id',
                            'value': 'selectedArticles'},
        'field': {'method': 'id',
                  'value': 'field'},
        'field_items': {'method': 'class_name',
                        'value': 'padding',
                        'order': -1}

    },
    'test_plans': {
        'test_plans_table': {'method': 'id',
                             'value': 'table'},
        'test_plans_edit_button': {'method': 'tag_name',
                                   'value': 'a',
                                   'order': 1},
        'new_test_plan': {'method': 'link_text',
                          'value': 'New Test Plan'}
    },

    'test_plan': {
        'no': {'method': 'id',
               'value': 'numberfield'},
        'test_plan': {'method': 'id',
                      'value': 'testPlan'},
        'material_type': {'method': 'xpath',
                          'value': '//*[@id="materialTypefield"]'},
        'material_type_options': {'method': 'class_name',
                                  'value': 'ng-option'},
        'article': {'method': 'css_selector',
                    'value': '#selectedArticles > div'
                    },
        'article_options': {'method': 'class_name',
                            'value': 'ng-option'},
        'next': {'method': 'link_text',
                 'value': 'Next'},
        'test_units': {'method': 'id',
                       'value': 'selectedTestUnitsfield'},
        'add': {'method': 'class_name',
                'value': 'btn-primary',
                'order': 0},
        'save': {'method': 'class_name',
                 'value': 'btn-primary',
                 'order': 1},
        'add_test_units': {'method': 'id',
                           'value': 'first-col'}
    },

    'orders': {
        'orders_table': {'method': 'id',
                         'value': 'table'},
        'orders_edit_button': {'method': 'tag_name',
                               'value': 'a',
                               'order': 4},
        'new_order': {'method': 'link_text',
                      'value': 'New Order'},
        'right_menu': {'method': 'xpath',
                       'value': '//*[@id="custom-accordion-panel"]/div/a/i'},
        'archive': {'method': 'link_text',
                    'value': 'Archive'},
        'analysis-confirmation': {
            'method': 'class_name',
            'value': 'swal2-header'},
        'duplicate': {'method': 'link_text',
                      'value': 'Duplicate'},
        'number_of_copies': {'method': 'id',
                             'value': 'numberOfCopies'},
        'create_copies': {'method': 'id',
                          'value': 'create_copies_id'},
        'save_order': {'method': 'id',
                'value': 'button_save_order'},
        'analysis_filter': {'method': 'id',
                'value': 'analysisfield'}        
    },

    'order': {
        'order': {'method': 'id',
                  'value': 'orderTypefield'},
        'material_type': {'method': 'xpath',
                          'value': '//*[@id="materialTypefield"]'},
        'article': {'method': 'css_selector',
                    'value': '#articlefield > div'},
        'departments': {'method': 'id',
                        'value': 'departments'},

        'contact': {'method': 'id',
                    'value': 'contactfield'},
        'tests': {'method': 'id',
                  'value': 'tests'},
        'test_plan': {'method': 'id',
                      'value': 'testPlans'},
        'test_plan_btn': {'method': 'tag_name',
                          'value': 'span',
                          'order': 0},
        'test_unit_btn': {'method': 'tag_name',
                          'value': 'span',
                          'order': 1},

        'save_btn': {'method': 'id',
                     'value': 'button_save_order'},

        'no': {'method': 'id',
               'value': 'orderNoWithYearfield'},
        # 'cancel': {'method': 'id',
        #            'value': 'button_cancel_order'},

        'cancel_button': {'method': 'class_name',
                          'value': 'swal2-cancel',
                          'order': 0},
        'ok': {'method': 'class_name',
               'value': 'swal2-confirm',
               'order': 0},

        'cancel': {'method': 'class_name',
                   'value': 'btn-secondary',
                   'order': 1},

        'order_number': {'method': 'id',
                         'value': 'orderNoWithYearfield'},
        'order_number_add_form': {'method': 'id',
                                  'value': 'selectedOrderNofield'},
        'shipment_date': {'method': 'id',
                          'value': 'date_shipmentDate'},
        'test_date': {'method': 'id',
                      'value': 'date_testDate'},
        'suborder_list': {'method': 'class_name',
                          'value': 'flaticon-signs',
                          'order': 0},
        'suborder_table': {'method': 'id',
                           'value': 'table-with-add'},
        'add_new_item': {'method': 'class_name',
                         'value': 'addNewItem',
                         'order': 0}
    }
}
