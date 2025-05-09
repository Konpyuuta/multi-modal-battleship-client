'''

@author Maurice Amon
'''
from abc import ABC


class Response(ABC):

    _response_type = None

    def get_response_type(self):
        return self._response_type
