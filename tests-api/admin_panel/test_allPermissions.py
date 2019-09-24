import pytest
import os
import json
from src import testlogger
from src import webservice
from src.setup import Setup_Library
from src import utils
from config import fwork
from src.dataReader import data
import pdb
# TO DO hardcoded to qa need to be made flexible
permissions_data = data().get_data("permissions_qa")

logger = testlogger.setup_custom_logger('ewa_admin')
setup_test = Setup_Library()


class TestPermissions(object):
    @pytest.fixture(scope='class')
    def admin_token(self):
        token = setup_test.get_admin_token()
        logger.debug("Token value %s" % (token))
        return token

    @pytest.fixture(scope='class')
    def test_setup(self):
        base_url = setup_test.data.login.base_url
        url = base_url + 'admin/permissions/allPermissions'
        logger.debug('base_urk: ' + base_url)
        permission_schema = os.path.join(fwork.IN_DATA_PATH, 'schema/permissions_schema.json')
        return {'url': url, 'schema': permission_schema}

    def test_validate_permissions_schema(self, test_setup, admin_token):
        logger.debug('Permissions: test_validate_permissions_schema')
        response = webservice.get(url=test_setup['url'], token=admin_token)
        logger.debug('Permissions: Validating json schema')
        utils.assert_valid_schema(response.json(), test_setup['schema'])

    def test_EWA_2013_pass_invalid_authorization_token(self, test_setup, admin_token):
        logger.debug('Permissions: test invalid authorization token')
        response = webservice.get(url=test_setup['url'], token=admin_token[::-1])  # reverse token
        assert response.status_code == 401

    def test_EWA_2012_pass_null_authorization_token(self, test_setup):
        logger.debug('Permissions: test_validate_permissions_schema')
        response = webservice.get(url=test_setup['url'], token=None)
        assert response.status_code == 401

    def test_EWA_2014_pass_empty_authorization_token(self, test_setup):
        logger.debug('Permissions: test invalid authorization token')
        response = webservice.get(url=test_setup['url'], token='')  # reverse token
        assert response.status_code == 401

    def test_EWA_2011_permission_data(self, test_setup, admin_token):
        logger.debug('Permissions: test_validate_permissions_schema')
        response = webservice.get(url=test_setup['url'], token=admin_token)
        response_data = response.json()
        permissions = utils.encode_to_ascii(response_data['permissions'])
        logger.debug('Permissions: Validating json data')
        assert response_data['message'].encode("ascii", "ignore") == permissions_data.get_all_permisssions.message
        assert permissions == permissions_data.get_all_permisssions.permissions
