"""
出票的执行流程
"""
import re, time, json

from conf.settings import PROXY
from common.stroge import rdb
from common.myexception import NoFlightException, PriceException, SearchException, PostDataEception  # 自定义异常信息


def check_info(self, *args, **kwargs):
    """
    校验提交的信息是否正确
    :param self: 类的对象
    :param args: 提交信息返回回来的结果
    :param kwargs:
    :return:
    """
    pass


# 选择目标航班
def select_flight_wrapper(func):
    target_url = "https://www.southwest.com/api/air-booking/v1/air-booking/page/air/booking/shopping"

    def inner(self, *args, **kwargs):
        # 获取航班数据
        post_data = {
            "int": "HOMEQBOMAIR",
            "adultPassengersCount": str(self.adult),
            "departureDate": self.dep_date,
            "departureTimeOfDay": "ALL_DAY",
            "destinationAirportCode": self.arr_airport,
            "fareType": "USD",
            "originationAirportCode": self.dep_airport,
            "passengerType": "ADULT",
            "promoCode": "",
            "reset": "true",
            "returnDate": "",
            "returnTimeOfDay": "ALL_DAY",
            "seniorPassengersCount": str(self.senior),
            "tripType": "oneway",
            "application": "air-booking",
            "site": "southwest"
        }
        for _ in range(3):
            self.headers = rdb.header()
            for _ in range(3):
                response = self.session.post(
                    url=target_url, headers=self.headers,
                    data=json.dumps(post_data),
                    proxies={"http": "127.0.0.1:3213", "https": "127.0.0.1:3213"} if PROXY else None
                )
                if response.status_code == 200:
                    flight_info = response.json()
                    all_flight = flight_info["data"]["searchResults"]["airProducts"][0]["details"]
                    for item in all_flight:
                        if [i[2:] for i in self.dep_flight_number.split("/")] == item["flightNumbers"]:
                            selected_result = func(self, item)
                            # 校验提交的信息
                            check_info(self, selected_result)
                            return
                    else:
                        raise NoFlightException("没有匹配到目标航班")
        else:
            raise SearchException("查询航班异常")

    return inner


# 校验选择的价格是否变价
def checkout_price_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


# 填写乘客信息
def fill_passengers_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


# 填写联系人信息
def fill_contact_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


# 填写支付信息
def fill_pay_info_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner
