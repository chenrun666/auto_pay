"""
出票的执行流程
"""
import re, time

from common.myexception import NoFlightException, PriceException  # 自定义异常信息


# 查询航班
def search_flight_wrapper(func):
    def inner(self, *args, **kwargs):
        # 移动鼠标


        # 点击单程
        self.click_btn(
            xpath='//ul[@class="nav nav--justified"]/li[2]'
        )

        # 选择开始目的地
        self.click_btn(
            xpath='//div[@class="fields search-fields py2 grouped"]/div[1]'
        )
        self.fill_input(
            xpath='//input[@type="search"]',
            content=self.dep_airport
        )
        self.click_btn(
            xpath='//ul[@class="airport-group"]/li[1]'
        )

        # 选择目的地
        self.click_btn(
            xpath='//div[@class="fields search-fields py2 grouped"]/div[2]'
        )
        self.fill_input(
            xpath='//input[@type="search"]',
            content=self.arr_airport
        )
        self.click_btn(
            xpath='//ul[@class="airport-group"]/li[1]'
        )

        # 选择出发日期
        self.click_btn(
            xpath='//i[contains(@class, "calender")]'
        )
        # 获取月份的table
        _, target_month, target_day = self.dep_date.split("-")
        target_month = int(target_month) - 1 if int(target_month) != 12 else 0
        target_month_table = self.get_ele_list(
            xpath=f'//div[@id={target_month}]'
        )[0]
        # 获取所有的天数行
        target_month_days = target_month_table.find_elements_by_xpath('.//div[@class="date-cell prev-month"]')
        target_month_days[int(target_day) - 1].click()
        self.click_btn(
            xpath='//span[contains(@class, "done")]'
        )

        # 选择乘客
        for i in range(self.adult - 1):
            self.click_btn(xpath='//i[contains(@class, "icon_plus")]')

        # 选择老年人
        if self.senior:
            self.click_btn(
                xpath='//div[@class="vertical-fill transparent segment"]/div[1]'
            )
            for i in range(self.senior - 1):
                self.click_btn(xpath='//div[contains(@class, "senior")]//i[contains(@class, "icon_plus")]')

        func(self)

    return inner


# 选择目标航班
def select_flight_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


# 校验选择的价格是否变价
def checkout_price_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


# 填写乘客信息
def fill_passengers_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


# 填写联系人信息
def fill_contact_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


# 填写支付信息
def fill_pay_info_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner
