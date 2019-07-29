import os

BASEDIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

# MODE = "mobile"
MODE = "web"
# MODE = "POST"

CAEGORY = "FD"
# CAEGORY = ""

# 手机配置
PLATFORM = "Android"
DEVICE_NAME = "emulator-5554"

if CAEGORY == "FD":
    DEVICE_NAME = "0a2096f90105"
    APP_PACKAGE = "com.tencent.mm"
    APP_ACTIVITY = '.ui.LauncherUI'
else:
    # DEVICE_NAME = "983a9da7"
    APP_PACKAGE = "com.southwestairlines.mobile"
    APP_ACTIVITY = 'com.southwestairlines.mobile.splash.SplashActivity'

TIMEOUT = 40
DRIVER_SERVER = 'http://localhost:4723/wd/hub'

PROXY = True

BROWSER = "chrome"  # 最新版本的chrome访问失败，尝试使用firefox
# BROWSER = "firefox"

CLIENTTYPE = "WN_APP_CLIENT"
MACHINECODE = "wn-ip"

# redis 配置
REDIS_HOST = "47.92.31.231"
REDIS_PORT = 6379
REDIS_DB = 15
PASSWORD = "af42bc0ada00320c679db3d3ab4b0bf7"

# headers 名字
HEADERS = "HEADERS_QUEUE_THREE"

# 回填的数据类型
RESULT = {
    "accountPassword": "",
    "accountType": "",
    "accountUsername": "",
    "cardName": "",
    "cardNumber": "",
    "checkStatus": True,
    "clientType": CLIENTTYPE,  # 跑单的客户端码
    "createTaskStatus": True,
    "linkEmail": "",
    "linkEmailPassword": "",
    "linkPhone": "",
    "machineCode": MACHINECODE,  # 跑单客户端ip
    "nameList": [],  # 如果支持乘客分开出，nameList里放本次跑单成功的乘客姓名，单个也是集合
    "payTaskId": 0,
    "pnr": "",  # 跑单成功的pnr
    "price": 0.00,  # 支付的机票含税总价
    "baggagePrice": 0.00,  # 支付行李总价
    "sourceCur": "",
    "errorMessage": "",
    "status": "",  # 350 保留成功，301 保留失败， 450 支付成功 ，401 支付失败
    "targetCur": "",
    "promo": "",
    "creditEmail": "",
    "creditEmailCost": "",
}
