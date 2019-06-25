from common.task import get_task, back_fill
from support.application_payment import *

if __name__ == '__main__':
    task = get_task()

    wn = WN(task)
    result = wn.main()

    back_fill(result)
