DEBUG = True

# MODE = "mobile"
MODE = "web"
# MODE = "POST"


# 手机配置
PLATFORM = "Android"
DEVICE_NAME = "983a9da7"
APP_PACKAGE = "com.southwestairlines.mobile"
APP_ACTIVITY = 'com.southwestairlines.mobile.splash.SplashActivity'
TIMEOUT = 30
DRIVER_SERVER = 'http://localhost:4723/wd/hub'

PROXY = True

BROWSER = "chrome"  # 最新版本的chrome访问失败，尝试使用firefox
# BROWSER = "firefox"

CLIENTTYPE = ""
MACHINECODE = ""

# redis 配置
REDIS_HOST = "47.92.31.231"
REDIS_PORT = 6379
REDIS_DB = 15
PASSWORD = "af42bc0ada00320c679db3d3ab4b0bf7"

# headers 名字
HEADERS = "HEADERS_QUEUE_THREE"
