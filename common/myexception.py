class StopException(Exception):
    def __init__(self, msg):
        self.msg = msg


class NoFlightException(Exception):
    def __init__(self, msg):
        self.msg = msg


class PriceException(Exception):
    def __init__(self, msg):
        self.msg = msg
