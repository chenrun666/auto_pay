import json, time, requests

from conf.settings import DEBUG, PROXY

from common.stroge import rdb
from common.log import logger
from common.myexception import *

from utils.utils import calculation_age

from extends.post_decorator import select_flight_wrapper, checkout_price_wrapper
from extends.post_decorator import fill_contact_wrapper, fill_passengers_wrapper, fill_pay_info_wrapper  # 填写信息的装饰器


class WN:
    def __init__(self, task):
        # 初始化一个session
        self.session = requests.session()

        # 初始化公共的请求头
        self.headers = None

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

        self.url = f"https://www.southwest.com/air/booking/select.html?int=HOMEQBOMAIR&adultPassengersCount={self.adult}&departureDate={self.dep_date}&departureTimeOfDay=ALL_DAY&destinationAirportCode={self.arr_airport}&fareType=USD&originationAirportCode={self.dep_airport}&passengerType=ADULT&promoCode=&reset=true&returnDate=&returnTimeOfDay=ALL_DAY&seniorPassengersCount={self.senior}&tripType=oneway"

    @select_flight_wrapper
    def select_flight(self, target_flight_info):
        # 提取可用的productID
        all_grade = target_flight_info["fareProducts"]["ADULT"]
        for k, v in all_grade.items():
            if v["availabilityStatus"] == "AVAILABLE":
                product_id = v["productId"]
                break
        else:
            raise NoFlightException("没有可用的航班供选择")

        # 提交选中航班
        target_url = "https://www.southwest.com/api/air-booking/v1/air-booking/page/air/booking/price"
        data = {
            "adultPassengersCount": str(self.adult),
            "currencyCode": "USD",
            "currencyType": "REVENUE",
            "promoCode": "",
            "requiredPricingInfo": True,
            "segmentProducts": [
                {
                    "ADULT": product_id
                }
            ],
            "seniorPassengersCount": str(self.senior),
            "application": "air-booking",
            "site": "southwest"
        }
        for _ in range(3):
            response = self.session.post(
                url=target_url, headers=self.headers,
                data=json.dumps(data),
                proxies={"http": "127.0.0.1:3213", "https": "127.0.0.1:3213"} if PROXY else None
            )
            if response.status_code == 200:
                select_result = response.json()
                return select_result
        else:
            raise PostDataEception("提交信息失败，购买失败")

    @checkout_price_wrapper
    def check_price(self):
        pass

    def main(self):
        try:
            self.select_flight()
            self.check_price()
        except NoFlightException as e:
            logger.error(str(e))
        except PriceException as e:
            logger.error(str(e))
        except PostDataEception as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(f"未知错误{e}")
        finally:
            return ""


if __name__ == '__main__':
    if DEBUG:
        with open("../files/fake_data.json", "r", encoding="utf-8") as f:
            fake_task = f.read()
        wn = WN(json.loads(fake_task))
        wn.main()
