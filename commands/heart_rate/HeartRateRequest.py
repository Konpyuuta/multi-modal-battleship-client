'''
@author Alessia Bussard
@description Request to send heart rate data to the server
'''

from commands.requests.Request import Request
from commands.requests.RequestTypes import RequestTypes


class HeartRateRequest(Request):

    _heart_rate = None

    def __init__(self, heart_rate):
        self._request_type = RequestTypes.HEART_RATE
        self._heart_rate = heart_rate

    def get_heart_rate(self):
        return self._heart_rate