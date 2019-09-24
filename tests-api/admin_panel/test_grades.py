import os
from src import testlogger
from src import webservice
from src.setup import Setup_Library
from src import utils
from config import fwork
from src.dataReader import data
import json
import pytest

logger = testlogger.setup_custom_logger('ewa_admin')
setup_test = Setup_Library()
admin_token = setup_test.get_admin_token()
base_url = setup_test.data.login.base_url
apis = setup_test.data.apis

grades_data = data().get_data("grades")


class TestGradesApi(object):
    """
            Fixtures for the Grades test


    """

    # schemas
    grades_schema = os.path.join(fwork.IN_DATA_PATH, grades_data.get('grades_list_schema'))

    @pytest.fixture(scope='class')
    def delete_after_add_grade(self, request):

        grades_added = []

        def cleanup():
            for grade_id in grades_added:
                grade_delete_url = base_url + apis.delete_grade_endpoint + str(grade_id)
                webservice.delete(url=grade_delete_url, token=admin_token)
                print " Grade Deleted ..."

        request.addfinalizer(cleanup)
        return grades_added

    @pytest.fixture(params=grades_data.get('add_grade'))
    def add_payload(self, request):
        return request.param

    """
                    Get Grade List Test cases

    """

    def test_validate_gradess_schema(self):
        logger.debug('Grade List: test_validate_gradess_schema')
        response = webservice.get(url=base_url + apis.grade_list_endpoint, token=admin_token)
        logger.debug('Grades: Validating json schema')
        utils.assert_valid_schema(response.json(), TestGradesApi.grades_schema)

    def test_EWA_1898_pass_invalid_authorization_token(self):
        logger.debug('Grade List: test invalid authorization token')
        response = webservice.get(url=base_url + apis.grade_list_endpoint, token=admin_token[::-1])  # reverse token
        assert response.status_code == 401

    def test_EWA_1899_pass_null_authorization_token(self):
        logger.debug('Grade List: test_validate_Grades_schema')
        response = webservice.get(url=base_url + apis.grade_list_endpoint, token=None)
        assert response.status_code == 401

    def test_EWA_1897_pass_empty_authorization_token(self):
        logger.debug('Grade List: test invalid authorization token')
        response = webservice.get(url=base_url + apis.grade_list_endpoint, token='')

        assert response.status_code == 401

    """
                    Add Grade  Test cases

    """

    def test_EWA_1900_empty_authorization_token_addNew(self):
        logger.debug('Add Grades : test empty authorization token')
        response = webservice.post(url=base_url + apis.add_grade_info_endpoint, token='', data={})
        assert response.status_code == 401

    def test_EWA_1903_invalid_authorization_token_addNew(self):
        logger.debug('Add Grades : test invalid authorization token')
        response = webservice.post(url=base_url + apis.add_grade_info_endpoint, token='invalidToken', data={})
        assert response.status_code == 401

    def test_EWA_1906_null_authorization_token_addNew(self):
        logger.debug('Add Grades : test null authorization token')
        response = webservice.post(url=base_url + apis.add_grade_info_endpoint, token=None, data={})
        assert response.status_code == 401

    def test_EWA_1893_1928__add_new_grade(self, add_payload, delete_after_add_grade):

        logger.debug('Add Grades : Add new grade ')
        response = webservice.post(url=base_url + apis.add_grade_info_endpoint, token=admin_token,
                                   data=json.dumps(add_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == grades_data.get('add_grade_response').get('responseCode')
        assert response_data['message'] == grades_data.get('add_grade_response').get('message')
        delete_after_add_grade.append(response_data['gradeInfo']['gradeId'])

    # @pytest.mark.skip('Test case is failing now will create dirty data')
    def test_EWA_2020_create_grade_with_same_name(self, add_payload):
        logger.debug('Add grades : Add new grade ')
        if isinstance(add_payload['gradeDescription'], int) or add_payload['gradeDescription'] == None:
            pytest.skip("Adding grade with same integer or None is not correct data")
        response = webservice.post(url=base_url + apis.add_grade_info_endpoint, token=admin_token,
                                   data=json.dumps(add_payload))
        response_data = response.json()
        assert response.status_code == 200

        assert response_data['responseCode'] == grades_data.get('add_grade_with_same_name').get('responseCode')
        assert response_data['message'] == grades_data.get('add_grade_with_same_name').get('message')

    # @pytest.mark.skip('Test case is failing now will create dirty data')
    def test_EWA_2021_create_grade_with_same_name_different_description(self, add_payload):
        logger.debug('Add grades : Add new grade ')
        new_payload = dict(add_payload)

        if isinstance(new_payload['gradeDescription'], int) or new_payload['gradeDescription'] == None:
            pytest.skip("Adding grade with same integer or None is not correct data")
        new_payload['gradeDescription'] = new_payload['gradeDescription'] + '_new'
        response = webservice.post(url=base_url + apis.add_grade_info_endpoint, token=admin_token,
                                   data=json.dumps(new_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == grades_data.get('grade_with_same_name_different_description').get(
            'responseCode')
        assert response_data['message'] == grades_data.get('grade_with_same_name_different_description').get('message')

    """
    Edit Grade  Test cases

    """

    def test_EWA_1901_empty_authorization_token_editGrade(self, delete_after_add_grade):
        logger.debug('Edit Grades : test empty authorization token')
        edit_grade_url = base_url + apis.edit_grade_info_endpoint + str(delete_after_add_grade[0])
        response = webservice.put(url=edit_grade_url, token='', data={})
        assert response.status_code == 401

    def test_EWA_1904_invalid_authorization_token_editGrade(self, delete_after_add_grade):
        logger.debug('Edit Grades : test invalid authorization token')
        edit_grade_url = base_url + apis.edit_grade_info_endpoint + str(delete_after_add_grade[0])

        response = webservice.put(url=edit_grade_url, token='invalid token', data={})
        assert response.status_code == 401

    def test_EWA_1907_null_authorization_token_editGrade(self, delete_after_add_grade):
        logger.debug('Edit Grades : test null authorization token')
        edit_grade_url = base_url + apis.edit_grade_info_endpoint + str(delete_after_add_grade[0])
        response = webservice.put(url=edit_grade_url, token=None, data={})
        assert response.status_code == 401

    def test_EWA_1894_edit_grade_info(self, delete_after_add_grade):
        logger.debug('Edit Grades : test null authorization token')
        edit_grade_url = base_url + apis.edit_grade_info_endpoint + str(delete_after_add_grade[0])
        edit_grade_payload = grades_data.get('edit_grade')
        response = webservice.put(url=edit_grade_url, token=admin_token, data=json.dumps(edit_grade_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == grades_data.get('edit_grade_response').get('responseCode')
        assert response_data['message'] == grades_data.get('edit_grade_response').get('message')

    def test_EWA_1930_edit_deleted_id_to_edit_gradeinfo(self, delete_after_add_grade):
        logger.debug('Edit Grades : test null authorization token')
        # taking the last grade from the grade list which has to be deleted and deleting it in this test case
        edit_grade_url = base_url + apis.edit_grade_info_endpoint + str(len(delete_after_add_grade) - 1)
        # deleting the grade which has to be edited, before editing it
        grade_delete_url = base_url + apis.delete_grade_endpoint + str(len(delete_after_add_grade) - 1)
        response = webservice.delete(url=grade_delete_url, token=admin_token)
        assert response.status_code == 200
        edit_grade_payload = grades_data.get('edit_grade')
        response = webservice.put(url=edit_grade_url, token=admin_token, data=json.dumps(edit_grade_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == grades_data.get('edit_grade_with_deleted_id_response').get(
            'responseCode')
        assert response_data['message'] == grades_data.get('edit_grade_with_deleted_id_response').get('message')

    def test_EWA_1933_pass_empty_payload_edit_gradeinfo(self, delete_after_add_grade):
        logger.debug('Edit Grades : Test with empty payload')
        edit_grade_url = base_url + apis.edit_grade_info_endpoint + str(delete_after_add_grade[0])
        edit_grade_payload = {}
        response = webservice.put(url=edit_grade_url, token=admin_token,
                                  data=json.dumps(edit_grade_payload))
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['responseCode'] == grades_data.get('edit_grade_response').get('responseCode')
        assert response_data['message'] == grades_data.get('edit_grade_response').get('message')

        """
       Delete Grade  Test cases

       """

    def test_EWA_1905_invalid_authorization_token_deleteGrade(self, delete_after_add_grade):
        logger.debug('Delete Grades : test invalid authorization token')
        grade_delete_url = base_url + apis.delete_grade_endpoint + str(len(delete_after_add_grade) - 1)
        response = webservice.delete(url=grade_delete_url, token=admin_token[::-1])
        assert response.status_code == 401

    def test_EWA_1908_null_authorization_token_deleteGrade(self, delete_after_add_grade):
        logger.debug('Delete Grades : test null authorization token')
        grade_delete_url = base_url + apis.delete_grade_endpoint + str(len(delete_after_add_grade) - 1)
        response = webservice.delete(url=grade_delete_url, token=None)
        assert response.status_code == 401

    def test_EWA_1939_1995_delete_grade_id(self, delete_after_add_grade):
        logger.debug('Delete Grades : Test delete grade')
        grade_delete_url = base_url + apis.delete_grade_endpoint + str(len(delete_after_add_grade) - 1)
        response = webservice.delete(url=grade_delete_url, token=admin_token)
        assert response.status_code == 200

    def test_EWA_1902_empty_authorization_token_deleteGrade(self, delete_after_add_grade):
        logger.debug('Delete Grades : test empty authorization token')
        grade_delete_url = base_url + apis.delete_grade_endpoint + str(delete_after_add_grade[0])
        response = webservice.delete(url=grade_delete_url, token=None)
        assert response.status_code == 401

    def test_EWA_1940_delete_grade_with_deleted_id(self, delete_after_add_grade):
        logger.debug('Delete Grades : test deleted grade with deleted id')
        grade_delete_url = base_url + apis.delete_grade_endpoint + str(len(delete_after_add_grade) - 1)
        response = webservice.delete(url=grade_delete_url, token=admin_token)
        assert response.status_code == 200
        response = webservice.delete(url=grade_delete_url, token=admin_token)
        response_data = response.json()
        assert response_data['responseCode'] == grades_data.get('delete_grade_with_deleted_id_response').get(
            'responseCode')
        assert response_data['message'] == grades_data.get('delete_grade_with_deleted_id_response').get('message')
