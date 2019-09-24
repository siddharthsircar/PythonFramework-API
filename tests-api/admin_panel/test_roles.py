import pytest
import os
from src import testlogger
from src import webservice
from src.setup import Setup_Library
from src import utils
from src import roles_helper
from config import fwork
from src.dataReader import data
import json

logger = testlogger.setup_custom_logger('ewa_admin')
setup_test = Setup_Library()
roles_data = data().get_data("roles")
base_url = setup_test.data.login.base_url
apis = setup_test.data.apis
admin_token = setup_test.get_admin_token()
non_admin_token=setup_test.get_employee_token()

class TestRolesApi(object):
    """
            Fixtures for the Roles test

    """
    roles_schema = os.path.join(fwork.IN_DATA_PATH, roles_data.get('roles_list_schema'))

    @pytest.fixture(scope='class')
    def delete_after_add_role(self, request):
        roles_added = []

        def cleanup():
            for roles_id in roles_added:
                role_delete_url = base_url + apis.delete_role_endpoint + str(roles_id)
                webservice.delete(url=role_delete_url, token=admin_token)
                print " Role Deleted ..."
        request.addfinalizer(cleanup)
        return roles_added

    @pytest.fixture(params=roles_data.get('add_role'))
    def add_payload(self, request):
        return request.param

    """
                    add roles List Test cases

    """

    # def test_validate_Roles_schema(self):
    #     logger.debug('roles List: test_validate_Roles_schema')
    #     response = webservice.get(url=base_url + apis.role_list_endpoint, token=admin_token)
    #     logger.debug('Roles: Validating json schema')
    #     utils.assert_valid_schema(response.json(), TestRolesApi.roles_schema)


    def test_1976_add_new_role(self,delete_after_add_role):
        logger.debug('Add roles : Add new Roles ')
        payload=roles_helper.generate_role_data()
        response = webservice.post(url=base_url + apis.add_role_info_endpoint, token=admin_token, data=json.dumps(payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == roles_data.get('add_role_response').get('responseCode')
        assert response_data['message'] == roles_data.get('add_role_response').get('message')
        delete_after_add_role.append(response_data['roleInfo']['roleId'])


    def test_9221_create_role_same_role(self):
        logger.debug('Add roles : creating same roles ')
        payload_same_role = roles_helper.generate_role_data()
        response = webservice.post(url=base_url + apis.add_role_info_endpoint, token=admin_token,
                                   data=json.dumps(payload_same_role))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == roles_data.get('add_role_with_same_name').get('responseCode')
        assert response_data['message'] == roles_data.get('add_role_with_same_name').get('message')

    def test_EWA_6076_Pass_non_org_admin_to_addRole(self):
        logger.debug('Pass non_Org_admin token:to create same roles')
        response = webservice.post(url=base_url + apis.add_role_info_endpoint, token=non_admin_token,
                                   data={})
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == roles_data.get('non_admin_token_response').get('responseCode')
        assert response_data['message'] == roles_data.get('non_admin_token_response').get('message')

    def test_6075_Pass_inncorrect_group_ID_to_addRole(self):

        logger.debug('Pass incorrect Group ID:to create same roles')
        add_paylod_nongroup_existence = roles_data.get('add_incorrect_Group_ID')

        response = webservice.post(url=base_url + apis.add_role_info_endpoint, token=admin_token,
                                   data=json.dumps(add_paylod_nongroup_existence))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == roles_data.get('pass_non_existence_roleGroup_Id').get('responseCode')
        assert response_data['message'] == roles_data.get('pass_non_existence_roleGroup_Id').get('message')

    def test_1969_Pass_null_authorization_token(self):
        logger.debug('Pass non_Org_admin token:to create same roles')
        response = webservice.post(url=base_url + apis.add_role_info_endpoint, token=None,
                                   data={})
        assert response.status_code == 401

    def test_1969_Pass_invalid_authorization_token(self):
        logger.debug('Pass non_Org_admin token:to create same roles')
        response = webservice.post(url=base_url + apis.add_role_info_endpoint, token='invalid token',
                                   data={})
        assert response.status_code == 401




    def test_1965_get_all_roles(self,delete_after_add_role):
        roles_get_payload=roles_helper.get_roleList()
        logger.debug('get Roles : get all roles accessed')
        group_id = roles_helper.get_group_list()[0]
        get_roles_list_url = base_url + apis.roles_list_enpoint + "group=" + (str(group_id['groupId']))
        role_list_response = webservice.get(url=get_roles_list_url, token=admin_token)
        role_list_response = role_list_response.json()['rolesList']
        result = utils.get_id_in_list(id=delete_after_add_role[0], lst=role_list_response, id_name="roleId")
        assert result['roleName'] == roles_get_payload['roleName']
        assert result['roleDescription'] == roles_get_payload['roleDescription']



    def test_1980_getAllRoles_passing_empty_token(self):
        logger.debug('get Roles : get all roles accessed by passing Empty Token')
        group_id = roles_helper.get_group_list()[0]
        get_roles_url = base_url + apis.roles_list_enpoint + "group=" + (str(group_id['groupId']))
        response = webservice.get(url=get_roles_url, token=None)
        assert response.status_code == 401

    def test_1981_passing_non_admin_token(self) :
        logger.debug('get Roles : get all roles accessed by passing Empty Token')
        group_id = roles_helper.get_group_list()[0]
        get_roles_url = base_url + apis.roles_list_enpoint + "group=" + (str(group_id['groupId']))
        response = webservice.get(url=get_roles_url, token=non_admin_token)
        response_data=response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] ==roles_data.get('non_admin_token_response').get('responseCode')
        assert response_data['message'] == roles_data.get('non_admin_token_response').get('message')


    def test_1982_pass_null_authorization_token(self):
        logger.debug('get Roles : get all roles accessed by passing Empty Token')
        group_id = roles_helper.get_group_list()[0]
        get_roles_url = base_url + apis.roles_list_enpoint + "group=" + (str(group_id['groupId']))
        response = webservice.get(url=get_roles_url, token='invalid token')
        assert response.status_code == 401


    def test_1967_Edit_role_description(self,delete_after_add_role):
        logger.debug('Edit Roles : by changing the Role name')
        edit_role_url = base_url + apis.edit_role_endpoint + str(delete_after_add_role[0])
        edit_role_payload = roles_helper.edit_role_data()
        response = webservice.put(url=edit_role_url, token=admin_token, data=json.dumps(edit_role_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == roles_data.get('edit_role_response').get('responseCode')
        assert response_data['message'] == roles_data.get('edit_role_response').get('message')
        group_id = roles_helper.get_group_list()[0]
        get_roles_list_url = base_url + apis.roles_list_enpoint + "group=" + (str(group_id['groupId']))
        role_list_response = webservice.get(url=get_roles_list_url, token=admin_token)
        role_list_response = role_list_response.json()['rolesList']
        result = utils.get_id_in_list(id=delete_after_add_role[0], lst=role_list_response, id_name="roleId")
        assert result['roleName'] == edit_role_payload['roleName']
        assert result['roleDescription'] == edit_role_payload['roleDescription']


    def test_1968_pass_null_authorization_editRole(self,delete_after_add_role):
        logger.debug('Edit Roles : by changing the Role name')
        edit_role_url = base_url + apis.edit_role_endpoint + str(delete_after_add_role[0])
        edit_role_payload = roles_helper.edit_role_data()
        response = webservice.put(url=edit_role_url, token=None, data=json.dumps(edit_role_payload))
        assert response.status_code == 401

    def test_1971_pass_invalid_authorization_editRole(self,delete_after_add_role):
        logger.debug('Edit Roles : by changing the Role name')
        edit_role_url = base_url + apis.edit_role_endpoint + str(delete_after_add_role[0])
        edit_role_payload = roles_helper.edit_role_data()
        response = webservice.put(url=edit_role_url, token='invalid token', data=json.dumps(edit_role_payload))
        assert response.status_code == 401

    def test_1974_pass_empty_authorization_editRole(self,delete_after_add_role):
        logger.debug('Edit Roles : by changing the Role name')
        edit_role_url = base_url + apis.edit_role_endpoint + str(delete_after_add_role[0])
        edit_role_payload = roles_helper.edit_role_data()
        response = webservice.put(url=edit_role_url, token='', data=json.dumps(edit_role_payload))
        assert response.status_code == 401

    def test_automation_pass_non_admin_authorization_editRole(self,delete_after_add_role):
        logger.debug('Edit Roles : by changing the Role name')
        edit_role_url = base_url + apis.edit_role_endpoint + str(delete_after_add_role[0])
        edit_role_payload = roles_helper.edit_role_data()
        response = webservice.put(url=edit_role_url, token=non_admin_token, data=json.dumps(edit_role_payload))
        response_data=response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == roles_data.get('non_admin_token_response').get('responseCode')
        assert response_data['message'] == roles_data.get('non_admin_token_response').get('message')

    def test_1984_pass_deletedID_to_editRole(self,delete_after_add_role):
        logger.debug('Edit roless : test null authorization token')
        # taking the last role from the role list which has to be deleted and deleting it in this test case
        edit_role_url = base_url + apis.edit_role_endpoint + str(len(delete_after_add_role) - 1)
        # deleting the roles which has to be edited, before editing it
        role_delete_url = base_url + apis.delete_role_endpoint + str(len(delete_after_add_role) - 1)
        response = webservice.delete(url=role_delete_url, token=admin_token)
        assert response.status_code == 200
        edit_role_payload = roles_data.get('edit_role')
        response = webservice.put(url=edit_role_url, token=admin_token, data=json.dumps(edit_role_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == roles_data.get('edit_role_with_deleted_id_response').get(
            'responseCode')
        assert response_data['message'] == roles_data.get('edit_role_with_deleted_id_response').get('message')



    """
         Delete group  Test cases

         """

    def test_EWA_1970_invalid_authorization_token_deleterole(self, delete_after_add_role):
        logger.debug('Delete roles : test invalid authorization token')
        role_delete_url = base_url + apis.delete_role_endpoint + str(len(delete_after_add_role) - 1)
        response = webservice.delete(url=role_delete_url, token=admin_token[::-1])
        assert response.status_code == 401

    def test_EWA_1966_pass_null_authorization_token_deleterole(self, delete_after_add_role):
        logger.debug('Delete roles : test invalid authorization token')
        role_delete_url = base_url + apis.delete_role_endpoint + str(len(delete_after_add_role) - 1)
        response = webservice.delete(url=role_delete_url, token=None)
        assert response.status_code == 401

    def test_EWA_1987_delete_rol_with_deleted_id(self, delete_after_add_role):
        logger.debug('Delete roless : test deleted role with deleted id')
        role_delete_url = base_url + apis.delete_role_endpoint + str(len(delete_after_add_role) - 1)
        response = webservice.delete(url=role_delete_url, token=admin_token)
        assert response.status_code == 200
        response = webservice.delete(url=role_delete_url, token=admin_token)
        response_data = response.json()
        assert response_data['responseCode'] == roles_data.get('delete_role_with_deleted_id_response').get(
            'responseCode')
        assert response_data['message'] == roles_data.get('delete_role_with_deleted_id_response').get('message')


    def test_EWA_1978_delete_role_id(self, delete_after_add_role):
        logger.debug('Delete Groups : Test delete group')
        role_delete_url = base_url + apis.delete_role_endpoint + str(len(delete_after_add_role) - 1)
        response = webservice.delete(url=role_delete_url, token=admin_token)
        assert response.status_code == 200