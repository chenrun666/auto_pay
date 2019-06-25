import time
from loguru import logger

logger.add(
    f'../logs/log_{time.strftime("%Y-%m-%d", time.localtime())}.log',
    rotation="10 MB",
    retention="2 months"
)