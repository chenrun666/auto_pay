import copy
import json

from common.log import logger
from common.myexception import *
from conf.settings import RESULT
from common.application_action import Action

from utils.utils import parse_passenger_info

from extends.application_decorator import login_wrapper, search_flight_wrapper, select_flight_wrapper
from extends.application_decorator import check_flight_info_wrapper, check_flight_price_wrapper
from extends.application_decorator import fill_passengers_info_wrapper, check_passengers_info_wrapper
from extends.application_decorator import fill_payment_info_wrapper, fill_bill_info_wrapper
from extends.application_decorator import payment_wrapper


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

        # 目标价格
        self.target_price = task["targetPrice"]

        # 乘客信息
        self.passenger_list = task["passengerVOList"]
        infant, self.adult, self.senior = parse_passenger_info(self.passenger_list, self.dep_date)

        # 组织回填数据
        self.back_fill = copy.deepcopy(RESULT)
        self.back_fill["linkEmail"] = self.contact["linkEmail"]
        self.back_fill["linkEmailPassword"] = self.contact["linkEmailPassword"]
        self.back_fill["linkPhone"] = self.contact["linkPhone"]
        self.back_fill["nameList"] = [name["name"] for name in self.passenger_list]
        self.back_fill["sourceCur"] = task["sourceCurrency"]
        self.back_fill["targetCur"] = task["targetCurrency"]
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
    @check_flight_price_wrapper
    def check_selected_info(self):
        self.swipe(
            distance=300
        )
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/flight_pricing_continue_button"]'
        )

    @fill_passengers_info_wrapper
    def fill_info(self):
        """填写所有信息"""
        for _ in range(2):
            self.swipe(
                distance=400
            )
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/passengers_continue"]'
        )

    @check_passengers_info_wrapper
    @fill_payment_info_wrapper
    @fill_bill_info_wrapper
    def payment_info(self):
        """填写支付信息进行购买"""
        pass

    @payment_wrapper
    def payment(self):
        """点击购买"""
        pass

    def main(self):
        try:
            self.login()
            self.search_flight()
            self.select_flight()
            self.check_selected_info()
            self.fill_info()
            self.payment_info()
            self.payment()
        except SearchException as e:
            self.back_fill["status"] = 401
            self.back_fill["msg"] = str(e)
            logger.error(e)
        except NoFlightException as e:
            self.back_fill["status"] = 401
            self.back_fill["msg"] = str(e)
            logger.error(e)
        except PriceException as e:
            self.back_fill["status"] = 403
            self.back_fill["msg"] = str(e)
            logger.error(e)
        except PnrException as e:
            self.back_fill["status"] = 440
            self.back_fill["msg"] = str(e)
            logger.error(e)
        except Exception as e:
            self.back_fill["status"] = 250
            self.back_fill["msg"] = str(e)
            logger.error(e)
        finally:
            self.driver.close_app()

            return self.back_fill


if __name__ == '__main__':
    with open("../files/fake_data.json", "r", encoding="utf-8") as f:
        fake_task = f.read()
    wn = WN(json.loads(fake_task))
    wn.main()
