import re
import time

from common.myexception import NoFlightException, PriceException, SelectedInfoException


def login_wrapper(func):
    def inner(self, *args, **kwargs):
        func(self)

    return inner


def clear_passengers_wrapper(func):
    def inner(self, *args, **kwargs):
        time.sleep(2)
        # 点击搜索
        self.click(
            xpath='//*[@resource-id="android:id/content"]/following-sibling::*[1]//android.support.v7.widget.LinearLayoutCompat/*[1]'
        )
        time.sleep(2)

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
        time.sleep(3)

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

            # 获取日期
            flight_date = self.get_text(
                xpath='//div[@class="today actived"]/div[1]'
            )

            if all_flights_list:
                # 判断路线正确
                start_code, end_code = re.findall(r".*?\((.*?)\)", all_flights_list[0].text)

                if self.dep_airport != start_code or self.arr_airport != end_code or self.dep_date != flight_date:
                    raise Exception("路线选择错误。重新选择")

            for flight_info in all_flights_list:
                # 获取航班号
                page_flight_num = self.get_ele_list(
                    xpath='.//div[@class="schedule"]',
                    el=flight_info
                )[-1].text.split("\n")
                page_flight_num.pop(-1)
                page_flight_num = [''.join(item.split()) for item in page_flight_num]

                if page_flight_num == self.dep_flight_number.split("/"):
                    flight_info.click()
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
                # 区分儿童的add按钮
                if self.passenger_list.index(passenger) + 1 <= self.adult:
                    self.click(
                        xpath='//div[@class="add"]'
                    )
                else:
                    self.click(
                        xpath='//div[@class="kids"]//div[@class="add"]'
                    )
                # 输入名字
                last_name, first_name = passenger["name"].split("/")
                self.fill_input(
                    xpath='//tr[@class="lastname"]//input',
                    content=last_name
                )
                self.fill_input(
                    xpath='//tr[@class="firstname"]//input',
                    content=first_name.replace(" ", "")
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
                fake_birthday = f"{birthday_year}-{birthday_mon}-{str(birthday_day).zfill(2)}"
                self.driver.execute_script(
                    f'document.querySelector("tr.birthday input").value = "{fake_birthday}"'
                )
                self.click(
                    xpath=f'//tr[@class="birthday"]//input'
                )
                time.sleep(1)
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
                xpath='//div[@class="detail"]'
            )
            time.sleep(1)
            # 获取所有明细
            detail_info = self.get_ele_list(
                xpath='//div[contains(@class, "detail-wrapper")]//div[@class="item"]'
            )

            # 判断币种是否是人民币
            if self.get_text(
                    xpath='//div[contains(text(), "成人票")]/following-sibling::*[1]'
            )[0] != "￥":
                raise PriceException("支付币种不是人民币。请检查航班币种")

            flight_total_price = 0
            luggage_sum_weight = 0
            luggage_sum_price = 0
            for item in detail_info:
                if "成人票" in item.text or "儿童票" in item.text:
                    total_price = float(re.findall(r"(\d+\.{0,1}\d+)?\s{2}", item.text)[0].replace(",", ""))
                    flight_total_price += total_price
                elif "托运行李" in item.text:
                    luggage_weight, luggage_price = re.findall(r"(\d+)kg.*?(\d+[.]{0,1}\d+)?\s{2}", item.text, re.S)[0]
                    luggage_sum_weight += float(luggage_weight)
                    luggage_sum_price += float(luggage_price)

                # 回填支付价格和行李价格
            self.back_fill["price"] = flight_total_price
            self.back_fill["baggagePrice"] = luggage_sum_price

            # 校验行李重量是否正确
            if luggage_sum_weight != sum(map(lambda x: int(x["baggageWeight"]), self.passenger_list)):
                raise SelectedInfoException("行李选择错误。请重新执行该任务！！")

            # 校验价格是否超出任务价格
            if flight_total_price > self.task_flight_price * len(self.passenger_list):
                raise PriceException("价格超出了任务价格")

            self.click(
                xpath='//div[@class="detail"]'
            )
            time.sleep(1)

            self.scroll_screen(el='//div[@class="button-wrapper"]')
            time.sleep(1)
            # 点击提交订单
            self.click(
                xpath='//div[@class="button-wrapper"]'
            )
            # 关闭提示
            self.click(
                xpath='//div[text()="确定"]'
            )

        func(self)

    return inner


