import time

from contextlib import contextmanager

from appium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException

from conf.settings import PLATFORM, DEVICE_NAME, APP_PACKAGE, APP_ACTIVITY, DRIVER_SERVER, TIMEOUT, BASEDIR


class Action:
    def __init__(self, url=None):
        self.desired_caps = {
            'platformName': PLATFORM,
            'deviceName': DEVICE_NAME,
            'appPackage': APP_PACKAGE,
            'appActivity': APP_ACTIVITY,
            'noReset': True,
            # 隐藏键盘
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'newCommandTimeout': 5000,
            'adbExecTimeout': 50000,
            # 'avdReadyTimeout': '300000',
            # "automationName": 'UiAutomator2'  # UiAutomator2
        }

        # 获取手机的唯一标示
        self.desired_caps["deviceName"] = "a2cdacf7"
        self.desired_caps["chromeOptions"] = {'androidProcess': 'com.tencent.mm:tools'}
        self.desired_caps["autoGrantPermissions"] = True

        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

        if url:
            self.driver.get(url)

    def click(self, xpath):
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        )).click()

    def send_keys(self, xpath, content):
        obj = self.get_obj_list(xpath=xpath)[0]
        obj.click()
        obj.set_text(content)

    def get_app_text(self, xpath):
        content = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        )).text
        return content

    def swipe(self, distance, direction="UP", duration=1000):
        """
        滑动屏幕
        :param distance: 滑动的距离 UP DOWN lEFT RIGHT
        :return:
        """
        # 获取屏幕大小
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]

        start_x = width * 0.5
        start_y = height * 0.5

        if direction == "UP" or direction == "DOWN":
            # 向上或向下 x 轴坐标不动
            end_x = start_x
        else:
            # 向左或右 y 轴坐标不动
            end_y = start_y

        if direction == "UP":
            end_y = start_y - distance
        elif direction == "LEFT":
            end_x = start_x + distance
        elif direction == "RIGHT":
            end_x = start_x - distance
        else:
            end_y = start_y + distance

        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        time.sleep(0.5)

    def get_obj_list(self, xpath):
        obj_list = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, xpath)
        ))
        return obj_list

    # 管理切换原生app和H5页面
    @contextmanager
    def switch_native_h5(self):
        context_list = self.driver.contexts
        self.driver.switch_to.context(context_list[1])

        yield

        self.driver.switch_to.context(context_list[0])
