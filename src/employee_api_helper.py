import random
from src.dataReader import data
from datetime import datetime
from src.setup import Setup_Library
from src import testlogger
import webservice
import utils
import json

employee_data = data().get_data('employee_basic')
setup_test = Setup_Library()
apis = setup_test.data.apis
base_url = setup_test.data.login.base_url
admin_token = setup_test.get_admin_token()
hr_token = setup_test.get_employee_token()
logger = testlogger.setup_custom_logger('ewa_admin')

# firstName: Test
#     lastName:  Automation
#     dateOfBirth: 01-01-1970
#     fatherName: Senion Automation
#     sex: Female
#     designation: Automation Engineer
#     selectedGrade:
#     dateOfJoining: 02-02-2015
#     selectedGroups: [Groups1, Groups2]
#     jobLocation: Noida
#     reportingManager: email@email.com
#     reportingManagerHR: email@email.com
#     reportingManagerFinance: email@email.com
#     emailId: test_automation@email.com
#     contactNumber: 1234567890
#     image: image

def generate_employee_data():
    new_employee_data = employee_data.get('add_employee_basic_info')
    logger.debug(new_employee_data)
    new_employee_data['lastName'] = "".join(random.sample(['Auto1', 'Auto2', 'Auto3'],1))
    new_employee_data['firstName'] = "".join(random.sample(['Test', 'Test1', 'Test2'],1))
    new_employee_data['fatherName'] = "".join(random.sample(['Trey', 'May', 'Prat'],1))
    new_employee_data['dateOfBirth'] = str(utils.convert_time_in_milliseconds(new_employee_data['dateOfBirth']))
    new_employee_data['sex'] = "".join(random.sample(['Male','Female'],1))
    new_employee_data['designation'] = 'Lead'

    new_employee_data['dateOfJoining'] = str(datetime.now().microsecond * 1000)
    new_employee_data['selectedGrade'] = str(get_grade())
    new_employee_data['selectedGroups'] = str(get_group())
    new_employee_data['jobLocation']   = str(get_job_location())
    new_employee_data['reportingManager'] = setup_test.data.admin.email
    new_employee_data['reportingManagerHR'] = setup_test.data.admin.email
    new_employee_data['reportingManagerFinance'] =setup_test.data.admin.email
    new_employee_data['emailId']                 = new_employee_data['lastName'] +  new_employee_data['firstName'] \
                                                   + '@celsysemail.celsyswtc.in'
    new_employee_data['contactNumber'] = generate_phone_number()
    logger.debug(new_employee_data)

    return new_employee_data


def get_grade():

    response = webservice.get(url=base_url +apis.grade_list_endpoint, token=admin_token)
    response_data = response.json()
    if response.status_code == 200:
        grades_list = response_data['grades']
        grade = random.sample(grades_list, 1)
        return grade[0]['gradeId']



def get_group(num=1):
    group_id_list = []
    response = webservice.get(url=base_url + apis.group_list_endpoint, token=admin_token)
    response_data = response.json()
    if response.status_code == 200:
        group_list = response_data['groups']
        grade = random.sample(group_list, num)
        group_id_list.append(grade[0]['groupId'])
        return group_id_list


def get_job_location():

    response = webservice.get(url=base_url+ apis.org_address_list_endpoint, token=admin_token)
    response_data = response.json()
    if response.status_code == 200:
        org_address_list = response_data['adresses']
        grade = random.sample(org_address_list, 1)
        return grade[0]['addressId']


def generate_phone_number():
    """ Generate 10 digit random phone number as a string"""

    phone_number = "".join([str(x) for x in random.sample(xrange(0,10),10)])
    if phone_number.startswith('0'):
        phone_number = generate_phone_number()
    return phone_number


