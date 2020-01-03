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
                self.restore_articles(ids=[id])
                return False
        else:
            return False