"""
获取任务
"""
import json
import time

import requests

from common.log import logger
from conf.settings import CLIENTTYPE, MACHINECODE


def get_task():
    """
    领任务
    :return: 返回任务的json格式， 统一返回data数据
    """
    taskheaders = {'Content-Type': 'application/json'}
    data = {
        "clientType": CLIENTTYPE,
        "machineCode": MACHINECODE
    }
    while True:
        try:
             # http://47.92.234.181:18008/book?carrier=JW&machineCode={data['machineCode']}
            taskJson = requests.post(f"http://47.92.119.88:18002/getBookingPayTask",
                                     data=json.dumps(data), headers=taskheaders)
            # taskJson = requests.get(f"http://47.92.234.181:18008/book?carrier=WN&machineCode=127.0.0.1",
            #                         data=json.dumps(data), headers=taskheaders)

            if taskJson.json()["data"]:
                logger.info(f"获取到任务：{taskJson.json()['data']}")
                return taskJson.json()["data"]
            else:
                print(taskJson.json(), type(taskJson.json()))
                print("没有任务，休息10秒")
                time.sleep(10)
        except Exception as e:
            logger.error("请求任务接口发生错误，错误提示：" + str(e))
            time.sleep(60)


def back_fill(data):
    logger.info(f"回填内容：{data}")
    taskheaders = {'Content-Type': 'application/json'}
    url = 'http://47.92.119.88:18002/bookingPayTaskResult'
    # url = 'http://47.92.234.181:18008/pnrVoResult'  # 跑单刷单
    response = requests.post(url, data=json.dumps(data), headers=taskheaders)
    if json.loads(response.text)["status"] == 'Y':
        logger.info('回填任务成功')
    else:
        logger.info(f'回传任务失败,错误信息：{response.text}')


if __name__ == '__main__':
    get_task()
