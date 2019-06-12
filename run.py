from support.payment import *

if __name__ == '__main__':
    if DEBUG:
        with open("../files/fake_data.json", "r", encoding="utf-8") as f:
            fake_task = f.read()
        wn = WN(json.loads(fake_task))
        wn.main()
