import os

FWORK_PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IN_DATA_PATH = os.path.join(FWORK_PARENT_DIR,  "data")
LOG_DIR = os.path.join(FWORK_PARENT_DIR, "logs")
TESTS_DIR = os.path.join(FWORK_PARENT_DIR, "tests-api")
CONFIG_DIR = os.path.join(FWORK_PARENT_DIR, "config")

print (FWORK_PARENT_DIR)
print (IN_DATA_PATH)
