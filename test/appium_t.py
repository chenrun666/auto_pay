from appium import webdriver

from conf.settings import *

desired_caps = {
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
    "automationName": 'UiAutomator'  # UiAutomator2
}

driver = webdriver.Remote(DRIVER_SERVER, desired_caps)

pass
driver.quit()
driver.close_app()