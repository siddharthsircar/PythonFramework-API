import yaml
import os
# import pdb

from config import fwork
from src import testlogger
logger = testlogger.setup_custom_logger('data_reader')


class data(object):
    def __init__(self):
        pass

    def create_file_data(self, walk_dir):
        for dirpath, dirs, files in os.walk(walk_dir):
            for filename in files:
                data_load = {}
                fname = os.path.join(dirpath, filename)
                if any(ext in filename for ext in [".yaml", ".props"]):
                    fname = open(fname, 'r')
                    data_load.update(yaml.load(fname))

                if ".yaml" in filename:
                    setattr(self.__class__, "%s_data" % os.path.splitext(filename)[0], data_load)
                elif ".props" in filename:
                    setattr(self.__class__, "%s_var_data" %os.path.splitext(filename)[0], data_load)

    def create_data(self):
        if os.environ.get('CONFIG_FILE') == None:
            walk_dir = fwork.CONFIG_DIR
            self.create_file_data(walk_dir)
        else:
            data_load = {}
            fname = os.environ.get("CONFIG_FILE")
            filename = open(fname, "r")
            data_load.update(yaml.load(filename))
            setattr(self.__class__, "topo_data", data_load)

        walk_dir = fwork.IN_DATA_PATH
        self.create_file_data(walk_dir)

    def get_data(self, feat):
        dict_data = getattr(self.__class__, "%s_data" % feat)
        data = Dotable.parse(dict_data)
        logger.info("DataReader: Done reading file %s " % feat)
        return data

    def get_var_data(self, feat, dic={}):
        try:
            dict_data = getattr(self.__class__, "%s_var_data" %feat)
        except:
            self.create_data()
            dict_data = getattr(self.__class__, "%s_var_data" % feat)
        data = Dotable.parse(dict_data)

        return data

class Dotable(dict):

    __getattr__= dict.__getitem__

    def __init__(self, d):
        self.update(**dict((k, self.parse(v))
                           for k, v in d.iteritems()))

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v







