import sys

import functionOther
from conf import config
from functionOther import dbMonitor
from tools import log

if __name__ == "__main__":
    print('mainMonitor')

    if len(sys.argv) == 2 and str(sys.argv[1]) == '0':
        print('change config.runInPycharm')
        config.set_runInPycharm(0)
    else:
        print('默认参数')
        dbMonitor.run()
