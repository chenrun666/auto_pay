"""
出票的执行流程
"""
import re

from common.myexception import NoFlightException, PriceException  # 自定义异常信息


# 选择目标航班
def select_flight_wrapper(func):
    def inner(self, *args, **kwargs):
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
def checkout_price(func):
    def inner(self, *args, **kwargs):
        # 获取选中的价格
        selected_price = self.get_text(
            xpath='//div[contains(@class, "fare-button_selected")]/button'
        )[1:]

        if self.task_flight_price < int(selected_price):
            raise PriceException("页面价格大于任务配置价格！购买失败")

        func(self)

    return inner
