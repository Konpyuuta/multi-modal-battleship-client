'''
@author Alessia Bussard
@description Response from server after receiving heart rate data
'''

from commands.responses.Response import Response
from commands.requests.RequestTypes import RequestTypes


class HeartRateResponse(Response):

    _success = None
    _message = None

    def __init__(self, success=True, message="Heart rate data received"):
        super().__init__(RequestTypes.HEART_RATE)
        self._success = success
        self._message = message

    def is_success(self):
        return self._success

    def get_message(self):
        return self._message