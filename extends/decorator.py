"""
出票的执行流程
"""
import re, time

from common.myexception import NoFlightException, PriceException  # 自定义异常信息


# 选择目标航班
def select_flight_wrapper(func):
    def inner(self, *args, **kwargs):

        # 点击下一步
        continue_js = 'document.querySelector("#air-booking-product-1").click()'
        self.driver.execute_script(continue_js)

        # 选择航班的逻辑
        # 获取所有航班
        all_flight = self.get_ele_list(
            xpath='//span[@class="transition-content"]/ul/li'
        )
        for item in all_flight:
            # 解析航班号
            flight_num = self.get_text(
                xpath='./div[@class="select-detail--indicators"]',
                el=item
            )
            flight_num_list = re.findall(r"([0-9]{4})", flight_num)
            task_flight_num_list = [i[2:] for i in self.dep_flight_number.split("/")]
            # 校验任务的航班号

            if flight_num_list == task_flight_num_list:
                # 点击选中航班
                all_price = self.get_ele_list(
                    xpath='./div[@class="select-detail--fares"]',
                    el=item
                )[0].find_elements_by_xpath("./div")
                all_price.reverse()  # 反转顺序

                for ele in all_price:
                    price = ele.text
                    if price.lower() == "sold out":
                        continue
                    else:
                        self.click_btn(
                            xpath="./button",
                            el=ele
                        )
                        break
                else:
                    raise NoFlightException("该航班所有销售完毕")

                break
            else:
                continue
        else:
            raise NoFlightException("没有匹配到任务航班")
            pass

        func(self)

    return inner


# 校验选择的价格是否变价
def checkout_price_wrapper(func):
    def inner(self, *args, **kwargs):
        # 获取选中的价格, 不含税的价格
        sub_total = self.get_text(
            xpath='//div[@class="price-summary price-summary_last"]/div//span[@class="currency--symbol"]/following-sibling::span[1]'
        )
        tax_price = self.get_text(
            xpath='//div[@class="checkout-flight-total-summary"]//div[@class="summary--taxes-fees"]//span[@class="currency currency_dollars"]/span[2]'
        )[1:]

        total_price = self.get_text(
            xpath='//div[@class="checkout-flight-total-summary"]//div[@class="summary--flight-total"]//span[@class="currency currency_dollars"]/span[2]/span[2]'
        )

        # 对比含税的价格
        if self.task_flight_price < int(total_price.replace(",", "")):
            raise PriceException("页面价格大于任务配置价格！购买失败")

        func(self)

    return inner


# 填写乘客信息
def fill_passengers_wrapper(func):
    def inner(self, *args, **kwargs):
        gender_map = {
            "F": 2,
            "M": 1
        }

        # 获取所有的乘客输入面板
        all_passengers_table = self.get_ele_list(
            xpath='//div[@class="form-container form-container_simple flying-form"]//form/section'
        )
        for index, item in enumerate(all_passengers_table):
            # 乘客姓名
            passenger_info = self.passenger_list[index]
            last_name, first_name = passenger_info["name"].split("/")

            birthday_year, birthday_month, birthday_day = passenger_info["birthday"].split("-")

            gender = passenger_info["sex"]

            self.fill_input(
                xpath='./div/div[contains(@class, "first-name")]//input',
                content=first_name,
                el=item
            )

            self.fill_input(
                xpath='./div/div[contains(@class, "last-name")]//input',
                content=last_name,
                el=item
            )

            self.fill_input(
                xpath='./div/div[contains(@class, "birth")]//input[@aria-label="Day"]',
                content=birthday_day,
                el=item
            )

            self.fill_input(
                xpath='./div/div[contains(@class, "birth")]//input[@aria-label="Year"]',
                content=birthday_year,
                el=item
            )

            # 选择月份
            self.click_btn(
                xpath='./div/div[contains(@class, "birth")]//div[contains(@class, "month")]//input',
                content=birthday_year,
                el=item
            )
            self.click_btn(
                xpath=f'//ul[contains(@id, "BirthMonth")]/li[{int(birthday_month)}]'
            )

            # 选择性别
            self.click_btn(
                xpath='./div/div[contains(@class, "gender")]//input',
                content=birthday_year,
                el=item
            )
            self.click_btn(
                xpath=f'//ul[contains(@id, "passengerGender")]/li[{gender_map[gender]}]'
            )

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
