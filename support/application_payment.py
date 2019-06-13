import json
import re
import time
import copy
from datetime import datetime

from common.application_action import Action

from utils.utils import parse_passenger_info

from extends.application_decorator import login_wrapper, search_flight_wrapper, select_flight_wrapper
from extends.application_decorator import check_flight_info_wrapper
from extends.application_decorator import fill_passengers_info_wrapper, fill_contact_info_wrapper


class WN(Action):
    def __init__(self, task):

        # 初始化任务信息
        self.dep_airport = task["depAirport"]
        self.arr_airport = task["arrAirport"]
        self.dep_date = task["depDate"]
        self.dep_flight_number = task["depFlightNumber"]
        self.task_flight_price = task["targetPrice"]

        # 联系人信息
        self.contact = task["contactVO"]

        # 支付信息
        self.pay_info = task["payPaymentInfoVo"]

        # 乘客信息
        self.passenger_list = task["passengerVOList"]
        infant, self.adult, self.senior = parse_passenger_info(self.passenger_list, self.dep_date)

        super(WN, self).__init__()

    @login_wrapper
    def login(self):
        pass

    @search_flight_wrapper
    def search_flight(self):

        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/book_a_flight_find_flights_button"]'
        )

    @select_flight_wrapper
    def select_flight(self):
        pass

    @check_flight_info_wrapper
    def check_selected_info(self):

        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/flight_pricing_continue_button"]'
        )

    @fill_passengers_info_wrapper
    @fill_contact_info_wrapper
    def fill_info(self):
        """填写所有信息"""
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/passengers_continue"]'
        )

    def main(self):
        try:
            self.login()
            self.search_flight()
            self.select_flight()
            self.check_selected_info()
            self.fill_info()
        except Exception as e:
            print(e)
        finally:
            self.driver.close_app()
            return ""


if __name__ == '__main__':
    with open("../files/fake_data.json", "r", encoding="utf-8") as f:
        fake_task = f.read()
    wn = WN(json.loads(fake_task))
    wn.main()
