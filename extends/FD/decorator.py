import time

from selenium.common.exceptions import NoSuchElementException

from .country import country_code

from common.myexception import NoFlightException, PriceException


def login_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


def clear_passengers_wrapper(func):
    def inner(self, *args, **kwargs):
        # 点击搜索
        self.click(
            xpath='//*[@resource-id="android:id/content"]/following-sibling::*[1]//android.support.v7.widget.LinearLayoutCompat/*[1]'
        )

        # 输入搜索内容
        self.send_keys(
            xpath='//android.widget.EditText[@text="搜索"]',
            content='亚洲航空'
        )

        # 点击亚洲航空
        self.click(
            xpath='//android.widget.TextView[@text="亚洲航空"]'
        )
        # 点击订机票
        self.click(
            xpath='//android.widget.TextView[@text="订机票"]'
        )

        # 点击常用信息
        self.click(
            xpath='//android.widget.TextView[@text="常用信息"]'
        )
        with self.switch_native_h5():
            # 修改联系人
            self.click(
                xpath='//span[contains(text(), "联系人")]'
            )
            # 点击修改
            self.click(
                xpath='//img[@class="edit"]'
            )

            last_name, first_name = self.contact["contactName"].split("/")
            # 修改联系人
            self.get_ele_list(
                xpath='//tr[@class="lastName"]//input'
            )[0].clear()
            self.fill_input(
                xpath='//tr[@class="lastName"]//input',
                content=last_name
            )
            self.get_ele_list(
                xpath='//tr[@class="firstName"]//input'
            )[0].clear()
            self.fill_input(
                xpath='//tr[@class="firstName"]//input',
                content=first_name
            )
            self.get_ele_list(
                xpath='//tr[@class="phone"]//input'
            )[0].clear()
            self.fill_input(
                xpath='//tr[@class="phone"]//input',
                content=self.contact["linkPhone"]
            )
            self.get_ele_list(
                xpath='//tr[@class="email"]//input'
            )[0].clear()
            self.fill_input(
                xpath='//tr[@class="email"]//input',
                content=self.contact["linkEmail"]
            )

            self.click(
                xpath='//div[@class="ok"]'
            )
            time.sleep(3)

            self.click(
                xpath='//span[contains(text(), "乘机人")]'
            )
            time.sleep(2)

            all_passengers = self.driver.find_elements_by_xpath(
                xpath='//div[@class="passengers"]/div'
            )
            for _ in all_passengers:
                self.driver.execute_script('document.querySelector("div.passengers div.operations").click()')
                time.sleep(1)
                self.click(
                    xpath='//div[contains(text(), "确定")]'
                )
                time.sleep(1)

        self.click(
            xpath='//android.widget.TextView[@text="我的常用信息"]/../preceding-sibling::*[1]'
        )

        func(self)

    return inner


def open_public_wrapper(func):
    def inner(self, *args, **kwargs):
        # 点击订机票
        self.click(
            xpath='//android.widget.TextView[@text="订机票"]'
        )
        time.sleep(1)
        self.click(
            xpath='//android.widget.TextView[@text="机票预订"]'
        )
        func(self)

    return inner


def search_flight_wrapper(func):
    def inner(self, *args, **kwargs):
        with self.switch_native_h5():  # f就是self
            # 进行H5页面操作
            self.click(
                xpath='//span[contains(text(), "单程")]'
            )

            # 点击出发地
            self.click(
                xpath='//div[@class="where-area"]//div[@class="departure"]/div'
            )
            self.fill_input(
                xpath='//input[@type="search"]',
                content=self.dep_airport
            )
            self.click(
                xpath=f'//div[contains(text(), "{self.dep_airport}")]'
            )

            # 选择目的地
            self.click(
                xpath='//div[@class="where-area"]//div[@class="destination"]/div'
            )
            self.fill_input(
                xpath='//input[@type="search"]',
                content=self.arr_airport
            )
            self.click(
                xpath=f'//div[contains(text(), "{self.arr_airport}")]'
            )

            # 选择日期
            date_map = {
                "01-01": "元旦",
                "02-14": "情人节",
                "03-08": "妇女节",
                "05-01": "劳动节",
                "06-01": "儿童节",
                "07-01": "建党节",
                "09-10": "教师节",
                "10-01": "国庆节",
                "12-24": "平安夜",
                "12-25": "圣诞节",
            }
            self.click(
                xpath='//div[@class="when-area"]/span'
            )
            year, month, day = self.dep_date.split("-")
            if date_map.get(f"{month}-{day}"):
                day = date_map[f"{month}-{day}"]
            self.click(
                xpath=f'//div[contains(text(), "{year}年{month}月")]/following-sibling::*[1]//div[contains(text(), "{day}")]'
            )

            # 选择 成人 人数
            page_adult_num = self.get_text(
                xpath='//div[contains(text(), "成人")]/../following-sibling::*[1]/div[@class="num"]'
            )
            adult_num_distance = int(self.adult) - int(page_adult_num)
            if adult_num_distance > 0:
                direction = '+'
            else:
                direction = '-'

            for item in range(abs(adult_num_distance)):
                self.click(
                    xpath=f'//div[contains(text(), "成人")]/../following-sibling::*[1]/div[contains(text(), "{direction}")]'
                )

            # 选择 儿童 人数
            page_child_num = self.get_text(
                xpath='//div[contains(text(), "儿童")]/../following-sibling::*[1]/div[@class="num"]'
            )
            child_num_distance = int(self.child) - int(page_child_num)
            if child_num_distance > 0:
                direction = '+'
            else:
                direction = '-'

            for item in range(abs(child_num_distance)):
                self.click(
                    xpath=f'//div[contains(text(), "儿童")]/../following-sibling::*[1]/div[contains(text(), "{direction}")]'
                )

            # 点击搜索
            self.click(
                xpath='//a[contains(text(), "立即搜索")]'
            )

        func(self)

    return inner


def select_flight_wrapper(func):
    def inner(self, *args, **kwargs):
        with self.switch_native_h5():
            all_flights_list = self.get_ele_list(
                xpath='//div[@class="flight"]'
            )
            for flight_info in all_flights_list:
                # 获取航班号
                page_flight_num = self.get_text(
                    xpath='.//div[@class="schedule"]',
                    el=flight_info
                ).split("\n")
                page_flight_num.pop(-1)
                page_flight_num = [''.join(item.split()) for item in page_flight_num]

                if page_flight_num == self.dep_flight_number.split("/"):
                    self.click_btn(
                        xpath='.//div[@class="schedule"]',
                        el=flight_info
                    )
                    break
            else:
                raise NoFlightException("没有匹配到航班")

        func(self)

    return inner


def check_flight_price_wrapper(func):
    def inner(self, *args, **kwargs):
        # 获取总价
        with self.switch_native_h5():
            amount = self.get_text(
                xpath='//div[@class="amount"]'
            ).replace(",", "")

            page_flight_total_price = float(amount)

            task_flight_total_price = ((self.task_flight_price * 100) * len(self.passenger_list)) / 100

            if page_flight_total_price > task_flight_total_price:
                raise PriceException(f"页面总价为: {page_flight_total_price}。 任务总价格为: {task_flight_total_price}")

            self.click(
                xpath='//div[@class="next"]'
            )

        func(self)

    return inner


def fill_passengers_info_wrapper(func):
    def inner(self, *args, **kwargs):
        gender_map = {
            "M": "0",
            "F": "1"
        }

        for passenger in self.passenger_list:
            with self.switch_native_h5():
                # 点击新增
                self.click(
                    xpath='//div[@class="add"]'
                )
                # 输入名字
                last_name, first_name = passenger["name"].split("/")
                self.fill_input(
                    xpath='//tr[@class="lastname"]//input',
                    content=last_name
                )
                self.fill_input(
                    xpath='//tr[@class="firstname"]//input',
                    content=first_name
                )

                # 选择性别
                self.click(
                    xpath=f'//input[@value="{gender_map[passenger["sex"]]}"]'
                )

                # 选择国籍
                self.click(
                    xpath=f'//option[@value="{passenger["nationality"]}"]'
                )

                # 选择出生日期
                birthday_year, birthday_mon, birthday_day = passenger["birthday"].split("-")
                if int(birthday_day) > 27:
                    birthday_day = int(birthday_day) - 1
                else:
                    birthday_day = int(birthday_day) + 1
                fake_birthday = f"{birthday_year}-{birthday_mon}-{birthday_day}"
                self.driver.execute_script(
                    f'document.querySelector("tr.birthday input").value = "{fake_birthday}"'
                )
                self.click(
                    xpath=f'//tr[@class="birthday"]//input'
                )
            select_birthday(self, passenger["birthday"])

            # 点击确定
            with self.switch_native_h5():
                self.click(xpath='//div[@class="ok"]')

            time.sleep(2)

        func(self)

    return inner


def select_contact_wrapper(func):
    def inner(self, *args, **kwargs):
        # 选择联系人
        with self.switch_native_h5():
            self.click(
                xpath='//div[contains(@class, "contacts")]//span'
            )
            time.sleep(2)
            self.driver.execute_script("document.querySelector('div.contact span').click()")
            time.sleep(1)
            self.click(
                xpath='//div[contains(text(), "确定")]'
            )

        func(self)

    return inner


def select_luggage_wrapper(func):
    def inner(self, *args, **kwargs):
        with self.switch_native_h5():
            self.click(
                xpath='//div[contains(@class, "baggages")]'
            )
            self.click(
                xpath='//div[@class="bar"]/following-sibling::*[1]//div[@class="seperate"]'
            )

            all_passenger_select = self.get_ele_list(
                xpath='//div[@class="options"]//select'
            )
            all_passenger_select.pop(-1)

            for index, item in enumerate(all_passenger_select):
                passenger_luggage_weight = self.passenger_list[index]["baggageWeight"]
                if passenger_luggage_weight == 0:
                    continue
                # 获取当前的行李索引

                luggage_index_list = [item.text.split()[0] for item in item.find_elements_by_xpath("./option")]
                luggage_index = luggage_index_list.index(f"{passenger_luggage_weight}kg")

                self.select_something(
                    xpath='../select',
                    el=item,
                    index=luggage_index
                )

            self.click(
                xpath='//a[contains(text(), "确定")]'
            )

        func(self)

    return inner


def check_selected_info_wrapper(func):
    def inner(self, *args, **kwargs):
        with self.switch_native_h5():
            # 获取票价
            # page_adult_total_price = self.get_text(
            #     xpath='//div[contains(text(), "成人票")]/following-sibling::*[1]'
            # ).split()[0][1:]
            self.click(
                xpath='//*[contains(text(), "明细")]'
            )
            detail_info = self.get_ele_list(
                xpath='//div[@class="detail-wrapper"]//div[@class="item"]'
            )

            pass

        func(self)

    return inner


def select_birthday(self, target_birthday):
    target_year, target_month, target_day = target_birthday.split("-")

    # 选择天
    self.click(
        xpath=f'//android.view.View[contains(@content-desc, "{target_day}")]'
    )

    # 点击设置
    self.click(
        xpath='//android.widget.Button[@text="设置"] | //android.widget.Button[@text="确定"]'
    )