def check_passengers_info_wrapper(func):
    def inner(self, *args, **kwargs):
        gender_map = {
            "先生": "M",
            "女士": "F",
            "女童": "F",
            "男童": "M"
        }

        # 检查乘机人信息是否正确
        with self.switch_native_h5():
            # 获取所有的乘客信息
            all_passengers_info = self.get_ele_list(
                xpath='//table[@class="passenger"]'
            )
            for index, passenger in enumerate(all_passengers_info):
                page_passenger_first_name, page_passenger_last_name = re.findall(
                    r"([A-Z \s]+)",
                    self.get_text(xpath='.//td[2]', el=passenger)
                )[0].strip().split()
                gender = self.get_text(
                    xpath='./tr[2]/td[2]',
                    el=passenger
                )
                birthday = self.get_text(
                    xpath='./tr[3]/td[2]',
                    el=passenger
                )
                if self.passenger_list[index]["name"].replace(" ", "").upper() != \
                        f"{page_passenger_last_name}/{page_passenger_first_name}" \
                        or self.passenger_list[index]["sex"] != gender_map[gender] \
                        or self.passenger_list[index]["birthday"] != birthday:
                    raise SelectedInfoException("乘客信息填写有误，请重新执行该任务！！！")

            # 点击同意条款
            self.click(
                xpath='//div[@class="part agreement"]//img'
            )

            # 点击下一步
            self.click(
                xpath='//div[@class="next"]'
            )

            pass

        func(self)

    return inner


def payment_wrapper(func):
    def inner(self, *args, **kwargs):
        self.back_fill["status"] = 440

        self.get_ele_list(
            xpath='//android.widget.TextView[contains(@text, "请输入支付密码")]'
        )
        time.sleep(5)
        screen_info = self.driver.get_window_size()
        width, height = screen_info['width'], screen_info['height']

        start_width = int((width / 3) // 2)
        start_height = int(height / 4) * 3

        x_distance = int(width / 3)
        y_distance = int((height - start_height) // 4)

        password = "102928"

        for num in password:
            # 计算几排几列。整除特殊处理

            res, more = divmod(int(num), 3)
            if res == 0 and more == 0:
                res = 3
                more = 2
            elif more == 0:
                more = 3
                res -= 1

            x = start_width + x_distance * (more - 1)
            y = start_height + y_distance * res
            self.driver.tap([(x, y)])

        print("输入完成")

        # 获取实际来支付价格
        total_price = float(self.get_text(
            xpath='//android.widget.TextView[contains(@text, "¥")]/following-sibling::*[1]'
        ).replace(",", ""))

        back_price = ((total_price * 100) - (self.back_fill["baggagePrice"] * 100)) / 100
        self.back_fill["price"] = back_price

        self.click(
            xpath='//android.widget.Button[contains(@text, "完成")]'
        )

        func(self)

    return inner


def get_pnr_wrapper(func):
    def inner(self, *args, **kwargs):
        time.sleep(8)
        # 获取票号
        try:
            with self.switch_native_h5():
                pnr = self.get_text(
                    xpath='//strong[@class="weui-dialog__title"]/../following-sibling::*[1]'
                ).split(":")[1]
                self.back_fill["pnr"] = pnr
                self.back_fill["status"] = 450
        except Exception:
            pass

        func(self)

    return inner


def select_birthday(self, target_birthday):
    month_map = {
        "01": "一",
        "02": "二",
        "03": "三",
        "04": "四",
        "05": "五",
        "06": "六",
        "07": "七",
        "08": "八",
        "09": "九",
        "10": "十",
        "11": "十一",
        "12": "十二",
    }
    target_year, target_month, target_day = target_birthday.split("-")
    time.sleep(1)
    # 选择天
    self.click(
        xpath=f'//android.view.View[@content-desc="{target_day} {month_map[target_month]}月 {target_year}"]'
    )
    time.sleep(1)

    # 点击设置
    self.click(
        xpath='//android.widget.Button[@text="设置"] | //android.widget.Button[@text="确定"]'
    )
