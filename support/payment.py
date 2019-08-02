import json, time

from conf.settings import DEBUG

from common.log import logger
from common.action import Action
from common.myexception import *

from utils.utils import calculation_age

from extends.decorator import select_flight_wrapper, checkout_price_wrapper
from extends.decorator import fill_contact_wrapper, fill_passengers_wrapper, fill_pay_info_wrapper  # 填写信息的装饰器

"""
https://www.southwest.com/air/booking/select.html?int=HOMEQBOMAIR&adultPassengersCount=3&departureDate=2019-06-12&departureTimeOfDay=ALL_DAY&destinationAirportCode=TUL&fareType=USD&originationAirportCode=LGB&passengerType=SENIOR&promoCode=&reset=true&returnDate=&returnTimeOfDay=ALL_DAY&seniorPassengersCount=1&tripType=oneway
"""


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
        infant, adult, senior = calculation_age(self.dep_date, self.passenger_list)

        url = f"https://www.southwest.com/air/booking/select.html?int=HOMEQBOMAIR&adultPassengersCount={adult}&departureDate={self.dep_date}&departureTimeOfDay=ALL_DAY&destinationAirportCode={self.arr_airport}&fareType=USD&originationAirportCode={self.dep_airport}&passengerType=ADULT&promoCode=&reset=true&returnDate=&returnTimeOfDay=ALL_DAY&seniorPassengersCount={senior}&tripType=oneway"
        super(WN, self).__init__(url)

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
