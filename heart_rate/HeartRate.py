'''

@author Maurice Amon
'''

class HeartRate:

    _instance = None

    _heart_rate = 0.0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(HeartRate, cls).__new__(cls)
        return cls._instance

    def set_heart_rate(self, heart_rate):
        self._heart_rate = heart_rate

    def get_heart_rate(self):
        return self._heart_rate
