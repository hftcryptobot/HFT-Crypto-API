import json
from .api_client import PyClient
from datetime import datetime
from .constants import *
from .bitmart_objects import *
from pydantic import BaseModel


class AccountConnector(BaseModel, validate_assignment=True):
    def __init__(self, exchange=Exchange.BITMART):
        super().__init__(self)
        self.exchange = exchange

#self._request_without_params(GET, ACCOUNT_BALANCE, Auth.KEYED)

    