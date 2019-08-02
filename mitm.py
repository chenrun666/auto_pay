import requests, json

import mitmproxy.http
from mitmproxy import ctx

headers = {}


# def response(flow):
#     """截取连接更换加密参数"""
#     if "api/air-booking/v1/air-booking/page/air/booking/price" in flow.request.url:
#         flow.request.headers["x-5ku220jw-b"] = headers["x-5ku220jw-b"]
#         flow.request.headers["x-5ku220jw-c"] = headers["x-5ku220jw-c"]
#         flow.request.headers["x-user-experience-id"] = headers["x-user-experience-id"]
#         flow.request.headers["x-5ku220jw-uniquestatekey"] = headers["x-5ku220jw-uniquestatekey"]
#         flow.request.headers["x-5ku220jw-a"] = headers["x-5ku220jw-a"]
#         flow.request.headers["x-api-key"] = headers["x-api-key"]

def response(flow):
    """firefox 屏蔽webdriver"""
    if """</head>""" in flow.response.text:
        flow.response.text = flow.response.text.replace("""</head>""",
                                                        '''</head><script type="text/javascript">delete window.navigator.__proto__.webdriver;</script>''')
