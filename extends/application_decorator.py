import time
import calendar

from utils.utils import select_flight_date, select_passengers, select_birthday, select_gender

from common.myexception import NoFlightException, PriceException, StopException, PnrException

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
        # 获取三字字码相关的列
        self.get_obj_list(
            xpath=f'//*[contains(@text, "{self.dep_airport}")]'
        )[1].click()

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
        self.get_obj_list(
            xpath=f'//*[contains(@text, "{self.arr_airport}")]'
        )[1].click()

        # 选择日期
        select_flight_date(self, self.dep_airport)
        # 选择购买任务
        select_passengers(self)

        func(self)

    return inner


# 选择任务对应的航班
def select_flight_wrapper(func):
    def inner(self, *args, **kwargs):
        while 1:
            all_slifht_obj_list = self.get_obj_list(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/flight_search_results_list"]/android.widget.FrameLayout'
            )

            for item in all_slifht_obj_list:
                try:
                    sold_out = item.find_elements_by_xpath(
                        './/android.widget.TextView[@resource-id="com.southwestairlines.mobile:id/summary_price_effective"]')
                    if not sold_out:
                        continue
                    if "Sold Out" in sold_out[0].text:
                        continue
                except Exception:
                    pass
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
                        if item not in self.driver.page_source:
                            continue
                        current_price_obj = self.get_obj_list(
                            xpath=xpath_templ.format(f"com.southwestairlines.mobile:id/{item}")
                        )[0]

                        if current_price_obj.text.lower() == "sold out":
                            continue
                        else:
                            current_price_obj.click()
                            if self.senior:
                                # 重新获取价格
                                for item in all_grade:
                                    if item not in self.driver.page_source:
                                        continue
                                    current_price_obj = self.get_obj_list(
                                        xpath=xpath_templ.format(f"com.southwestairlines.mobile:id/{item}")
                                    )[0]
                                    if current_price_obj.text.lower() == "sold out":
                                        continue
                                    else:
                                        current_price_obj.click()
                                        break
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
        # 检测选择的航班是否正确
        flight_num_info = self.dep_flight_number.split("/")
        if len(flight_num_info) > 1:
            flight_first_num = flight_num_info[0][2:]
            flight_second_flight = flight_num_info[1][2]
        else:
            flight_first_num = flight_num_info[0][2:]
            flight_second_flight = None

        if flight_second_flight:
            page_flight_first_num = self.get_text(
                xpath=xpath_templ.format('com.southwestairlines.mobile:id/reservation_view_card_flight_number')
            )
            page_flight_second_num = self.get_text(
                xpath=xpath_templ.format(
                    'com.southwestairlines.mobile:id/reservation_view_card_secondary_flight_number')
            )
            if flight_first_num != page_flight_first_num and flight_second_flight != page_flight_second_num:
                raise NoFlightException("航班选择错误，中断程序")

        else:
            page_flight_first_num = self.get_text(
                xpath=xpath_templ.format('com.southwestairlines.mobile:id/reservation_view_card_flight_number')
            )
            if flight_first_num != page_flight_first_num:
                raise NoFlightException("航班选择错误, 中断程序")

        # 检测出发地和目的地是否选择正确
        start = self.get_text(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/reservation_view_card_departure_airport_code")
        )
        end = self.get_text(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/reservation_view_card_arrival_airport_code")
        )
        if start != self.dep_airport or end != self.arr_airport:
            raise NoFlightException("出发地和目的地选择错误，中断执行")

        func(self)

    return inner


# 校验价格
def check_flight_price_wrapper(func):
    def inner(self, *args, **kwargs):
        # 滑动到总价格
        self.swipe(
            distance=500
        )

        # 获取页面总价格
        page_total_price = self.get_text(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/money_total_value"]'
        )[1:].replace(",", "")

        # 回填支付总价格
        self.back_fill["price"] = page_total_price

        if float(page_total_price) > self.target_price * len(self.passenger_list):
            raise PriceException("页面价格大于任务目标价格。")

        func(self)

    return inner


# 填写乘客信息
def fill_passengers_info_wrapper(func):
    def inner(self, *args, **kwargs):
        for index, item in enumerate(self.passenger_list):
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
            time.sleep(1)

            if index == 0:
                for _ in range(2):
                    self.swipe(
                        distance=400
                    )

                # 第一个乘客填写联系人信息
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

                # receipt_obj = self.get_obj_list(
                #     xpath='//android.widget.EditText[@text="Email Receipt To"]'
                # )[0]
                # receipt_obj.set_text(self.contact["linkEmail"])
                self.send_keys(
                    xpath='//android.widget.EditText[@text="Email Receipt To"]',
                    content=self.contact["linkEmail"]
                )

            # 点击下一个乘客
            if index < len(self.passenger_list) - 1:
                for _ in range(2):
                    self.swipe(
                        distance=300
                    )
                self.click(
                    xpath=xpath_templ.format('com.southwestairlines.mobile:id/passengers_continue')
                )

        func(self)

    return inner


# 校验乘客信息是否正确
def check_passengers_info_wrapper(func):
    def inner(self, *args, **kwargs):
        # 获取所有的乘客列表

        for index in range(len(self.passenger_list)):
            self.click(
                xpath=f'//*[@resource-id="com.southwestairlines.mobile:id/passenger_preview_passengers_booking"]/android.widget.LinearLayout[{index + 1}]'
            )
            # 点开每个乘客的填写信息。进行校验
            # 获取页面的乘客详细信息
            page_first_name = self.get_text(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_firstname"]//android.widget.EditText'
            )
            page_last_name = self.get_text(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_lastname"]//android.widget.EditText'
            )

            # 获取对应任务中的乘客信息
            if f"{page_last_name}/{page_first_name}" != self.passenger_list[index]["name"]:
                raise StopException("乘客信息填写错误(姓名填写错误)，终止购买")

            # 获取乘客的生日
            page_birth = self.get_text(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_dob_picker_edittext"]'
            )
            target_birth_list = [i[-2:] for i in self.passenger_list[index]["birthday"].split("-")]
            target_birth = f"{target_birth_list[1]}/{target_birth_list[2]}/{target_birth_list[0]}"

            if page_birth != target_birth:
                raise StopException("乘客信息填写错误(生日选择错误)，终止购买")

            # 获取性别
            page_gender = self.get_text(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_gender_picker_edittext"]'
            )[0].upper()

            if page_gender != self.passenger_list[index]["sex"].upper():
                raise StopException("乘客信息选择错误(性别选择错误), 终止购买")

            self.click(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/action_done"]'
            )

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
        time.sleep(2)
        for _ in range(len(self.passenger_list)):
            self.swipe(
                distance=200
            )
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
        self.click(
            xpath=xpath_templ.format("com.southwestairlines.mobile:id/billinginfo_card_security_code_edit_text")
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
        expired_info = card_info["cardExpired"].split("-")
        if len(expired_info) > 2:
            card_expired_year, card_expired_month, _ = expired_info
        else:
            card_expired_year, card_expired_month = expired_info
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
        for _ in range(2):
            self.swipe(
                distance=400
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
                    distance=500
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
        )[0].set_text("17710407835")
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


# 支付的装饰器
def payment_wrapper(func):
    def inner(self, *args, **kwargs):
        time.sleep(5)
        self.swipe(
            distance=500
        )
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/payment_continue"]'
        )

        # 获取pnr
        try:
            pnr = self.get_text(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/confirmation_number"]'
            )
            self.back_fill["pnr"] = pnr
            self.back_fill["status"] = 450
        except Exception:
            raise PnrException("获取票号失败")

        func(self)

    return inner
