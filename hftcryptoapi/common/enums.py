from enum import Enum


class BaseURL(str, Enum):
    """Base urls for API endpoints"""

    API_URL = 'https://api-cloud.bitmart.com'
    WS_URL = 'wss://ws-manager-compress.bitmart.com/api?protocol=1.1'
    WS_URL_USER = 'wss://ws-manager-compress.bitmart.com/user?protocol=1.1'
    CONTRACT_WS_URL = 'wss://openapi-ws.bitmart.com/api?protocol=1.1'
    CONTRACT_WS_URL_USER = 'wss://openapi-ws.bitmart.com/user?protocol=1.1'


class Sort(str, Enum):
    ASC = "asc"
    DESC = "desc"

