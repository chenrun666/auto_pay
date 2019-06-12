import json, time

from conf.settings import DEBUG

from common.log import logger
from common.action import Action
from common.myexception import *

from utils.utils import parse_passenger_info

from extends.mobile_decorator import select_flight_wrapper, checkout_price_wrapper, search_flight_wrapper
from extends.mobile_decorator import fill_contact_wrapper, fill_passengers_wrapper, fill_pay_info_wrapper  # 填写信息的装饰器


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
        self.infant, self.adult, self.senior = parse_passenger_info(self.passenger_list, self.dep_date)


        url = "https://mobile.southwest.com/air/booking/shopping"
        super(WN, self).__init__(url)

    @search_flight_wrapper
    def search_flight(self):
        """查询航班"""

        self.click_btn(
            xpath='//button[@role="submit"]'
        )

    @select_flight_wrapper
    def select_flight(self):

        self.click_btn(
            xpath='//button[@id="air-booking-product-1"]'
        )

    @checkout_price_wrapper
    def check_price(self):

        self.get_ele_list(
            xpath='//div[@class="price--continue-button"]/button'
        )[0].click()

    @fill_passengers_wrapper
    @fill_contact_wrapper
    @fill_pay_info_wrapper
    def fill_info(self):

        self.click_btn(
            xpath='//button[contains(@aria-label, "Purchase")]'
        )

    def main(self):
        try:
            self.search_flight()
            self.select_flight()
            self.check_price()
            self.fill_info()
        except NoFlightException as e:
            logger.error(str(e))
        except PriceException as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(f"未知错误{e}")
        finally:
            self.close()


if __name__ == '__main__':
    if DEBUG:
        with open("../files/fake_data.json", "r", encoding="utf-8") as f:
            fake_task = f.read()
        wn = WN(json.loads(fake_task))
        wn.main()
