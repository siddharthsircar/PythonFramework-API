import sys
import os

from src.dataReader import data
from config import fwork
import src.webservice

dat = data()
data().create_data()


class Setup_Library(object):

    def __init__(self):
        if os.getenv('DEV')=='dev':
            self.data = dat.get_data('topo_dev')
        elif os.getenv('QA')=='qa':
            self.data = dat.get_data('topo_qa')
        self.admin_token = self.fetch_token(self.data.get('admin'))
        self.employee_token = self.fetch_token(self.data.get('employee'))

    def fetch_token(self, login_values = None, email=None, password=None):
        if login_values:
            email = login_values['email']
            password =login_values['password']

        token = src.webservice.get_token(self.data.get('login').get('base_url') + 'login', email, password)
        return token

    def get_admin_token(self):
        """
        :rtype:
        """
        return self.admin_token

    def get_employee_token(self):
        return self.employee_token