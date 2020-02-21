from api_testing.apis.base_api import BaseAPI


class OrdersAPI(BaseAPI):
    def get_all_orders(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['list_all_orders'])
        _payload = {"sort_value": "createdAt",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response
        

    def get_order_by_id(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['get_order_by_id'], str(id)) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    # the following steps creates you an order
    # autogenerated_order_no = self.orders_api.get_auto_generated_order_no()
    # material_type = self.general_utilities_api.list_all_material_types()[0]
    # article = self.article_api.list_articles_by_materialtype(materialtype_id=material_type['id'])[0]
    # testunits = self.test_unit_api.list_testunit_by_name_and_material_type(materialtype_id=material_type['id'])[0]
    # testplans = self.article_api.list_testplans_by_article_and_materialtype(materialtype_id=material_type['id'], article_id=article['id'])[0]
    # test_date = self.test_unit_page.get_current_date_formated()
    # shipment_date = self.test_unit_page.get_current_date_formated()
    # current_year = self.test_unit_page.get_current_year()[2:]
    # contacts = self.contacts_api.get_all_contacts().json()['contacts'][0]
    # self.base_selenium.LOGGER.info(self.orders_api.create_new_order(yearOption=1, orderNo=autogenerated_order_no, year=current_year, testUnits=[testunits], testPlans=[testplans], article=article, materialType=material_type, shipmentDate=shipment_date, testDate=test_date, contact=[contacts]))

    def create_new_order(self, **kwargs):
        """
        this function will create order with the following data.
        orderNo: random order no,
        contact: ASContact,
        materialType: Raw Material,
        article: art_rm no 2,
        testUnits: tu_rm_ql no 2,
        testDate and shipmentDate: 1-1-2020
        if you want to create an order with specific data, here are the parameters you will need to change.
        orderNo: number, denotes the rder number,
        contact: [{
            'id': contact id,
            'text': contact text
        }],
        'departments': [{
            'id': department id,
            'text': department name,
            'group': department's contact id
        }]
        'materialType': {
            'id': material type id,
            'text': material type name
        },
        article: {
            'id': article id,
            'text': article text
        },
        'testUnits': [{
            'id': testunit id,
            'text': testunit name,
            'new': True/False True for create, False is while updating so it doesn't add new testunit to this order's analysis
        }],
        'testPlans': {
            'id': orders testplan id, can be obtained using this call self.article_api.list_testplans_by_article_and_materialtype(materialtype_id=material_type['id'], article_id=article['id'])[0],
            'text' testplan name
        },
        'testDate': order's testdate in format 'YYYY-MM-DD' ex. '2020-1-1',
        'shipmentDate': order's shipmentDate in format 'YYYY-MM-DD' ex. '2020-1-1',

        """
        auto_generated_order_no = self.generate_random_number()
        _payload = {
            'orderNo': str(auto_generated_order_no),
            'contact':[{
                'id': 1,
                'text': 'ASContact No: 1'
            }],
            'deletedTestPlans': [],
            'deletedAnalysisIds': [],
            'dynamicFieldsValues': [],
            'analysisNo': [],
            'selectedDepartments': [],
            'orderType': {
                'id': 1,
                'text': 'New Order'
            },
            'departments': [],
            'attachments': [],
            'testPlans': [],
            'selectedTestPlans': [],
            'testUnits': [{
                'id': 2,
                'name': 'tu_rm_ql No: 2',
                'new': True
            }],
            'selectedTestUnits': [{
                'id': 2,
                'name': 'tu_rm_ql No: 2',
                'new': True
            }],
            'materialType': {
                'id': 1,
                'text': 'Raw MAterial'
            },
            'materialTypeId': 1,
            'article': {
                'id': 2,
                'text': 'art_rm No:2'
            },
            'articleId': 2,
            'shipmentDate': '2020-1-1',
            'testDate': '2020-1-1',
            'testDatedateOption': {
                'year': 2020,
                'month': 1,
                'day': 1
            },
            'shipmentDatedateOption': {
                'year': 2020,
                'month': 1,
                'day': 1
            },
            'year': str(20),
            'yearOption': 1
        }
        payload = self.update_payload(_payload, **kwargs)

        if 'testPlans' in kwargs:
            selected_testplan_arr = []
            for testplan in payload['testPlans']:
                selected_testplan_arr.append({
                    'id': testplan['id'],
                    'name': testplan['name'],
                    'new': True,
                    'version': ''
                })
            payload['selectedTestPlans'] = selected_testplan_arr

        
        if 'testUnits' in kwargs:
            selected_testunits_arr=[]
            for testunit in payload['testUnits']:
                selected_testunits_arr.append({
                    'id': testunit['id'],
                    'name': testunit['name'],
                    'new': True
                })
                payload['selectedTestUnits'] = selected_testunits_arr

        if 'shipmentDate' in kwargs and kwargs['shipmentDate'] != '':
            shipment_date_arr = kwargs['shipmentDate'].split('-')
            payload['shipmentDatedateOption'] = {
                'year': shipment_date_arr[0],
                'month': shipment_date_arr[1],
                'day': shipment_date_arr[2]
            }
        
        current_date = {}
        if 'testDate' not in kwargs:
            current_date = self.get_current_date()
        else:
            current_date = kwargs['testDate']
        
        test_date_arr = current_date.split('-')
        payload['testDatedateOption']={
            'year': test_date_arr[0],
            'month': test_date_arr[1],
            'day': test_date_arr[2]
        }
        if 'article' in kwargs:
            payload['articleId'] = payload['article']['id']

        if 'yearOption' in kwargs:
            if kwargs['yearOption'] == 1:
                payload['orderNoWithYear']=kwargs['orderNo']+'-'+kwargs['year']
            elif kwargs['yearOption'] == 2:
                payload['orderNoWithYear']=kwargs['year']+'-'+kwargs['orderNo']
        else:
            payload['orderNoWithYear']=payload['orderNo']+'-'+payload['year']

        if 'materialType' in kwargs:
            payload['materialTypeId'] = kwargs['materialType']['id']


        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['create_new_order']) 
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=[payload], params='', headers=self.headers, verify=False)

        self.info('Status code: {}'.format(response.status_code))
        data = response.json()

        if data['status'] == 1:
            return payload
        else:
            return data['message']

    def get_auto_generated_order_no(self):
        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['get_auto_generated_number']) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return str(data['id'])
        return 

    def format_object(self, **kwargs):
        request_body = {}
        request_body = self.update_payload({}, **kwargs)
        request_body['deletedTestPlans'] = []
        request_body['deletedAnalysisIds'] = []
        request_body['dynamicFieldsValues'] = []
        request_body['analysisNo'] = []
        request_body['selectedDepartments'] = []
        request_body['orderType'] = {
            'id': 1,
            'text': 'New Order'
        }

        if 'departments' not in kwargs:
            request_body['departments'] = []
        if 'attachments' not in kwargs:
            request_body['attachments'] = []
        if 'testPlans' in kwargs:
            selected_testplan_arr = []
            for testplan in request_body['testPlans']:
                selected_testplan_arr.append({
                    'id': testplan['id'],
                    'name': testplan['name'],
                    'version': ''
                })
            request_body['selectedTestPlans'] = selected_testplan_arr
        else:
            request_body['testPlans'] = []
            request_body['selectedTestPlans'] = []

        
        if 'testUnits' in kwargs:
            selected_testunits_arr=[]
            for testunit in kwargs['testUnits']:
                selected_testunits_arr.append({
                    'id': testunit['id'],
                    'name': testunit['name'],
                    'new': True
                })
                request_body['selectedTestUnits'] = selected_testunits_arr
        else:
            request_body['testUnits'] = []
            request_body['selectedTestUnits'] = []

        if 'shipmentDate' in kwargs and kwargs['shipmentDate'] != '':
            shipment_date_arr = kwargs['shipmentDate'].split('-')
            request_body['shipmentDatedateOption'] = {
                'year': shipment_date_arr[0],
                'month': shipment_date_arr[1],
                'day': shipment_date_arr[2]
            }
        
        test_date_arr = kwargs['testDate'].split('-')
        request_body['testDatedateOption']={
            'year': test_date_arr[0],
            'month': test_date_arr[1],
            'day': test_date_arr[2]
        }

        request_body['articleId'] = kwargs['article']['id']
        if kwargs['yearOption'] == 1:
            request_body['orderNoWithYear']=kwargs['orderNo']+'-'+kwargs['year']
        elif kwargs['yearOption'] == 2:
            request_body['orderNoWithYear']=kwargs['year']+'-'+kwargs['orderNo']

        request_body['materialTypeId'] = kwargs['materialType']['id']


        return request_body

    def archive_main_order(self, mainorder_id):
        api = '{}{}{}/archive/mainOrder'.format(self.url, self.END_POINTS['orders_api']['archive_testunits'], str(mainorder_id)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def restore_main_order(self, mainorder_id):
        api = '{}{}{}/restore/mainOrder'.format(self.url, self.END_POINTS['orders_api']['restore_main_order'], str(mainorder_id)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'restore_success':
            return True
        else:
            return False
    
    def delete_main_order(self, mainorder_id):
        api = '{}{}{}/delete/mainOrder'.format(self.url, self.END_POINTS['orders_api']['delete_main_order'], str(mainorder_id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def archive_sub_order(self, suborder_id):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['orders_api']['archive_suborder'], str(suborder_id)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def restore_sub_order(self, suborder_id):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['orders_api']['restore_suborder'], str(suborder_id)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'restore_success':
            return True
        else:
            return False
    
    def delete_sub_order(self, suborder_id):
        api = '{}{}{}'.format(self.url, self.END_POINTS['orders_api']['delete_suborder'], str(suborder_id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False

    def get_archived_orders_json(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['orders_api']['list_all_orders'])
        _payload = {"sort_value": "createdAt",
                    "limit": 1000,
                    "start": 0,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "1"}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response.json()['orders']
