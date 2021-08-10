import json
import os

import requests

from conf import config
from tools import excelTools, log
from tools.mySqlHelper import insertBalance, insertBalanceBaseCode


def saveBalance(dicts, company):
    for balance in dicts:
        insertBalance(dicts[balance], company)
def saveBalanceBaseCode(dicts, company):
    for balance in dicts:
        insertBalanceBaseCode(dicts[balance], company)


def upladYiDaiZgangFiles(path, company):
    balancePath = ''
    documentPath = ''
    fixedAssetsPath = ''
    baseCodePath = ''
    list = os.listdir(path)
    for file in list:
        if file.find('余额表') > -1:
            balancePath = path + file
        elif file.find('凭证列表') > -1:
            documentPath = path + file
        elif file.find('固定资产') > -1:
            fixedAssetsPath = path + file
        elif file.find('科目表') > -1:
            baseCodePath = path + file

    kv = {'taxNo': company}
    files = dict()
    if os.path.isfile(balancePath):
        files['balance'] = ('余额表.xls', open(balancePath, 'rb'), 'application/msword')
    else:
        return 1, '上传文件失败 不存在余额表'
    if os.path.isfile(documentPath):
        files['document'] = ('凭证.xls', open(documentPath, 'rb'), 'application/msword')
    else:
        return 1, '上传文件失败 不存在凭证表'
    if os.path.isfile(fixedAssetsPath):
        files['fixedAssets'] = ('固定资产.xls', open(fixedAssetsPath, 'rb'), 'application/msword')
    else:
        return 1, '上传文件失败 不存在固定资产表'
    if os.path.isfile(baseCodePath):
        files['baseCode'] = ('科目表.xls', open(baseCodePath, 'rb'), 'application/msword')
    else:
        return 1, '上传文件失败 不存在科目表'
    response = requests.post('http://localhost:8180/fast_mab/mig/importFile', params=kv, files=files,
                             allow_redirects=False)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        ret = json.loads(response.text)
        if ret['result'] == 200:
            return 0, ret['message']
        else:
            return 1, '上传文件失败 http请求返回：' + ret['message']
    else:
        return 1, '上传文件失败 http请求失败：' + response.status_code


def importAll():
    list = os.listdir(config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG)
    times = 0
    for company in list:
        times = times + 1

        try:
            retCode, msg = upladYiDaiZgangFiles(config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG + company + "\\", company)
            if retCode != 0:
                log.e(str(times), '  导入文件失败：' + company + '  ' + msg)
            else:
                log.i(str(times), '  导入文件成功：' + company)
        except:
            log.exception(str(times), '  导入文件异常：' + company + '  ' + msg)

        # if times == 100:
        #     break
    log.i('导入文件完成   ' + str(len(list)))


def importOne(company):
    try:
        retCode, msg = upladYiDaiZgangFiles(config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG + company + "\\", company)
        if retCode != 0:
            log.e('导入文件失败：' + company + '  ' + msg)
        else:
            log.i('导入文件成功：' + company)
    except Exception  as e:
        log.exception(company + '  导入文件异常')


if __name__ == "__main__":
    print('main')
    # importAll()
    # importOne("张家港市鸿泉物流有限公司")


    path = 'D:\\seleniumTemp\\浪潮云\\'

    # if os.path.isfile(path+'湖北嘉明物流有限公司/科目表.xls'):
    #     log.e('科目表读取失败：')
    # else:
    #     log.e('科目表读取失败：')
    list = os.listdir(path)
    for file in list:
        company = file
        if os.path.isfile(path + file+'/科目表.xls'):
            retCode, dicts = excelTools.read_BalanceBaseCodeLangChao(path + file+'/科目表.xls')
            if retCode != 0:
                log.e('科目表读取失败：')
            saveBalanceBaseCode(dicts, company)
            log.i('科目表保存完成   '+company)


