from selenium import webdriver

# ./Google Chrome --remote-debugging-port=9222
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:6666')

browser = webdriver.Chrome(chrome_options=chrome_options)

browser.get('https://www.southwest.com')


# profile = webdriver.FirefoxProfile()



# profile.set_preference('network.proxy.type', 1)
# profile.set_preference('network.proxy.http', '127.0.0.1')
# profile.set_preference('network.proxy.http_port', 6000)
# profile.set_preference('network.proxy.ssl', '127.0.0.1')
# profile.set_preference('network.proxy.ssl_port', 8080)
# profile.update_preferences()

# driver = webdriver.Firefox(profile)
# driver.get("http://www.baidu.com")

# driver = Remote(command_executor="")
