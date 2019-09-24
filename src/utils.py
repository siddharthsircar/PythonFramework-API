import json
from jsonschema import validate
from datetime import datetime



def assert_valid_schema(data, schema_file):
    """ Checks whether the given data matches the schema """

    schema = load_json_file(schema_file)
    return validate(data, schema)


def load_json_file(filename):
    """ Loads the given schema file """

    with open(filename) as schema_file:
        return json.loads(schema_file.read())


def assert_valid_json_data(data, json_file):
    """ Checks whether the given data matches the data file """

    json_data = load_json_file(json_file)

    return _validate_data(data, json_data)


def _validate_data(response_data, json_file_data):
    """ Validate the response data with stored data """

    assert json.loads(response_data) == json_file_data


def encode_to_ascii(lst):
    """ Encode unicode chars to ascii  """
    new_list = []
    for dic in lst:
        new_dic = {}
        for k, v in dic.iteritems():
            new_dic[k.encode("ascii", "ignore")] = v.encode("ascii", "ignore") if isinstance(v, basestring) else v
        new_list.append(new_dic)
    return new_list

def get_id_in_list (id=None, lst=None, id_name='groupId'):
    """ Find item by id in the list  """

    if not id or not lst or not id_name:
        return None
    for val in lst:
        if val[id_name] == id:
           return val
    return None

def convert_time_in_milliseconds(timeToConvert):
    """ Converts timestamp in the format dd-mm-yy into milliseconds """

    try:
        dt_obj = datetime.strptime(timeToConvert,'%d-%m-%Y').strftime('%s')
        millisec = int(dt_obj)* 1000
        return millisec
    except ValueError:
        return None



