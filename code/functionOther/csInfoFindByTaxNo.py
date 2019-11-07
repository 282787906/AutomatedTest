import json

import requests

from conf import config
from tools import log


def run(taxId):
    log.i('cs-info 查询企业')
    kv = {'taxNo': taxId}
    response = requests.get(config.domain + '/cs-info/customer/findByTaxNo', params=kv, allow_redirects=False)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        ret = json.loads(response.text)
        if ret['code'] == '200':
            year = ret['data']['currHjyYear']
            month = ret['data']['currHjyMonth']

            log.i('无年月查询成功')
            ret,company,taxNo, id, uid, accountSystem, year, month,   invoiceNo=runWithDate(taxId, year, month)
            if  ret!= 0:
                return 1
            else:
                return ret, company,taxNo,id, uid, accountSystem, year, month,   invoiceNo
        else:

            log.e('查询失败 ：', ret['msg'])
    else:
        log.e('登录失败 http请求失败：', response.status_code)

        return 1


def runWithDate(taxId, year, month):
    log.i('cs-info 带年月参数查询企业')
    kv = {'taxNo': taxId, 'year': year, 'month': month}
    response = requests.get(config.domain + '/cs-info/customer/findByTaxNo', params=kv, allow_redirects=False)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        ret = json.loads(response.text)
        if ret['code'] == '200':
            log.i('带年月参数查询成功')
            year = ret['data']['currHjyYear']
            month = ret['data']['currHjyMonth']
            id = ret['data']['id']
            uid = ret['data']['uid']
            accountSystem = ret['data']['accountSystem']
            invoiceNo = ret['data']['invoiceNo']
            taxNo = ret['data']['taxNo']
            company = ret['data']['company']
            return 0,company,taxNo, id, uid, accountSystem, year, month,  invoiceNo
        else:

            log.e('带年月参数查询失败', ret['msg'])
    else:
        log.e('登录失败 http请求失败：', response.status_code)

        return 1


if __name__ == "__main__":
    config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        run('91310116761150572C')
