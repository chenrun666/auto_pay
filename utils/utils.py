"""
公用的方法
"""
from dateutil.parser import parse


def parse_passenger_info(passengers_info: list, flight_date: str) -> tuple:
    """
    解析乘客信息，返回乘客总数，成人，青年，儿童数目

    passengers_info: 任务的乘客信息
    flight_date: 航班起飞时间
    :return: 婴儿， 成人，老人
    """
    infant = 0
    adult = 0  # 2+
    senior = 0  # 65+
    # 起飞的时间处理
    flight_date_obj = parse(flight_date)

    for item in passengers_info:
        age = item.get("birthday")
        age_time_obj = parse(age)

        delta = (flight_date_obj - age_time_obj).days
        years = delta // 365

        if 2 <= years <= 64:
            adult += 1
        elif years >= 65:
            senior += 1
        else:
            infant += 1

    return infant, adult, senior


if __name__ == '__main__':
    # 测试
    test_data = [
        {
            "id": 651374,
            "payTaskId": None,
            "name": "ZHU/YAO",
            "sex": "F",
            "birthday": "1993-06-29",
            "nationality": "CN",
            "cardNum": "E37931421",
            "cardExpired": "20241027",
            "cardIssuePlace": "CN",
            "baggageWeight": 0,
            "baggageWeightStr": None,
            "passengerType": None
        },
        {
            "id": 651374,
            "payTaskId": None,
            "name": "ZHU/YAO",
            "sex": "F",
            "birthday": "1993-06-29",
            "nationality": "CN",
            "cardNum": "E37931421",
            "cardExpired": "20241027",
            "cardIssuePlace": "CN",
            "baggageWeight": 0,
            "baggageWeightStr": None,
            "passengerType": None
        },
        {
            "id": 651374,
            "payTaskId": None,
            "name": "ZHU/YAO",
            "sex": "F",
            "birthday": "1018-06-29",
            "nationality": "CN",
            "cardNum": "E37931421",
            "cardExpired": "20241027",
            "cardIssuePlace": "CN",
            "baggageWeight": 0,
            "baggageWeightStr": None,
            "passengerType": None
        }
    ]
    flight_date = "2019-06-29"

    get = parse_passenger_info(test_data, flight_date)
    print(get)
