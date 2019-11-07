import json
import os
import time

import requests

from conf import config
from functionOther import csInfoLogin, csInfoFindByTaxNo
from tools import log


def run(taxNo, type, count):
    log.i('cs-info 文件上传')
    userName = '615891768@qq.com'
    pwd = '12345678',
    retLogin, userId = csInfoLogin.run(userName, pwd)
    if retLogin == 0:
        retFindByTaxNo, company, taxNo, id, uid, accountSystem, year, month, invoiceNo = csInfoFindByTaxNo.run(
            taxNo)
        if retFindByTaxNo == 0:
            kv = {
                'id': id,
                'uid': uid,
                'userId': userId,
                'company': company,
                'taxNo': taxNo,
                'year': year,
                'month': month,
                'type': type,
                'invoiceNo': invoiceNo,
                'origin': '1',
                'status': '1',
                'accountSystem': accountSystem}

            case_dir = os.path.dirname(os.path.dirname(__file__)) + '/testCases/tax.jpg'
            for i in range(count):
                files = {
                    'files': ('tax' + str(int(time.time())) + '.jpg',  # file是请求参数，要与接口文档中的参数名称一致
                              open(case_dir, 'rb'),  # 已二进制的形式打开文件
                              'application/msword')  # 上传文件的MIME文件类型，这个必须要有
                }  # 上传的文件
                response = requests.post(config.domain + '/cs-info/file/upload', params=kv, files=files,
                                         allow_redirects=False)
                response.encoding = 'utf-8'
                if response.status_code == 200:
                    ret = json.loads(response.text)
                    if ret['code'] == '200':
                        log.d('上传文件成功', i)

                    else:
                        log.e('上传文件失败 ：', i, ret['msg'])
                else:
                    log.e('上传文件失败 http请求失败：', i, response.status_code)
                    return 1
            log.i('上传文件完成')
            return 0
    #     else:
    #         log.e('上传文件失败 ：查询企业失败' )
    # else:
    #     log.e('上传文件失败 ：登录失败')
    return 1

if __name__ == "__main__":
    print('DbMonitor', str(int(time.time())))
    config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        run('91310116761150572C', 1, 2)
