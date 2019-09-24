import os
import logging
import datetime

from config import fwork
root_dir = os.path.dirname(os.path.abspath('ewa_api'))
log_dir = fwork.LOG_DIR

def setup_custom_logger(name, loglevel=None):
    # Create directory if not present
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # create logger
    logger = logging.getLogger(name)
    logger.propagate = False
    if not loglevel or loglevel.lower()=='debug':
        logger.setLevel(logging.DEBUG)

    else:
        if loglevel.lower() == 'info':
            logger.setLevel(logging.INFO)

    # add a file handler
    now = datetime.datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(os.path.join(log_dir, 'apitestinfo_%s.log' % now))
    file_handler.setLevel(logging.DEBUG)  # ensure all messages are logged to file

    # create a formatter and set the formatter for the handler.
    #formatter = logging.Formatter("%(asctime)s.%(msecs)d,%(name)s,%(message)s", "%Y-%m-%d,%H:%M:%S")
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s][%(funcName)s][%(name)s:%(lineno)d)] %(message)s')

    file_handler.setFormatter(formatter)

    # add the Handler to the logger
    logger.addHandler(file_handler)
    return logger
