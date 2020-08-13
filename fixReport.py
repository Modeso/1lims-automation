import IPython
import requests

BASE_API = "http://35.239.200.77:8080/api/v1"
AUTHONTICATION = "bearer bc3accb5-5e4f-4dcc-ba68-2307fb40a56d"
session = requests.Session()
headers = {'Content-Type': "application/json",
           'Authorization': AUTHONTICATION,
           'Connection': "keep-alive",
           'cache-control': "no-cache"}


def get_project_launchs(project_name):
    API = f"{BASE_API}/{project_name}/launch"
    response = session.get(API, headers=headers)
    return response

def get_project_launch_by_description(project_name, description):
    API = f"{BASE_API}/{project_name}/launch?filter.eq.description={description}"
    response = session.get(API, headers=headers)
    return response

def get_project_launch_id_by_description(project_name, desription):
    res = get_project_launch_by_description(project_name, desription)
    return res

def get_test_items(project_name, launch_id):
    API = f"{BASE_API}/{project_name}/item?page.size=500&filter.eq.launch={launch_id}"
    response = session.get(API, headers=headers)
    return response


def get_test_items_by_status(project_name, launch_id, status):
    API = f"{BASE_API}/{project_name}/item?page.size=500&filter.eq.launch={launch_id}&filter.eq.status={status}"
    response = session.get(API, headers=headers)
    return response

def delete_test_items(project_name, ids):
    API = f"{BASE_API}/{project_name}/item?ids={ids}"
    response = session.delete(API, headers=headers)
    return response


def merge_launchs_with_same_description(project_name, launch_des):
    API = f"{BASE_API}/{project_name}/launch/merge"
    launchs_res = get_project_launch_id_by_description(project_name, launch_des)
    ids = [content['id'] for content in launchs_res.json()['content']]
    _payload = {
              "tags": [""],
              "start_time": launchs_res.json()['content'][0]['start_time'],
              "end_time": launchs_res.json()['content'][0]['end_time'],
              "name": project_name,
              "description": launch_des,
              "launches": ids,
              "extendSuitesDescription": False,
              "merge_type": "BASIC"
    }
    return session.post(API, headers=headers, json=_payload)

def _get_duplicate_fliky_test_cases(project_name, launch_id):
    duplicate_test_case = {}
    test_items = get_test_items(project_name, launch_id).json()['content']
    for test_item in test_items:
        for tmp in test_items:
            if test_item['name'] == "test026_filter_article_by_any_field_1_number":
                if tmp['name'] == "test026_filter_article_by_any_field_1_number":
                    import ipdb; ipdb.set_trace()
            if (test_item['name'] == tmp['name']) and (test_item['id'] != tmp['id']):
                if test_item['name'] in duplicate_test_case.keys():
                    duplicate_test_case[test_item['name']].append(test_item)
                else:
                    duplicate_test_case[test_item['name']] = [test_item]
    return duplicate_test_case

def delete_fliky_failed_test_items(project_name, launch_id):
    delete_id = ""
    duplicate_fliky_tests = _get_duplicate_fliky_test_cases(project_name, launch_id)
    for _, duplicate_tests in duplicate_fliky_tests.items():
        duplicate_test_failed = []
        fliky_flag = False
        for duplicate_test in duplicate_tests:
            if duplicate_test['status'] == 'FAILED':
                duplicate_test_failed.append(duplicate_test['id'])
            elif duplicate_test['status'] == 'PASSED':
                fliky_flag = True

        duplicate_test_failed_ids = list(set(duplicate_test_failed))
        if fliky_flag:
            for duplicate_test in duplicate_test_failed_ids:
                delete_id = f"{delete_id},{duplicate_test}"
        else:
            for duplicate_test in duplicate_test_failed_ids[:-1]:
                delete_id = f"{delete_id},{duplicate_test}"
    return delete_test_items(project_name, delete_id[1:])




PROJECT_NAME = 'onelims'
LAUNCH_DES = 'refs/pull/307/merge-204101434-366'

print(f'merge all launches with {LAUNCH_DES} description')
merged_launch = merge_launchs_with_same_description(PROJECT_NAME, LAUNCH_DES)

print(f'delete duplicate fliky test cases in launch : {LAUNCH_DES}')
# launch_id = get_project_launch_id_by_description(PROJECT_NAME, LAUNCH_DES).json()['content'][0]['id']

print(f'launch ID : {merged_launch.json()["id"]}')
res = delete_fliky_failed_test_items(PROJECT_NAME, merged_launch.json()["id"])
print(res.json())

IPython.embed()
