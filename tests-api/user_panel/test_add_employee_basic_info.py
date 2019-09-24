import pytest
import os
import json
from src import testlogger
from src import webservice
from src import employee_api_helper
from src.setup import Setup_Library
from src import utils
from config import fwork
from src.dataReader import data
import random


employee_basic_data = data().get_data("employee_basic")

logger = testlogger.setup_custom_logger('ewa_admin')
setup_test = Setup_Library()
admin_token = setup_test.get_admin_token()
hr_token = setup_test.get_employee_token()
base_url = setup_test.data.login.base_url
apis = setup_test.data.apis

class TestEmployeeBasicData(object):

    @pytest.fixture(scope='class')
    def delete_user(self, request):
        users_added = []

        def cleanup():
            for email in users_added:
                remove_user = apis.remove_user_endpoint + email
                webservice.delete(url=base_url + remove_user, token=admin_token)
                logger.debug( " User Deleted ..." + email)

        request.addfinalizer(cleanup)
        return users_added



    def test_EWA_150_to_validate_add_user_api(self, delete_user):
        logger.debug('Employee Data: add user validation')
        employee_payload = employee_api_helper.generate_employee_data()

        files = {"image" : ("duck.png", (open(os.path.join(fwork.IN_DATA_PATH,"images/duck.png"),"rb")))}
        response = webservice.post(url=base_url + apis.employee_basic_data_endpoint,data=employee_payload, files=files,
                                   token=hr_token, headers={})

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == employee_basic_data.get('add_employee_response').get('responseCode')
        assert response_data['message'] == employee_basic_data.get('add_employee_response').get('message')
        delete_user.append(employee_payload['emailId'])

    def test_EWA_151_add_duplicate_user(self, delete_user):

        employee_payload = employee_api_helper.generate_employee_data()
        employee_payload['emailId'] = delete_user[0]
        files = {"image" : ("duck.png", (open(os.path.join(fwork.IN_DATA_PATH,"images/duck.png"),"rb")))}
        response = webservice.post(url=base_url + apis.employee_basic_data_endpoint,data=employee_payload, files=files,
                                   token=hr_token, headers={})

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == employee_basic_data.get('add_duplicate_user').get('responseCode')
        assert response_data['message'] == employee_basic_data.get('add_duplicate_user').get('message')


    def test_EWA_159_check_for_mandatory_fields(self, delete_user):

        employee_payload = employee_api_helper.generate_employee_data()
        employee_payload['emailId'] = delete_user[0]
        employee_payload['jobLocation'] = None
        files = {"image" : ("duck.png", (open(os.path.join(fwork.IN_DATA_PATH,"images/duck.png"),"rb")))}
        response = webservice.post(url=base_url + apis.employee_basic_data_endpoint,data=employee_payload, files=files,
                                   token=hr_token, headers={})

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['message'] == employee_basic_data.get('missing_fields').get('message')

    def test_EWA_710_check_for_missing_email(self):

        employee_payload = employee_api_helper.generate_employee_data()
        employee_payload['emailId'] = None
        files = {"image" : ("duck.png", (open(os.path.join(fwork.IN_DATA_PATH,"images/duck.png"),"rb")))}
        response = webservice.post(url=base_url + apis.employee_basic_data_endpoint,data=employee_payload, files=files,
                                   token=hr_token, headers={})

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['message'] == employee_basic_data.get('missing_fields').get('message')


    def test_EWA_3113_pass_non_hr_token(self):
        '''

            Sending admin token instead of hr token. Admin token should not have permission to add users.

        :return:
        '''
        employee_payload = employee_api_helper.generate_employee_data()
        files = {"image": ("duck.png", (open(os.path.join(fwork.IN_DATA_PATH, "images/duck.png"), "rb")))}
        response = webservice.post(url=base_url + apis.employee_basic_data_endpoint, data=employee_payload, files=files,
                                   token=admin_token, headers={})

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == employee_basic_data.get('non_admin_token_response').get('responseCode')
        assert response_data['message'] == employee_basic_data.get('non_admin_token_response').get('message')


    def test_EWA_3114_check_grades_incorrect_value(self, delete_user):
        employee_payload = employee_api_helper.generate_employee_data()
        employee_payload['emailId'] = delete_user[0]
        employee_payload['selectedGrade'] = random.randint(1000,2000)
        files = {"image": ("duck.png", (open(os.path.join(fwork.IN_DATA_PATH, "images/duck.png"), "rb")))}
        response = webservice.post(url=base_url + apis.employee_basic_data_endpoint, data=employee_payload, files=files,
                                   token=hr_token, headers={})

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == employee_basic_data.get('incorrect_grade_value').get('responseCode')

        assert response_data['message'] == employee_basic_data.get('incorrect_grade_value').get('message')


    def test_EWA_3114_check_groups_incorrect_value(self, delete_user):
        employee_payload = employee_api_helper.generate_employee_data()
        employee_payload['emailId'] = delete_user[0]
        employee_payload['selectedGroups'] =str([ random.randint(1000,2000)]) # array has to passed as a string
        files = {"image": ("duck.png", (open(os.path.join(fwork.IN_DATA_PATH, "images/duck.png"), "rb")))}
        response = webservice.post(url=base_url + apis.employee_basic_data_endpoint, data=employee_payload, files=files,
                                   token=hr_token, headers={})

        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == employee_basic_data.get('incorrect_group_value').get('responseCode')
        assert response_data['message'] == employee_basic_data.get('incorrect_group_value').get('message')

    def test_EWA__pass_invalid_authorization_token(self):
        logger.debug('Employee Data: test invalid authorization token')
        employee_payload = employee_api_helper.generate_employee_data()
        files = {"image": ("duck.png", (open(os.path.join(fwork.IN_DATA_PATH, "images/duck.png"), "rb")))}
        response = webservice.post(url=base_url + apis.employee_basic_data_endpoint, data=employee_payload, files=files,
                                   token=admin_token[::-1], headers={})

        assert response.status_code == 401

