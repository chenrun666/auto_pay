import redis, json

from common.log import logger

from conf.settings import HEADERS
from conf.settings import REDIS_PORT, REDIS_HOST, REDIS_DB, PASSWORD


class Redis:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.db = redis.Redis(host=host, port=port, decode_responses=True, db=REDIS_DB, password=PASSWORD)

    def header(self):
        try:
            headers = json.loads(self.db.lpop(HEADERS))
            headers["authority"] = headers.pop(":authority")
            return headers
        except Exception as e:
            logger.error(f"获取请求头失败，错误提示:{e}")


rdb = Redis()
