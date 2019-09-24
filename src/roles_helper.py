
from src.dataReader import data
from src.setup import Setup_Library
from src import testlogger
import webservice


roles_data = data().get_data('roles')
setup_test = Setup_Library()
apis = setup_test.data.apis
base_url = setup_test.data.login.base_url
admin_token = setup_test.get_admin_token()
hr_token = setup_test.get_employee_token()
logger = testlogger.setup_custom_logger('ewa_admin')

def get_group_list():
    logger.debug('group List: Get group List')
    response = webservice.get(url=base_url + apis.group_list_endpoint, token=admin_token)
    logger.debug('Groups: Validating json schema')
    response_data = response.json()
    group_id_list=response_data['groups']
    return group_id_list

def generate_role_data():
    new_role_data = roles_data.get('add_new_role')
    logger.debug(new_role_data)
    new_role_data['roleName'] = 'AddingroleFromAutomation'
    new_role_data['roleDescription'] = 'Automation group Test Case'
    group_dict=get_group_list()[0]
    new_role_data['roleGroup'] = str(group_dict['groupId'])
    new_role_data['permissions'] = group_dict['permissions']
    return new_role_data



def get_roleList():
    new_role_data = roles_data.get('add_new_role')
    new_role_data['roleName'] = 'AddingroleFromAutomation'
    new_role_data['roleDescription'] = 'Automation group Test Case'
    group_dict = get_group_list()[0]
    #new_role_data['roleGroup'] = str(group_dict['groupId'])
    new_role_data['permissions'] = group_dict['permissions']
    return new_role_data

def edit_role_data() :
    new_role_data = roles_data.get('edit_role')
    logger.debug('edit_role')
    new_role_data['roleName'] = 'Edited_AddingroleFromAutomation'
    new_role_data['roleDescription'] = 'Edited_Automation group Test Case'
    group_dict = get_group_list()[0]
    new_role_data['roleGroup'] = str(group_dict['groupId'])
    new_role_data['permissions'] = group_dict['permissions']
    return new_role_data







