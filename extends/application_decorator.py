import time
import calendar

from utils.utils import select_flight_date, select_passengers, select_birthday, select_gender

from common.myexception import NoFlightException

xpath_templ = '//*[@resource-id="{}"]'


# 登陆操作
def login_wrapper(func):
    def inner(self, *args, **kwargs):
        # 点击游客访问
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/login_continue_as_guest")
        )
        func(self)

    return inner


# 查询航班
def search_flight_wrapper(func):
    def inner(self, *args, **kwargs):
        # 点击booking flight
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/home_book_flight_button")
        )
        # 点击单程
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/book_a_flight_one_way_section")
        )

        # 选择出发地，点击from
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/book_a_flight_airport_code_from")
        )
        # 输入查询条件
        self.send_keys(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/airport_list_search"),
            content=self.dep_airport
        )
        # 选择航班
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/airport_list_fast_scroller"]/android.widget.LinearLayout[2]'
        )

        # 选择到达地，点击to
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/book_a_flight_airport_code_to")
        )
        # 输入查询条件
        self.send_keys(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/airport_list_search"),
            content=self.arr_airport
        )
        # 选择航班
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/airport_list_fast_scroller"]/android.widget.LinearLayout[2]'
        )

        # 选择日期
        select_flight_date(self, self.dep_airport)
        # 选择购买任务
        select_passengers(self)

        func(self)

    return inner


# 选择任务对应的航班
def select_flight_wrapper(func):
    def inner(self, *args, **kwargs):
        all_slifht_obj_list = self.get_obj_list(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/flight_search_results_list"]/android.widget.FrameLayout'
        )
        for item in all_slifht_obj_list:
            item.click()
            # 获取页面航班号
            page_flight_obj = self.get_obj_list(
                xpath=xpath_templ.format("com.southwestairlines.mobile:id/flight_number")
            )[0]
            page_flight_num = page_flight_obj.text
            if "/".join([item[2:] for item in self.dep_flight_number.split("/")]) == page_flight_num:
                # 选择最低价格
                all_grade = [
                    "wanna_get_away_price_effective",
                    "anytime_price_effective",
                    "business_select_price_effective"
                ]
                for item in all_grade:
                    current_price_obj = self.get_obj_list(
                        xpath=xpath_templ.format(f"com.southwestairlines.mobile:id/{item}")
                    )[0]
                    if current_price_obj.text.lower() == "sold out":
                        continue
                    else:
                        current_price_obj.click()
                        func(self)
                        return
                else:
                    raise NoFlightException("航班卖完了。购买失败")

            # 收起价格面板，点击下一个
            page_flight_obj.click()

    return inner


# 校验选择的信息
def check_flight_info_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


# 填写乘客信息
def fill_passengers_info_wrapper(func):
    def inner(self, *args, **kwargs):
        for item in self.passenger_list:
            last_name, first_name = item["name"].split("/")
            birth_year, birth_month, birth_day = [int(i) for i in item["birthday"].split("-")]
            self.send_keys(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_firstname"]//android.widget.EditText',
                content=first_name
            )
            self.send_keys(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_lastname"]//android.widget.EditText',
                content=last_name
            )

            # 选择生日
            self.click(
                xpath=xpath_templ.format("com.southwestairlines.mobile:id/booking_passenger_dob_picker_edittext")
            )

            # 选择生日
            select_birthday(self, birth_year, birth_month, birth_day)
            # 选择性别
            select_gender(self, item["sex"])

        func(self)

    return inner


# 填写联系人信息
def fill_contact_info_wrapper(func):
    def inner(self, *args, **kwargs):
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/booking_passenger_contact_method")
        )

        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/contact_method_email_layout")
        )

        self.send_keys(
            xpath='//android.widget.EditText',
            content=self.contact["linkEmail"]
        )

        self.click(
            xpath='//android.widget.EditText'
        )

        # 打对勾
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/action_done")
        )

        time.sleep(2)
        self.swipe(
            distance=1000
        )

        receipt_obj = self.get_obj_list(
            xpath='//android.widget.EditText[@text="Email Receipt To"]'
        )[0]
        receipt_obj.set_text(self.contact["linkEmail"])

        func(self)

    return inner


# 填写支付信息
def fill_payment_info_wrapper(func):
    def inner(self, *args, **kwargs):
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/booking_review_payment_method")
        )

        # 添加一个支付卡
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/new_card_icon")
        )

        # 输入支付信息
        card_info = self.pay_info["cardVO"]
        # 卡号
        self.send_keys(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/billinginfo_card_number_edit_text"),
            content=card_info["cardNumber"]
        )
        # CVV
        self.send_keys(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/billinginfo_card_security_code_edit_text"),
            content=card_info["cvv"]
        )

        # 选择卡的过期时间
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/billinginfo_card_expiration")
        )
        # 选择过期的月份
        self.click(
            xpath=xpath_templ.format("android:id/text1")
        )
        card_expired_year, card_expired_month = card_info["cardExpired"].split("-")
        self.click(
            xpath=f'//android.widget.CheckedTextView[@text="{int(card_expired_month)}-{calendar.month_name[int(card_expired_month)]}"]'
        )

        # 选择过期年份
        self.get_obj_list(
            xpath='//*[@resource-id="android:id/text1"]'
        )[1].click()
        time.sleep(2)
        for item in self.get_obj_list(xpath='//*[@resource-id="android:id/text1"]'):
            if item.text == card_expired_year:
                item.click()
                break
        self.click(
            xpath='//android.widget.Button[@text="OK"]'
        )
        # 卡的名字
        self.send_keys(
            xpath='//android.widget.EditText[@text="Name on card"]',
            content=f"{card_info['firstName']} {card_info['lastName']}"
        )

        func(self)

    return inner


# 填写账单地址信息
def fill_bill_info_wrapper(func):
    def inner(self, *args, **kwargs):
        # 填写账单地址信息
        self.swipe(
            distance=800
        )
        # 选择国家
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/billinginfo_country"]'
        )

        flag = False
        while 1:
            for item in self.get_obj_list(
                    xpath='//*[@resource-id="com.southwestairlines.mobile:id/select_dialog_listview"]/android.widget.CheckedTextView'):
                if "CN" in item.text:
                    flag = True
                    item.click()
                    break
            else:
                self.swipe(
                    distance=1000
                )
            if flag:
                break

        # 点击OK
        self.click(
            xpath=xpath_templ.format("android:id/button1")
        )

        self.send_keys(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/billinginfo_street_1"]//android.widget.EditText',
            content="beijingshi"
        )

        self.send_keys(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/billinginfo_postal"]//android.widget.EditText',
            content="100000"
        )

        self.send_keys(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/billinginfo_city"]//android.widget.EditText',
            content="beijingshi"
        )

        self.send_keys(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/billinginfo_province"]//android.widget.EditText',
            content="beijingshi"
        )

        self.get_obj_list(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/billinginfo_phone"]//android.widget.EditText'
        )[0].set_text("17610780919")
        self.get_obj_list(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/billinginfo_phone"]//android.widget.EditText'
        )[0].click()

        # 取消光标
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/billinginfo_phone_countrycode"]'
        )

        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/action_done"]'
        )

        func(self)

    return inner
