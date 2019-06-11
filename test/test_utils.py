import unittest

from utils.utils import *


class UtilsTest(unittest.TestCase):
    def test_passenger_info(self):
        test_data = [
            {
                "id": 651374,
                "payTaskId": None,
                "name": "ZHU/YAO",
                "sex": "F",
                "birthday": "1993-10-04",
                "nationality": "CN",
                "cardNum": "E37931421",
                "cardExpired": "20241027",
                "cardIssuePlace": "CN",
                "baggageWeight": 0,
                "baggageWeightStr": None,
                "passengerType": None
            }
        ]

        want = (1, 1, 0, 0, 0)
        get = parse_passenger_info(test_data)

        self.assertEqual(get, want)
