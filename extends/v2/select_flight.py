import time

from common.myexception import NoFlightException

from selenium.common.exceptions import NoSuchElementException

xpath_templ = '//*[@resource-id="{}"]'


# 选择任务对应的航班
def select_flight_wrapper(func):
    flag = 0

    def inner(self, *args, **kwargs):
        nonlocal flag
        flag += 1
        if flag > 8:
            flag = 0
            raise NoFlightException("没有匹配到目标航班")
        # 根据时间选择航班
        all_slifht_obj_list = self.get_obj_list(
            xpath='//*[@resource-id="com.southwestairlines.mobile:id/flight_search_results_list"]/android.widget.FrameLayout'
        )

        for index, item in enumerate(all_slifht_obj_list):
            # 获取航班的起飞时间
            try:
                flight_start_time = self.driver.find_element_by_xpath(
                    f'//*[@resource-id="com.southwestairlines.mobile:id/flight_search_results_list"]/android.widget.FrameLayout[{index + 1}]//*[@resource-id="com.southwestairlines.mobile:id/meridiem_time_view_time"]').text
                # 获取早上还是下午 com.southwestairlines.mobile:id/meridiem_time_view_meridiem
                am_or_pm = self.driver.find_element_by_xpath(
                    f'//*[@resource-id="com.southwestairlines.mobile:id/flight_search_results_list"]/android.widget.FrameLayout[{index + 1}]//*[@resource-id="com.southwestairlines.mobile:id/meridiem_time_view_meridiem"]').text
            except NoSuchElementException:
                continue
            hour, minute = flight_start_time.split(":")
            if am_or_pm == "PM" and hour != "12":
                flight_start_time = f"{12 + int(hour)}:{minute}"

            # 对比任务的起飞时间
            target_flight_start_time = self.flight_start_time[8:]
            if str(int(target_flight_start_time[:2])) + ":" + target_flight_start_time[2:] == flight_start_time:
                # 选择该航班
                item.click()
                # 将flag重置为0, 避免影响下一次的跑单。
                flag = 0

                time.sleep(2)
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

        self.swipe(
            distance=500
        )

        inner(self, *args, **kwargs)

    return inner
