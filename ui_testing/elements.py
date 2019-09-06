elements = {
    'general': {
        'child_table_arrow': {'method': 'class_name',
                              'value': 'm-datatable__toggle-subtable',
                              'order': 0},
        'table_child': {'method': 'class_name', 'value': 'dataTable', 'order': 1},

        'search': {'method': 'id',
                           'value': 'generalSearch'},
                'table': {'method': 'id',
                          'value': 'table'},
                'table_child': {"method": "class_name",
                                "value": "dataTable",
                                "order":1
                                },
                'save': {'method': 'class_name',
                         'value': 'btn-primary',
                         'order': 0},
                'saveWithId': {'method': 'id',
                               'value': 'saveButton'},
                'cancelWithId': {'method': 'id',
                                 'value': 'cancelButton'},
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
        'filter_apply_btn': {'method': 'class_name',
                             'value': 'btn-primary',
                             'order': 0},
                # 'filter_reset_btn': {'method': 'class_name',
                #              'value': 'btn-secondary',
                #              'order': 1},
                'ng_values': {'method': 'class_name',
                              'value': 'ng-value',
                              'order': -1},
                'cancel_span': {'method': 'tag_name',
                                'value': 'span',
                                'order': 0},
                'checkbox': {'method': 'class_name',
                             'value': 'm-checkbox',
                             'order': 0},
                'child_table_arrow': {'method': 'class_name',
                                'value': 'm-datatable__toggle-subtable',
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
                'oh_snap_msg': {'method': 'id',
                                'value': 'ohSnapMsg'},
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
                               'value': 'table_info'},
                'filter_btn': {'method': 'id',
                            'value': 'filter_btn'},
                'filter_reset_btn': {'method': 'id',
                            'value': 'reset_btn'}
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

    'test_units': {
        'test_units_table': {'method': 'id',
                             'value': 'table'},
    'right_menu': {'method': 'xpath',
                       'value': '//*[@id="custom-accordion-panel"]/div/a/i'},
    'archive': {'method': 'link_text',
                    'value': 'Archive'},
    'archived': {'method': 'link_text',
                     'value': 'Archived'},
    'restore': {'method': 'link_text',
                    'value': 'Restore'},
    'active': {'method': 'link_text',
                   'value': 'Active'},

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

    'test_unit': {
        'no': {'method': 'id',
               'value': 'numberfield'},
        'upperLimitField': {'method': 'id',
                            'value': 'upperLimitfield'},
        'material_type': {'method': 'xpath',
                          'value': '//*[@id="materialTypefield"]'},
        'material_type_options': {'method': 'class_name',
                                  'value': 'ng-option'},
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
        'filter_order_no': {'method': 'id',
                            'value': 'orderNofield'},
        'analysis_filter': {'method': 'id',
                            'value': 'analysisfield'},
        'order_filter': {'method': 'id',
                         'value': 'orderNofield'},
        'contact_filter': {'method': 'id',
                           'value': 'companyfield'},
        'changed_by': {'method': 'id',
                       'value': 'lastModifiedUserfield'},
        'material_type_filter': {'method': 'id',
                                 'value': 'materialTypefield'},
        'article_filter': {'method': 'id',
                           'value': 'articlefield'},
        'chnaged_on_filter': {'method': 'id',
                              'value': 'start_createdAt'},
        'test_date_filter': {'method': 'id',
                             'value': 'start_testDate'},
        'shipment_date_filter': {'method': 'id',
                                 'value': 'start_shipmentDate'}
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

        'auto_fill': {'method': 'xpath', 'value': '//*[@id="field"]/div[2]/div/span'},
        'auto_fill_container': {'method': 'xpath', 'value': '//*[@id="field"]/div[2]'},

        'contact': {'method': 'id',
                    'value': 'contactfield'},
        'tests': {'method': 'id',
                  'value': 'tests'},
        'test_plan': {'method': 'id',
                      'value': 'testPlans'},
        'test_unit': {'method': 'id',
                      'value': 'testUnits'},
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

        'cancel_btn': {'method': 'id',
                       'value': 'button_cancel_order'},
        'value': 'orderNoWithYearfield',
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
        'save': {'method': 'class_name',
                 'value': 'btn-primary',
                 'order': 1},
        'duplicate_table_view': {'method': 'id',
                                 'value': 'duplicate_table_view'},
        'delete_table_view': {'method': 'id',
                              'value': 'delete_table_view'},
        'change_view': {'method': 'class_name',
                        'value': 'icon-views',
                        'order': 0
                        },

        'suborder_list': {'method': 'class_name',
                          'value': 'flaticon-signs',
                          'order': 0},
        'suborder_table': {'method': 'id',
                           'value': 'table-with-add'},
        'add_new_item': {'method': 'class_name',
                         'value': 'addNewItem',
                         'order': 0},
        'order_no_error_message' : {'method': 'xpath',
                                'value': '//*[@id="field"]/div[3]/div/span'},
        'confirm_pop': {'method': 'class_name',
                                'value': 'btn-success',
                                'order': 0},
        'confirm_cancel': {'method': 'class_name',
                                'value': 'btn-secondary',
                                'order': 2},
    'analysis': {
        'filter_order_no': {
                        'method': 'id',
                        'value': 'orderNofield'}
                        },
        'filter_analysis_no': {
                        'method': 'id',
                        'value': 'nofield'
        }
    }
}
