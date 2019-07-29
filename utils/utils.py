"""
公用的方法
"""
import time
import datetime
import calendar

from dateutil.parser import parse

from selenium.common.exceptions import NoSuchElementException

month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def is_leap(year):
    """判断是否为瑞年"""
    if year % 400 == 0 or year % 40 == 0 or year % 4 == 0:
        return True
    else:
        return False


def minus_result(first_year, second_year):
    y = first_year.year - second_year.year
    m = first_year.month - second_year.month
    d = first_year.day - second_year.day
    if d < 0:
        if second_year.month == 2:
            if is_leap(second_year.year):
                month_days[2] = 29
        d += month_days[second_year.month]
        m -= 1
    if m < 0:
        m += 12
        y -= 1
    if y == 0:
        if m == 0:
            return 0, 0, d
            # return ('{}天'.format(d))
        else:
            return 0, m, d
            # return ('{}月{}天'.format(m, d))
    else:
        return y, m, d
        # return ('{}岁{}月{}天'.format(y, m, d))


def calculation_age(fligth_date: str, passengers_list: list) -> tuple:
    """
    计算list中乘客的年龄，计算出大人小孩婴儿的数量
    :return:
    """
    adult_num = 0
    child_num = 0
    infant_num = 0

    for passenger in passengers_list:
        birth_year, birth_mon, birth_day = passenger["birthday"].split("-")
        birth_obj = datetime.datetime(
            year=int(birth_year), month=int(birth_mon), day=int(birth_day)
        )

        # 飞机起飞时间
        flight_date_year, flight_date_mon, flight_date_day = fligth_date.split("-")
        flight_date_obj = datetime.datetime(
            year=int(flight_date_year),
            month=int(flight_date_mon),
            day=int(flight_date_day)
        )

        passenger_age = minus_result(flight_date_obj, birth_obj)[0]  # 获取乘客年龄

        if passenger_age < 2:
            infant_num += 1
        elif passenger_age < 12:
            child_num += 1
        else:
            adult_num += 1

    return adult_num, child_num, infant_num


# 选择目标日历
def select_flight_date(self, target_date):
    """
    选择目标日期
    :param self: 类的对象
    :param target_date: 目标日期
    :return:
    """
    # 打开日历
    self.click(
        xpath='//*[@resource-id="com.southwestairlines.mobile:id/book_a_flight_depart_date"]'
    )
    # 目标月份
    target_month_index = int(self.dep_date.split("-")[1])
    target_month_eng = calendar.month_name[target_month_index]
    # 获取目标天的索引值
    target_day_str = int(self.dep_date.split("-")[2])
    while 1:
        page_month = self.get_text(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/month_title"]'
        ).split()[0]
        if target_month_eng == page_month:
            # 选择天
            for _ in range(10):
                try:
                    self.driver.find_elements_by_xpath(
                        xpath=f'//android.widget.TextView[contains(@text, "{target_month_eng}")]/following-sibling::*[2]//*[contains(@text, "{target_day_str}")]'
                    )[0].click()
                    break
                except (NoSuchElementException, IndexError):
                    self.swipe(
                        distance=150
                    )
            self.click(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/action_done"]'
            )
            break
        # 滑动屏幕
        self.swipe(
            distance=500
        )
        time.sleep(1)


# 选择乘机人数
def select_passengers(self):
    """
    选择乘机人数
    :param self:
    :param adult: 成年人
    :param senior: 老年人
    :return:
    """
    for _ in range(self.adult - 1):
        self.click(
            xpath='//*[@ resource-id="com.southwestairlines.mobile:id/book_a_flight_increment_passengers_button"]'
        )
    # 添加老年人
    if self.senior:
        self.click(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/book_a_flight_add_senior_fare_section_text"]'
        )
        for _ in range(self.senior - 1):
            self.click(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/book_a_flight_increment_seniors_button"]'
            )


# 选择乘客的生日
def select_birthday(self, birth_year, birth_month, birth_day):
    """选择乘客的生日"""
    if birth_year >= 1970:
        direction = "UP"
    else:
        direction = "DOWN"

    flag = False

    while 1:

        all_years_obj = self.get_obj_list(
            xpath='//*[@resource-id="android:id/date_picker_year_picker"]/android.widget.TextView'
        )
        for item in all_years_obj:
            if item.text == str(birth_year):
                item.click()
                flag = True
                break
        else:
            self.swipe(
                distance=400,
                direction=direction
            )
        if flag:
            break

    # 选择对应的月份
    for _ in range(birth_month - 1):
        self.click(
            xpath=f'//*[@resource-id="android:id/next"]'
        )
    self.click(
        xpath=f'//*[@resource-id="android:id/month_view"]/android.view.View[{birth_day}]'
    )
    # 点击确定
    self.click(
        xpath='//*[@resource-id="android:id/button1"]'
    )


# 选择乘客性别
def select_gender(self, gender):
    """选择乘客性别"""
    gender_map = {
        "F": "Female",
        "M": "Male"
    }
    self.click(
        xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_gender_picker"]'
    )

    gender_obj_list = self.get_obj_list(
        xpath='//*[@resource-id="android:id/text1"]'
    )
    for item in gender_obj_list:
        if item.text == gender_map[gender]:
            item.click()
            self.click(xpath='//*[@resource-id="android:id/button1"]')  # 点击OK
            break


# 校验接收邮箱是否正确，如果错误进行多次重写
def check_receipt_email(self):
    # page input email

    # target email
    target_email = self.contact["linkEmail"]
    flag = 0  # 重复次数记录

    def again_input():
        nonlocal flag
        flag += 1
        if flag > 3:
            raise Exception("邮箱填写错误。")

        page_receipt_email = self.get_text(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_email_receipt_to"]//android.widget.EditText'
        ).strip()

        if page_receipt_email.lower() == target_email.lower().strip():
            flag = 0
        else:
            self.send_keys(
                xpath='//*[@resource-id="com.southwestairlines.mobile:id/booking_passenger_email_receipt_to"]//android.widget.EditText',
                content=target_email
            )
            # 递归输入
            again_input()

    return again_input()


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
