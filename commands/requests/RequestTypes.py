'''

@author Maurice Amon
'''
from abc import ABC
from enum import Enum


class RequestTypes(Enum):

    MOVE_REQUEST = "MOVE",
    START_REQUEST = "START",
    FETCH_REQUEST = "FETCH",
    HEART_RATE = "HEART_RATE"
