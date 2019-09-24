import optparse
import os
import time

usage = """Usage: %prog [options]"""
from config import fwork
import os


class Configuration:
    """
    Base class for Command Line Interface .
    """

    def __init__(self, options, args):
        self.options = options
        self.args = args


def get_options():
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-d', "--tests_dir", dest='tests_dir',
                      default=fwork.TESTS_DIR,
                      help='Parent directory of test case modules. Default: As per fwork.py')
    parser.add_option('-k', "--input_dir", dest='input_dir',
                      default=fwork.IN_DATA_PATH,
                      help='Parent directory of input files. Default: As per fwork.py')
    parser.add_option('-q', "--quiet", dest='quiet', action='store_true',
                      default=False,
                      help='Switch off debug log messages')
    parser.add_option('-l', "--log_to_file", dest='log_to_file', action='store_true',
                      default=False,
                      help='Log to file instead of console')
    parser.add_option('-c', "--config_file", dest='config',
                      default=os.path.join(fwork.CONFIG_DIR, 'topo_qa.yaml'),
                      help='Config file to be used for the run')
    cmd, args = parser.parse_args()
    config = Configuration(cmd, args)
    return config
