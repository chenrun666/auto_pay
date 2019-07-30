import copy
import json

from common.log import logger
from common.myexception import *
from common.application_action import Action
from common.action import Action as WebAction

from extends.FD import *
from utils.utils import calculation_age


class WN(Action, WebAction):
    def __init__(self, task):

        # 初始化任务信息
        self.dep_airport = task["depAirport"]
        self.arr_airport = task["arrAirport"]
        self.dep_date = task["depDate"]
        self.dep_flight_number = task["depFlightNumber"]
        self.task_flight_price = task["targetPrice"]
        self.flight_start_time = task["segmentVOList"][0]["depDate"]

        # 联系人信息
        self.contact = task["contactVO"]

        # 支付信息
        self.pay_info = task["payPaymentInfoVo"]

        # 目标价格
        self.target_price = task["targetPrice"]

        # 乘客信息
        self.passenger_list = task["passengerVOList"]
        self.adult, self.child, self.infant = calculation_age(self.dep_date, self.passenger_list)

        self.back_fill = task["pnrVO"]
        self.back_fill["sourceCur"] = task["sourceCurrency"]
        self.back_fill["targetCur"] = task["targetCurrency"]
        super(WN, self).__init__()

    @login_wrapper
    @clear_passengers_wrapper
    @open_public_wrapper
    def login(self):
        pass

    @search_flight_wrapper
    def search_flight(self):
        pass

    @select_flight_wrapper
    @check_flight_price_wrapper
    def select_flight(self):
        pass

    @fill_passengers_info_wrapper
    @select_contact_wrapper
    def fill_passengers_info(self):
        pass

    @select_luggage_wrapper
    def select_luggage(self):
        pass

    @check_selected_info_wrapper
    @check_passengers_info_wrapper
    def check_selected_info(self):
        pass

    def main(self):
        try:
            self.login()
            self.search_flight()
            self.select_flight()
            self.fill_passengers_info()
            self.select_luggage()
            self.check_selected_info()
        except (SearchException, StopException) as e:
            self.back_fill["status"] = 401
            self.back_fill["errorMessage"] = str(e)
            logger.error(e)
        except NoFlightException as e:
            self.back_fill["status"] = 401
            self.back_fill["errorMessage"] = str(e)
            logger.error(e)
        except PriceException as e:
            self.back_fill["status"] = 403
            self.back_fill["errorMessage"] = str(e)
            logger.error(e)
        except PnrException as e:
            self.back_fill["status"] = 440
            self.back_fill["errorMessage"] = str(e)
            logger.error(e)
        except SelectedInfoException as e:
            self.back_fill["status"] = 401
            self.back_fill["errorMessage"] = str(e)
        except Exception as e:
            if not self.back_fill.get("status"):
                self.back_fill["status"] = 401
            self.back_fill["errorMessage"] = str(e)
            logger.exception(e)
        finally:
            self.driver.close_app()
            self.driver.quit()
            return self.back_fill


if __name__ == '__main__':
    with open("../files/fake_data.json", "r", encoding="utf-8") as f:
        fake_task = f.read()
    wn = WN(json.loads(fake_task))
    wn.main()
