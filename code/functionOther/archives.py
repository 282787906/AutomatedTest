import json
import os
import shutil
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird, loginNew
from module.Kemuyueb import dict2Kemuyueb
from tools import log, commonSelenium, excelTools
from tools.mySqlHelper import getMigCompany


def run(driver):
    log.d('余额表')
    dictsApi = {}
    try:
        params = {'origin': 'zidh',
                  'taxNo': config.caseTaxId,
                  'year': config.caseCurrentAccountYear,
                  'startMonth': config.caseCurrentAccountMonth,
                  'endMonth': config.caseCurrentAccountMonth}
        log.i('API 余额表获取', config.domain_api)
        response = requests.get(config.domain_api + '/api/report/balance', params=params, allow_redirects=False)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            ret = json.loads(response.text)
            if str(ret['code']) == '200':
                dicts = ret['data']
                for dict in dicts:
                    if dict['beginningBalanceDebit'] == dict['beginningBalanceCrebit'] == dict['currentAmountDebit'] \
                            == dict['currentAmountCrebit'] == dict['endingBalanceDebit'] == dict[
                        'endingBalanceCrebit'] == '0.00':
                        continue
                    km = dict2Kemuyueb(dict)
                    dictsApi[km.accountCode] = km
            else:

                log.e('API 余额表获取失败：', response.text)
                return 1
        else:
            log.e('API 余额表获取失败HTTP：', response.status_code)
            return 1
        log.i('API 余额表获取成功：')
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            time.sleep(config.FAIL_WAIT_SLEEP)
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/cer/balance/balanceList"):
            return 1

        driver.find_element_by_id('startMonth').find_elements_by_tag_name("option")[
            config.caseCurrentAccountMonth - 1].click()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        driver.find_element_by_id('endMonth').find_elements_by_tag_name("option")[
            config.caseCurrentAccountMonth - 1].click()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        shutil.rmtree(config.FILE_DOWNLOAD)
        os.mkdir(config.FILE_DOWNLOAD)
        driver.find_element_by_id('downloadBtn').click()
        times = 0
        maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
        while times < maxTimes:
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
            if '数据导出并下载成功' in driver.find_element_by_class_name('bootbox-body').text:
                driver.find_element_by_class_name('btn-primary').click()
                break
            if times == maxTimes:
                log.e("余额表-余额表下载超时")
                return 1
            times = times + 1

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        retCode, dictsDownload = excelTools.read_balanceList()
        if retCode != 0:
            time.sleep(config.FAIL_WAIT_SLEEP)
            log.e('余额表批量下载失败：')
            return 1
        if len(dictsDownload) - 1 != len(dictsApi):
            log.e('API余额表数量与下载数量不一致 dictsDownload:', str(len(dictsDownload)), 'listsApi:', str(len(dictsApi)))

            return 1

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        driver.find_element_by_id('doFind').click()

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        rows = driver.find_elements_by_xpath("//table[@id='customerTable']/tbody/tr")
        for i in range(len(rows)):
            if i < 2:
                continue
            tdsSum = rows[i].find_elements_by_tag_name("td")
            code = tdsSum[0].text
            name = tdsSum[1].text
            qcDebit = float('0.00' if (tdsSum[2].text == '') else tdsSum[2].text.replace(',', ''))
            qcCrebit = float('0.00' if (tdsSum[3].text == '') else tdsSum[3].text.replace(',', ''))

            bqDebit = float('0.00' if (tdsSum[4].text == '') else tdsSum[4].text.replace(',', ''))
            bqCrebit = float('0.00' if (tdsSum[5].text == '') else tdsSum[5].text.replace(',', ''))

            qmDebit = float('0.00' if (tdsSum[6].text == '') else tdsSum[6].text.replace(',', ''))
            qmCrebit = float('0.00' if (tdsSum[7].text == '') else tdsSum[7].text.replace(',', ''))
            if i == len(rows) - 1:
                if qcDebit != qcCrebit or bqDebit != bqCrebit or qmDebit != qmCrebit:
                    log.e('页面合计不平衡', qcDebit, qcCrebit, bqDebit, bqCrebit, qmDebit, qmCrebit)
                    return 1
                else:
                    if dictsDownload.get('sum').beginningBalanceDebit != qcDebit \
                            or dictsDownload.get('sum').beginningBalanceCrebit != qcCrebit \
                            or dictsDownload.get('sum').currentAmountDebit != bqDebit \
                            or dictsDownload.get('sum').currentAmountCrebit != bqCrebit \
                            or dictsDownload.get('sum').endingBalanceDebit != qmDebit \
                            or dictsDownload.get('sum').endingBalanceCrebit != qmCrebit:
                        log.e('页面与下载文件合计对比失败', '\n', '页面结果：\t', name, qcDebit, qcCrebit, bqDebit, bqCrebit, qmDebit,
                              qmCrebit,
                              '\n',
                              '下载文件:\t',
                              dictsDownload.get('sum').beginningBalanceDebit,
                              dictsDownload.get('sum').beginningBalanceCrebit,
                              dictsDownload.get('sum').currentAmountDebit,
                              dictsDownload.get('sum').currentAmountCrebit,
                              dictsDownload.get('sum').endingBalanceDebit,
                              dictsDownload.get('sum').endingBalanceCrebit
                              )
                        return 1
                    else:
                        log.i('页面合计', qcDebit, qcCrebit, bqDebit, bqCrebit, qmDebit, qmCrebit)
                break
            continue

            # else:
            #     log.d('页面接口对比通过', code, str(i) + '/' + str(len(rows)))
        log.i('页面接口对比通过')
        return 0
    except:

        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('余额表', r.status_code)

        return 1


