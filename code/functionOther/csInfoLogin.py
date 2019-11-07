import json

import requests

from conf import config
from tools import log


def run(userName ,pwd):
    log.i('cs-info 登录')
    kv = {'userName': userName, 'pwd': pwd}
    response = requests.get(config.domain + '/cs-info/user/login', params=kv, allow_redirects=False)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        ret = json.loads(response.text)
        if ret['code'] == '200':
            log.i('登录成功')
            return 0 ,ret['data']['id']
        else:

            log.e('登录失败 ：', ret['msg'])
    else:
        log.e('登录失败 http请求失败：', response.status_code)

        return 1


if __name__ == "__main__":
    print('DbMonitor')
    config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        run('615891768@qq.com','12345678')
