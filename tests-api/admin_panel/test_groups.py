import pytest
import os
from src import testlogger
from src import webservice
from src.setup import Setup_Library
from src import utils
from config import fwork
from src.dataReader import data
import json

logger = testlogger.setup_custom_logger('ewa_admin')
setup_test = Setup_Library()
groups_data = data().get_data("groups")
base_url = setup_test.data.login.base_url
apis = setup_test.data.apis
admin_token = setup_test.get_admin_token()


class TestGroupsApi(object):
    """
            Fixtures for the Groups test

    """
    # schemas
    group_schema = os.path.join(fwork.IN_DATA_PATH, groups_data.get('groups_list_schema'))

    @pytest.fixture(scope='class')
    def delete_after_add_group(self, request):
        groups_added = []

        def cleanup():
            for group_id in groups_added:
                group_delete_url = base_url + apis.delete_group_endpoint + str(group_id)
                webservice.delete(url=group_delete_url, token=admin_token)
                print " Group Deleted ..."

        request.addfinalizer(cleanup)
        return groups_added

    @pytest.fixture(params=groups_data.get('add_group'))
    def add_payload(self, request):
        return request.param

    """
                    Get group List Test cases

    """

    def test_validate_Groups_schema(self):
        logger.debug('group List: test_validate_Groupss_schema')
        response = webservice.get(url=base_url + apis.group_list_endpoint, token=admin_token)
        logger.debug('Groups: Validating json schema')
        utils.assert_valid_schema(response.json(), TestGroupsApi.group_schema)

    def test_EWA_1898_pass_invalid_authorization_token(self):
        logger.debug('group List: test invalid authorization token')
        response = webservice.get(url=base_url + apis.group_list_endpoint,
                                  token=admin_token[::-1])  # reverse token
        assert response.status_code == 401

    def test_EWA_1918_null_authorization_getGroupList(self):
        logger.debug('group List: test_validate_Groups_schema')
        response = webservice.get(url=base_url + apis.group_list_endpoint, token=None)
        assert response.status_code == 401

    def test_EWA_1916_empty_authorization_token_getGroupList(self):
        logger.debug('group List: test invalid authorization token')
        response = webservice.get(url=base_url + apis.group_list_endpoint, token='')

        assert response.status_code == 401

    def test_EWA_1917_non_admin_token_getGroupList(self):
        logger.debug('group List: test with non admin  authorization token')
        response = webservice.get(url=base_url + apis.group_list_endpoint, token=setup_test.get_employee_token())
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == groups_data.get('non_admin_token_response').get('responseCode')
        assert response_data['message'] == groups_data.get('non_admin_token_response').get('message')



    """
                    Add group  Test cases

    """

    def test_EWA_1927_empty_authorization_token_addNewGroup(self):
        logger.debug('Add Groups : test empty authorization token')
        response = webservice.post(url=base_url + apis.add_group_info_endpoint, token='', data={})
        assert response.status_code == 401

    def test_EWA_1924_invalid_authorization_token_addNewGroup(self):
        logger.debug('Add Groups : test invalid authorization token')
        response = webservice.post(url=base_url + apis.add_group_info_endpoint, token='invalidToken', data={})
        assert response.status_code == 401

    def test_EWA_1921_null_authorization_token_addNewGroup(self):
        logger.debug('Add Groups : test null authorization token')
        response = webservice.post(url=base_url + apis.add_group_info_endpoint, token=None, data={})
        assert response.status_code == 401



    def test_EWA_1909_1934_add_new_group(self,add_payload, delete_after_add_group):

        logger.debug('Add groups : Add new group ')
        response = webservice.post(url=base_url + apis.add_group_info_endpoint, token=admin_token, data=json.dumps(add_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == groups_data.get('add_group_response').get('responseCode')
        assert response_data['message'] == groups_data.get('add_group_response').get('message')
        delete_after_add_group.append(response_data['groupInfo']['groupId'])



    def test_EWA_2020_create_group_with_same_name(self, add_payload):
        logger.debug('Add groups : Add new group ')
        response = webservice.post(url=base_url + apis.add_group_info_endpoint, token=admin_token,
                                   data=json.dumps(add_payload))
        response_data = response.json()
        assert response.status_code == 200


        assert response_data['responseCode'] == groups_data.get('add_group_with_same_name').get('responseCode')
        assert response_data['message'] == groups_data.get('add_group_with_same_name').get('message')

    def test_EWA_2021_create_group_with_same_name_different_description(self, add_payload):
        logger.debug('Add groups : Add new group ')
        new_payload = dict(add_payload)
        new_payload['groupDescription'] = add_payload.get('groupDescription') + "_new"

        response = webservice.post(url=base_url + apis.add_group_info_endpoint, token=admin_token,
                                   data=json.dumps(new_payload))
        response_data = response.json()
        assert response.status_code == 200


        assert response_data['responseCode'] == groups_data.get('group_with_same_name_different_description').get('responseCode')
        assert response_data['message'] == groups_data.get('group_with_same_name_different_description').get('message')

    def test_create_group_with_same_permissions(self, add_payload):
        logger.debug('Add groups : Add new group ')
        new_payload = dict(add_payload)
        new_payload['groupName'] = add_payload.get('groupName') + "_new"

        response = webservice.post(url=base_url + apis.add_group_info_endpoint, token=admin_token,
                                   data=json.dumps(new_payload))
        response_data = response.json()
        assert response.status_code == 200


        assert response_data['responseCode'] == groups_data.get('add_group_with_same_permissions').get('responseCode')
        assert response_data['message'] == groups_data.get('add_group_with_same_permissions').get('message') + " " + \
               add_payload.get('groupName') + "."

    """
    Edit Groups  Test cases

    """

    def test_EWA_1926_empty_authorization_token_editGroup(self, delete_after_add_group):
        logger.debug('Edit Groups : test empty authorization token')
        edit_group_url = base_url + apis.edit_group_info_endpoint + str(delete_after_add_group[0])
        response = webservice.put(url=edit_group_url, token='', data={})
        assert response.status_code == 401

    def test_EWA_1923_invalid_authorization_token_editGroup(self, delete_after_add_group):
        logger.debug('Edit Groups : test invalid authorization token')
        edit_group_url = base_url + apis.edit_group_info_endpoint + str(delete_after_add_group[0])

        response = webservice.put(url=edit_group_url, token='invalid token', data={})

        assert response.status_code == 401

    def test_EWA_1920_null_authorization_token_editGroup(self, delete_after_add_group):
        logger.debug('Edit Groups : test null authorization token')
        edit_group_url = base_url + apis.edit_group_info_endpoint + str(delete_after_add_group[0])

        response = webservice.put(url=edit_group_url, token=None, data={})

        assert response.status_code == 401



    def test_EWA_1910_edit_group_info(self, delete_after_add_group):

        logger.debug('Edit groups : test null authorization token')
        edit_group_url = base_url + apis.edit_group_info_endpoint + str(delete_after_add_group[0])
        edit_group_payload = groups_data.get('edit_group')
        response = webservice.put(url=edit_group_url, token=admin_token, data=json.dumps(edit_group_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == groups_data.get('edit_group_response').get('responseCode')
        assert response_data['message'] == groups_data.get('edit_group_response').get('message')
        #validate that the value has been edited as expected
        group_list_response = webservice.get(url=base_url + apis.group_list_endpoint, token=admin_token)
        group_list_response = group_list_response.json()['groups']
        result = utils.get_id_in_list(id=delete_after_add_group[0], lst=group_list_response, id_name="groupId")
        assert result['groupName'] == edit_group_payload['groupName']
        assert result['groupDescription'] == edit_group_payload['groupDescription']






    def test_EWA_1935_pass_deleted_group_id_toedit(self, delete_after_add_group):
        logger.debug('Edit groups : test null authorization token')
        #taking the last group from the group list which has to be deleted and deleting it in this test case
        edit_group_url = base_url + apis.edit_group_info_endpoint + str(len(delete_after_add_group)-1)
        #deleting the group which has to be edited, before editing it
        group_delete_url = base_url + apis.delete_group_endpoint + str(len(delete_after_add_group)-1)
        response = webservice.delete(url=group_delete_url, token=admin_token)
        assert response.status_code == 200
        edit_group_payload = groups_data.get('edit_group')
        response = webservice.put(url=edit_group_url, token=admin_token, data=json.dumps(edit_group_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == groups_data.get('edit_group_with_deleted_id_response').get('responseCode')
        assert response_data['message'] == groups_data.get('edit_group_with_deleted_id_response').get('message')

    def test_EWA_1936_pass_empty_payload_group_id_toedit(self, delete_after_add_group):
        logger.debug('Edit groups : Test with empty payload')
        edit_group_url = base_url + apis.edit_group_info_endpoint + str(delete_after_add_group[0])
        edit_group_payload = {}
        response = webservice.put(url=edit_group_url, token=admin_token,
                                  data=json.dumps(edit_group_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == groups_data.get('edit_group_response').get('responseCode')
        assert response_data['message'] == groups_data.get('edit_group_response').get('message')


    """
         Delete group  Test cases

         """

    def test_EWA_1922_invalid_authorization_token_deleteGroup(self, delete_after_add_group):
        logger.debug('Delete Groups : test invalid authorization token')
        group_delete_url = base_url + apis.delete_group_endpoint + str(len(delete_after_add_group) - 1)
        response = webservice.delete(url=group_delete_url, token=admin_token[::-1])
        assert response.status_code == 401

    def test_EWA_1919_null_authorization_token_deleteGroup(self, delete_after_add_group):
        logger.debug('Delete Groups : test null authorization token')
        group_delete_url = base_url + apis.delete_group_endpoint + str(len(delete_after_add_group) - 1)
        response = webservice.delete(url=group_delete_url, token=None)
        assert response.status_code == 401

    def test_EWA_2004_delete_group_id(self, delete_after_add_group):
        logger.debug('Delete Groups : Test delete group')
        group_delete_url = base_url + apis.delete_group_endpoint + str(len(delete_after_add_group) - 1)
        response = webservice.delete(url=group_delete_url, token=admin_token)
        assert response.status_code == 200

    def test_EWA_1925_empty_authorization_token_deleteGroup(self, delete_after_add_group):
        logger.debug('Delete Groups : test empty authorization token')
        group_delete_url = base_url + apis.delete_group_endpoint + str(delete_after_add_group[0])
        response = webservice.delete(url=group_delete_url, token=None)

        assert response.status_code == 401


    def test_EWA_1941_delete_group_with_deleted_id(self, delete_after_add_group):
        logger.debug('Delete Groups : test deleted group with deleted id')
        group_delete_url = base_url + apis.delete_group_endpoint + str(len(delete_after_add_group) - 1)
        response = webservice.delete(url=group_delete_url, token=admin_token)
        assert response.status_code == 200
        response = webservice.delete(url=group_delete_url, token=admin_token)
        response_data = response.json()
        assert response_data['responseCode'] == groups_data.get('delete_group_with_deleted_id_response').get(
            'responseCode')
        assert response_data['message'] == groups_data.get('delete_group_with_deleted_id_response').get('message')


    def test_EWA_1941_delete_group_with_deleted_id(self, delete_after_add_group):
        logger.debug('Delete Groups : test deleted group with deleted id')
        group_delete_url = base_url + apis.delete_group_endpoint + str(len(delete_after_add_group) - 1)
        response = webservice.delete(url=group_delete_url, token=admin_token)
        assert response.status_code == 200
        response = webservice.delete(url=group_delete_url, token=admin_token)
        response_data = response.json()
        assert response_data['responseCode'] == groups_data.get('delete_group_with_deleted_id_response').get('responseCode')
        assert response_data['message'] == groups_data.get('delete_group_with_deleted_id_response').get('message')