def 归档上传_易代账(host, site):
    retCode, companies, msg = getMigCompany(site)
    if retCode != 0:
        log.e(msg)

        return
    for index in range(len(companies)):
        jindu = str(index + 1) + '/' + str(len(companies))
        name = companies[index].companyName.strip()
        taxNo = companies[index].taxNo.strip()
        startYear = companies[index].startYear
        currentYear = companies[index].currentYear
        # path = config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG + name + '\\'
        path = config.FILE_DOWNLOAD_COMPANY_LANGCHAOYUN + name + '\\'
        if path.endswith('*\\'):
            path = path.replace('*\\', '\\')
        if not os.path.isdir(path):
            os.mkdir(path)
        log.e(jindu, taxNo, name, str(startYear), str(currentYear))
        if currentYear > 2020:

            count = 2020 - startYear + 1
        else:
            count = currentYear - startYear + 1
        list = os.listdir(path)
        if len(list) != count:
            log.e('len(list)!=count', str(count), str(len(list)))
            return
        for file in list:
            if site=='浪潮':
                uploadPath = taxNo + "/" + file[-8:-4]
            else:
                uploadPath = taxNo + "/" + file[-12:-8]
            log.d('上传路径：', path)
            kv = {
                'uid': "d23e61eaa36611eb8cf900163e1209b5",
                'path': uploadPath,
                # 'tags': '易代账归档,' + site + ',' + taxNo}
                'tags':  site + ',' + taxNo}

            case_dir = path + file

            files = {
                'multipartFile': (file,  # file是请求参数，要与接口文档中的参数名称一致
                                  open(case_dir, 'rb'),  # 已二进制的形式打开文件
                                  'application/msword')  # 上传文件的MIME文件类型，这个必须要有
            }  # 上传的文件
            requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
            s = requests.session()
            s.keep_alive = False  # 关闭多余连接
            response = requests.post(host + '/file/upload', params=kv, files=files,
                                     allow_redirects=False)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                ret = json.loads(response.text)
                if ret['code'] == 200:
                    log.d('上传文件成功')

                else:
                    log.e('上传文件失败 ：', ret['msg'])
            else:
                log.e('上传文件失败 http请求失败：', response.status_code)
                return 1


if __name__ == "__main__":
    print('main')
    site = '浪潮'
    host = 'http://localhost:8083/archives'
    # host = 'https://caitest.75force.com/archives'
    # host = 'http://220.196.40.243:18080/archives'
    # host = 'https://75force.jink7.com/archives'
    归档上传_易代账(host, site)
