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


def run(driver):
    log.d('余额表')
    dictsApi = {}
    try:
        params = {'origin': 'zidh',
                  'taxNo': config.caseTaxId,
                  'year': config.caseCurrentAccountYear,
                  'startMonth': config.caseCurrentAccountMonth,
                  'endMonth': config.caseCurrentAccountMonth}
        log.i('API 余额表获取',config.domain_api)
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
            qcDebit =float( '0.00' if (tdsSum[2].text == '') else tdsSum[2].text.replace(',', ''))
            qcCrebit =float( '0.00' if (tdsSum[3].text == '') else tdsSum[3].text.replace(',', ''))

            bqDebit = float('0.00' if (tdsSum[4].text == '') else tdsSum[4].text.replace(',', ''))
            bqCrebit =float( '0.00' if (tdsSum[5].text == '') else tdsSum[5].text.replace(',', ''))

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
                        log.e('页面与下载文件合计对比失败',  '\n', '页面结果：\t', name, qcDebit, qcCrebit, bqDebit, bqCrebit, qmDebit, qmCrebit,
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
            if dictsApi.get(code).beginningBalanceDebit == dictsDownload.get(code).beginningBalanceDebit == qcDebit \
                    and dictsApi.get(code).beginningBalanceCrebit == dictsDownload.get(
                code).beginningBalanceCrebit == qcCrebit \
                    and dictsApi.get(code).currentAmountDebit == dictsDownload.get(
                code).currentAmountDebit == bqDebit \
                    and dictsApi.get(code).currentAmountCrebit == dictsDownload.get(
                code).currentAmountCrebit == bqCrebit \
                    and dictsApi.get(code).endingBalanceDebit == dictsDownload.get(
                code).endingBalanceDebit == qmDebit \
                    and dictsApi.get(code).endingBalanceCrebit == dictsDownload.get(
                code).endingBalanceCrebit == qmCrebit:
                log.e('页面接口对比失败', code, '\n', '页面结果：\t', name, qcDebit, qcCrebit, bqDebit, bqCrebit, qmDebit, qmCrebit,
                      '\n', '接口结果:\t',
                      dictsApi.get(code).beginningBalanceDebit,
                      dictsApi.get(code).beginningBalanceCrebit,
                      dictsApi.get(code).currentAmountDebit,
                      dictsApi.get(code).currentAmountCrebit,
                      dictsApi.get(code).endingBalanceDebit,
                      dictsApi.get(code).endingBalanceCrebit, '\n',
                      '下载文件:\t',
                      dictsDownload.get(code).beginningBalanceDebit,
                      dictsDownload.get(code).beginningBalanceCrebit,
                      dictsDownload.get(code).currentAmountDebit,
                      dictsDownload.get(code).currentAmountCrebit,
                      dictsDownload.get(code).endingBalanceDebit,
                      dictsDownload.get(code).endingBalanceCrebit
                      )
                return 1
            # else:
            #     log.d('页面接口对比通过', code, str(i) + '/' + str(len(rows)))
        log.i('页面接口对比通过')
        return 0
    except:

        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('余额表', r.status_code)

        return 1


if __name__ == "__main__":
    print('main')
    # config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        option = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': config.FILE_DOWNLOAD}

        option.add_experimental_option('prefs', prefs)
        option.add_argument('disable-infobars')
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(config.window_size_w, config.window_size_h)
        driver.implicitly_wait(5)
        ret = loginNew.run(driver)
        if (ret != 0):
            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:
            for i in range(20):
                run(driver)

            time.sleep(5)

            driver.quit()
