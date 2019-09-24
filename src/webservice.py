import requests
from src import testlogger


logger = testlogger.setup_custom_logger('webservice')


def put(httplibrary=requests, url=None, data=None, files=None,
        headers={'content-type': 'application/json; charset=utf-8'}, token=None):
    headers["Authorization"] = token

    headers["X-No-Throttle"] = "True"

    logger.debug("Request : %s Headers %s Post body %s and files %s " % (url, headers, data, files))
    response = httplibrary.put(url=url, data=data, files=files, headers=headers)
    logger.debug("Response code %d and response body %s" % (response.status_code, response.content))
    return response


def get(http_library=requests, url=None, headers={'content-type': 'application/json; charset=utf-8'}, token=None,
        verify=True, allow_redirects=True, params=None):

    headers["Authorization"] = token

    headers["X-No-Throttle"] = "True"

    logger.debug("About to make get request for url %s Headers %s" % (url, headers))
    response = http_library.get(url=url, headers=headers, verify=verify, allow_redirects=allow_redirects, params=params)
    logger.debug("Response code %d and response body %s" % (response.status_code, response.text))
    return response


def post(httplibrary=requests, url=None, data=None, files=None,
         headers={'content-type': 'application/json; charset=utf-8'}, token=None, ):

    headers["Authorization"] = token

    logger.debug("Request : %s Headers %s Post body %s and files %s " % (url, headers, data, files))
    response = httplibrary.post(url=url, data=data, files=files, headers=headers)
    logger.debug("Response code %d and response body     %s" % (response.status_code, response.content))
    return response


def delete(httplibrary=requests, url=None, data=None, files=None,
           headers={'content-type': 'application/json; charset=utf-8'}, token=None ):

    headers["Authorization"] = token

    headers["X-No-Throttle"] = "True"


    logger.debug("Request : %s Headers %s DELETE body %s and files %s " % (url, headers, data, files))
    response = httplibrary.delete(url=url, data=data, files=files, headers=headers)
    logger.debug("Response code %d and response body %s" % (response.status_code, response.content))
    return response


def get_token(url, email, password):
    """

    :param url:
    :param email:
    :param password:
    :return: returns the token
    """

    post_data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=post_data)
    logger.debug(response.status_code)
    if response.status_code is not 200:
        print "Status code is not 200"
        print response.status_code
    if response.status_code > 299:
        logger.info("Webservice: Token request failed with status code: %s " % response.status_code)
    resp_json = response.json()
    auth_token = resp_json.get('user').get('accessToken')
    logger.debug("Webservice: Got the token %s " % auth_token)
    return str(auth_token)


if __name__ == '__main__':
    response = get_token('http://52.9.78.11:4000/login', 'ewaadmin@celsysemail.celsyswtc.in', 'Cel@123')
    print response
