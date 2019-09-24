import pytest
import os
from src import testlogger
from src import webservice
from src.setup import Setup_Library
from src import utils
from config import fwork
from src.dataReader import data

admin_data = data().get_data("hr_admin")

logger = testlogger.setup_custom_logger('ewa_admin')
setup_test = Setup_Library()
admin_token = setup_test.get_admin_token()
base_url = setup_test.data.login.base_url
apis = setup_test.data.apis
hr_token = setup_test.get_employee_token()



class TestHrAdminData(object):

    # schemas
    admin_schema = os.path.join(fwork.IN_DATA_PATH, admin_data.get('hr_admin_data_schema'))

    def test_EWA_6069_validate_groups_schema(self):
        logger.debug('HR Admin Data: test_validate_get_schema')
        response = webservice.get(url=base_url + apis.hr_admin_data_endpoint, token=hr_token)
        logger.debug('HR Admin Data: Validating json schema')
        utils.assert_valid_schema(response.json(), TestHrAdminData.admin_schema)


    def test_EWA_6070_non_hr_token(self):
        logger.debug('HR Admin Data: test invalid authorization token')
        response = webservice.get(url=base_url + apis.hr_admin_data_endpoint, token=admin_token)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == 401
        assert response_data['message'] == 'Permission denied'

    def test_EWA_6072_pass_invalid_authorization_token(self):
        logger.debug('HR Admin Data: test invalid authorization token')
        response = webservice.get(url=base_url + apis.hr_admin_data_endpoint, token=admin_token[::-1])
        assert response.status_code == 401

    def test_EWA_6071_pass_null_authorization_token(self):
        logger.debug('HR Admin Data:test_validate_permissions_schema')
        response = webservice.get(url=base_url + apis.hr_admin_data_endpoint, token=None)
        assert response.status_code == 401

    def test_EWA_6073_pass_empty_authorization_token(self):
        logger.debug('HR Admin Data: test invalid authorization token')
        response = webservice.get(url=base_url + apis.hr_admin_data_endpoint, token='')
        assert response.status_code == 401


