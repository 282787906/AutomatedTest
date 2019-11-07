import os
import sys

import functionOther
from conf import config
from functionOther import dbMonitor
from tools import log


def paramInfo():
    str = os.path.basename(__file__) + '数据库状态监控'
    str = str + '\n参数说明:'
    str = str + '\n' + 'runWith:\t0-default;1-pycharm;2-Cmd'
    str = str + '\n' + 'host:\tonline-生产环境;pre-预发布环境'
    return str


if __name__ == "__main__":
    print('mainMonitor')

    if len(sys.argv) == 3 and (sys.argv[1] == '0' or sys.argv[1] == '1' or sys.argv[1] == '2') and (
            sys.argv[2] == 'online' or sys.argv[2] == 'pre'):
        config.set_runWith(sys.argv[1])
        config.set_host(sys.argv[2])
        dbMonitor.run()
    else:
        print(paramInfo())
