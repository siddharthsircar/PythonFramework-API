import sys
import os
import pytest
fwork_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(fwork_path)
from src import testlogger
from config import fwork
from src.setup import Setup_Library
from config import command
pytest_paramters = ['--html=report.html', '--junit-xml=output.xml']

config = command.get_options()

if not config.options.quiet:
    logger = testlogger.setup_custom_logger('ewa_api', 'debug')
else:
    logger = testlogger.setup_custom_logger('ewa_api', 'info')

if 'qa' in config.options.config:
    os.environ["QA"] = 'qa'
else:
    os.environ["DEV"] = 'dev'

logger.debug("TestRunner: Set Up")
setup_data = Setup_Library()
logger.debug("Test Run:: Begin")
pytest_paramters.append(fwork.TESTS_DIR)

#pytest_paramters.append('-k ' + 'test_Company_address')

pytest.main(pytest_paramters)

