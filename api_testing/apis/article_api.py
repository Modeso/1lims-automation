from api_testing.apis.base_api import BaseAPI

class ArticleAPI(BaseAPI):
    def get_all_articles(self, **kwargs):
        api = '{}{}'.format(self.url, self.END_POINTS['article_api']['list_all_articles'])
        _payload = {"sort_value": "number",
                    "limit": 100,
                    "start": 1,
                    "sort_order": "DESC",
                    "filter": "{}",
                    "deleted": "0"}
        payload = self.update_payload(_payload, **kwargs)
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params=payload, headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        return response

    def get_article_form_data(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['article_api']['form_data'], str(id)) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['article']
        else:
            return False
    
    def archive_articles(self, ids=['1']):
        api = '{}{}{}/archive'.format(self.url, self.END_POINTS['article_api']['archive_articles'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message'] == 'delete_success':
            return True
        else:
            return False
    
    def restore_articles(self, ids=['1']):
        api = '{}{}{}/restore'.format(self.url, self.END_POINTS['article_api']['restore_articles'], ','.join(ids)) 
        self.info('PUT : {}'.format(api))
        response = self.session.put(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='restore_success':
            return True
        else:
            return False
    
    def delete_archived_article(self, id=1):
        api = '{}{}{}'.format(self.url, self.END_POINTS['article_api']['delete_article'], str(id)) 
        self.info('DELETE : {}'.format(api))
        response = self.session.delete(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1 and data['message']=='hard_delete_success':
            return True
        else:
            return False

    def delete_active_article(self, id=1):
        if self.archive_articles(ids=[str(id)]):
            if self.delete_archived_article(id=id):
                return True
            else:
                self.restore_articles(ids=[str(id)])
                return False
        else:
            return False

    def create_article(self, number, name, material_type={"id": "", "text": ""}, **kwargs):
        """
        Create an article.
        :param number: article number.
        :param name: article name.
        :param material_type: {"id": "new" or general_utilities_api.list_all_material_types()[#NUMBER], "test": material_type text}
        :param kwargs:
        :return: response
        """
        api = '{}{}'.format(self.url, self.END_POINTS['article_api']['create_article'])
        _payload = {
            "No": number,
            "name": name,
            "materialType": material_type,
            "selectedArticles": [],
            "selectedArticlesNos": [],
            "dynamicFieldsValues": [],
            "selectedMaterialType": [material_type],
            "materialTypeId": [material_type['id']]
        }
        payload = self.update_payload(_payload, **kwargs)
        self.info('POST : {}'.format(api))
        response = self.session.post(api, json=payload, params='', headers=self.headers, verify=False).json()
        self.info('Status code: {}'.format(response['status']))
        return response

    def list_articles_by_materialtype(self, materialtype_id=1, name='', is_archived=0):
        api = '{}{}{}/{}?name={}'.format(self.url, self.END_POINTS['article_api']['list_articles_by_materialtype'], materialtype_id, is_archived, name) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['articles']
        return []
    
    def list_testplans_by_article_and_materialtype(self, materialtype_id=1, article_id=1):
        api = '{}{}{}/{}'.format(self.url, self.END_POINTS['article_api']['list_testplans_by_article_and_materialtype'], article_id, materialtype_id) 
        self.info('GET : {}'.format(api))
        response = self.session.get(api, params='', headers=self.headers, verify=False)
        self.info('Status code: {}'.format(response.status_code))
        data = response.json()
        if data['status'] == 1:
            return data['testPlans']
        return []

    def get_articles_with_no_testplans(self,**kwargs):
        response = self.get_all_articles(**kwargs)
        all_articles = response.json()['articles']
        articles = [article for article in all_articles if len(article['testPlanNames']) < 1]
        return articles

    def get_articles_with_testplans(self, **kwargs):
        response = self.get_all_articles(**kwargs)
        all_articles = response.json()['articles']
        articles = [article for article in all_articles if len(article['testPlanNames']) >= 1]
        return articles
