from api_testing.apis.base_api import BaseAPI


class TestUnitAPI(BaseAPI):
    def get_all_test_units(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_all_test_units'])
        _payload = {"sort_value": "number",
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

    def report_sheet_get_list_table(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['report_sheet_get_list_table'])
        _payload = {'sort_value': 'id',
                    'limit': 5,
                    'start': 0,
                    'sort_order': 'asc',
                    'filter': '{"id":2440}'}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    def get_all_testunits_json(self):
        testunits = self.get_all_test_units().json()['testUnits']
        return testunits
        
    def get_testunit_form_data(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_unit_api']['form_data'], str(id)) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['testUnit']
        else:
            return False
    
    def archive_testunits(self, ids=['1']):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['test_unit_api']['archive_testunits'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def restore_testunits(self, ids=['1']):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['test_unit_api']['restore_testunits'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='operation_success':
            return True
        else:
            return False
    
    def delete_archived_testunit(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['test_unit_api']['delete_testunit'], str(id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='hard_delete_success':
            return True
        else:
            return False

    def delete_active_testunit(self, id=1):
        if self.archive_testunits(ids=[str(id)]):
            if self.delete_archived_testunit(id=id):
                return True
            else:
                self.restore_testunits(ids=[str(id)])
                return False
        else:
            return False

    def list_testunits_types(self):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_testunit_types']) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        return data
    
    def list_testunits_concentrations(self):
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['list_testunit_concentrations']) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        return data['concentrations']

    def create_qualitative_testunit(self, **kwargs):
        request_body = {}
        request_body['selectedConcs'] = []
        request_body['unit'] = ''
        request_body['dynamicFieldsValues'] = []
        request_body['type'] = {
            'id': 1,
            'text': "Qualitative"
        }
        request_body['testUnitTypeId'] = 1
        qualitiative_values = kwargs['textValue'].split(',')
        values_arr = []
        for value in qualitiative_values:
            values_arr.append({
                'display': value,
                'value': value
            })
        request_body['textValueArray'] = values_arr
        
        if 'method' not in kwargs:
            request_body['method'] = 'random method'

        if 'iterations' not in kwargs:
            request_body['iterations'] = '1'

        request_body['selectedCategory'] = [kwargs['category']]
        
        payload = self.update_payload(request_body, **kwargs)
        
        api = '{}{}'.format(self.url, self.END_POINTS['test_unit_api']['create_testunit']) 
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=payload, params='', headers=self.headers, verify=False)

        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        
        if data['status'] == 1:
            return data['testUnit']
        else:
            return data['message']
    
    def create_quantitative_testunit(self, **kwargs):
        request_body = {}
        request_body['selectedConcs'] = []
        request_body['textValueArray'] = []
        request_body['textValue'] = ''
        request_body['unit'] = ''
        request_body['upperLimit'] = ''
        request_body['lowerLimit'] = ''
        request_body['useSpec'] = True
        request_body['quantificationUpperLimit'] = ''
        request_body['quantificationLowerLimit'] = ''
        request_body['dynamicFieldsValues'] = []
        request_body['type'] = {
            'id': 2,
            'text': "Quantitative"
        }
        request_body['testUnitTypeId'] = 2
        return self.create_testunit(request_body=request_body, **kwargs)
    
    
    def create_mibi_testunit(self, **kwargs):
        request_body = {}
        request_body['textValueArray'] = []
        request_body['textValue'] = ''
        request_body['unit'] = ''
        request_body['textValue'] = ''
        request_body['dynamicFieldsValues'] = []
        request_body['type'] = {
            'id': 3,
            'text': "Quantitative MiBi"
        }
        request_body['testUnitTypeId'] = 3
        concentrations_arr = []
        self.info(kwargs['selectedConcs'])
        for concetration in kwargs['selectedConcs']:
            concentrations_arr.append({
                'id': concetration['id'],
                'text': concetration['name']
            })

        kwargs['selectedConcs'] = concentrations_arr

        return self.create_testunit(request_body=request_body, **kwargs)

    # you need to add the following attributes
    # {
    # number: testunit number
    # name: testunit name
    # selectedMAterialType: [
    # {
    #   'id': material type id,
    #   'text': material type text
    # }
    # ]
    # category: {
    #   'id': 'new' in case of creating new category, category id in case of old category
    #   'text': category text
    # }
    # type: {
    #   'id': testunit type id can be obtained using API call list_testunits_types,
    #   'text': testunit type text
    # }
    # unit: *optional*
    # method: mandatory field, will be set to 'random method' in case no method provided
    # textValue: string separated by ',' dentoes the values of specifications (in case of qualtiative testunit only)
    # useQuantification: True/False in case of Quantitative testunits with quantification limit 
    # useSpec: True/False in case of Quantitative testunits with specifications
    # upperLimit: specification upper limit in case of Quantitative with specifications
    # lowerLimit: specification lower limit in case of Quantitative with specifications
    # quantificationUpperLimit: quantification upper limit in case of Quantitative with quantification
    # quantificationLowerLimit: quantification lower limit in case of Quantitative with quantification
    # quantificationUnit: unit in case of quantification limit
    # selectedConcs: [
    # {
    #   'id': concentration id, can be obtained using list_testunits_concentrations,
    #   'text': concentration text, can be obtained using list_testunits_concentrations
    # }
    # ]
    # in case of MiBi, use upperLimit: to define mibi upper limit value
    # }

    def list_testunit_by_name_and_material_type(self, materialtype_id, name='', negelectIsDeleted=0, searchableValue=''):
        api = '{}{}{}?name={}&negelectIsDeleted={}&searchableValue={}'.format(self.url, self.END_POINTS['test_unit_api']['list_testunit_by_name_and_materialtype'], materialtype_id, name, negelectIsDeleted, searchableValue) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['testUnits']
        return []
        
