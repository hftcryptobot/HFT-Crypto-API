import requests, json
from .bm_logging import log
from . import exceptions, bitmart_utils
from .data import constants as c


class PyClient(object):

    def __init__(self, api_key, secret_key, memo, url, timeout):
        """
        :param api_key: Get from bitmart API page.
        :param secret_key: Get from bitmart API page.
        :param memo: Your memo
        :param url: Request Domain URL.
        :param timeout: (connection timeout, read timeout).
        """
        self.API_KEY = api_key
        self.SECRET_KEY = secret_key
        self.MEMO = memo
        self.URL = url
        self.TIMEOUT = timeout

    @log
    def _request(self, method, request_path, params, auth):
        if method == c.GET or method == c.DELETE:
            url = self.URL + request_path + bitmart_utils.parse_params_to_str(params)
        else:
            url = self.URL + request_path

        # set body
        body = json.dumps(params) if method == c.POST else ""

        # set header
        if auth == c.Auth.NONE:
            header = bitmart_utils.get_header(api_key=None, sign=None, timestamp=None)
        elif auth == c.Auth.KEYED:
            header = bitmart_utils.get_header(self.API_KEY, sign=None, timestamp=None)
        else:
            timestamp = bitmart_utils.get_timestamp()
            sign = bitmart_utils.sign(bitmart_utils.pre_substring(timestamp, self.MEMO, str(body)), self.SECRET_KEY)
            header = bitmart_utils.get_header(self.API_KEY, sign, timestamp)

        # send request
        response = None
        if method == c.GET:
            response = requests.get(url, headers=header, timeout=self.TIMEOUT)
        elif method == c.POST:
            response = requests.post(url, data=body, headers=header, timeout=self.TIMEOUT)
        elif method == c.DELETE:
            response = requests.delete(url, headers=header, timeout=self.TIMEOUT)

        # exception handle
        if not str(response.status_code) == '200':
            raise exceptions.APIException(response)
        try:
            res_header = response.headers
            r = dict()
            try:
                r['Remaining'] = res_header['X-BM-RateLimit-Remaining']
                r['Limit'] = res_header['X-BM-RateLimit-Limit']
                r['Reset'] = res_header['X-BM-RateLimit-Reset']
            except:
                pass
            return response#json(), r

        except ValueError:
            raise bitmart_exceptions.RequestException('Invalid Response: %s' % response.text)

    def _request_without_params(self, method, request_path, auth=c.Auth.NONE):
        return self._request(method, request_path, {}, auth)

    def _request_with_params(self, method, request_path, params, auth=c.Auth.NONE):
        return self._request(method, request_path, params, auth)