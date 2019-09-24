import pytest
import os
import json
from src import testlogger
from src import webservice
from src.setup import Setup_Library
from src import utils
from config import fwork
from src.dataReader import data
# TO DO hardcoded to qa need to be made flexible
permissions_data = data().get_data("permissions_qa")

logger = testlogger.setup_custom_logger('ewa_admin')
setup_test = Setup_Library()

# @pytest.fixture
# def admin_token():
#     token = setup_test.get_admin_token()
#     logger.debug("Token value %s" % (token))
#     return token

