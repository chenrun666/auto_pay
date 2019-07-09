"""
公用的方法
"""
import calendar
import time

from dateutil.parser import parse

from selenium.common.exceptions import NoSuchElementException


def parse_passenger_info(passengers_info: list, flight_date: str) -> tuple:
    """
    解析乘客信息，返回乘客总数，成人，青年，儿童数目

    passengers_info: 任务的乘客信息
    flight_date: 航班起飞时间
    :return: 婴儿， 成人，老人
    """
    infant = 0
    adult = 0  # 2+
    senior = 0  # 65+
    # 起飞的时间处理
    flight_date_obj = parse(flight_date)

    for item in passengers_info:
        age = item.get("birthday")
        age_time_obj = parse(age)

        delta = (flight_date_obj - age_time_obj).days
        years = delta // 365

        if 2 <= years <= 64:
            adult += 1
        elif years >= 65:
            senior += 1
        else:
            infant += 1

    return infant, adult, senior


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
                except NoSuchElementException:
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
