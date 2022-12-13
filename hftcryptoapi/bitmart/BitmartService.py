import json
from .api_client import PyClient
from datetime import datetime
from .constants import *
from .bitmart_objects import *

class MarketDataAgent():
    def __init__(self, exchange=Exchange.BITMART):
        self.exchange = exchange

    def get_system_time(self):
        response =  self._request_without_params(GET, SYSTEM_TIME)
        server_time =  json.loads(response.content)['data']['server_time']
        return datetime.datetime.fromtimestamp(server_time)
    
    def get_service_status(self):
        response =  self._request_without_params(GET, SERVICE_STATUS)
        services = []
        for bt_service in json.loads(response.content)['data']['service']:
            title = bt_service["title"]
            service_type = bt_service["service_type"]
            status = bt_service["status"]
            start_time = bt_service["start_time"]
            end_time = bt_service["end_time"]
            services.append(BitmartService(title, service_type, status, start_time, end_time))
        return datetime.datetime.fromtimestamp(services)