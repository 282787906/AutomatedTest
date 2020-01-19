import json
import os
import shutil
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird, loginNew
from module.SubsidiaryLedger import SubsidiaryLedger, dict2SubsidiaryLedger
from tools import log, commonSelenium, excelTools


def subsidiaryLedgerListFromApi():
    params = {'origin': 'zidh',
              'taxNo': config.caseTaxId,
              'year': config.caseCurrentAccountYear,
              'month': config.caseCurrentAccountMonth}

    log.i('API 明细帐获取', config.domain_api)
    response = requests.get(config.domain_api + '/api/report/subsidiaryLedger', params=params, allow_redirects=False)
    response.encoding = 'utf-8'
    lastKmCode = ''
    listsApi = dict()
    subsidiaryLedgers = []
    if response.status_code == 200:
        ret = json.loads(response.text)
        if str(ret['code']) == '200':
            dicts = ret['data']
            for index in range(len(dicts)):
                sl = dict2SubsidiaryLedger(dicts[index])

                if (lastKmCode == ''):
                    lastKmCode = dicts[index]['accountCode']
                    # log.d('第一次' )
                if (lastKmCode == dicts[index]['accountCode']):
                    subsidiaryLedgers.append(sl)
                else:
                    for k in range(len(subsidiaryLedgers)):

                        if subsidiaryLedgers[k].summary == '本年累计' and subsidiaryLedgers[k].direction == '平':
                            continue
                    listsApi[lastKmCode] = subsidiaryLedgers
                    subsidiaryLedgers = []
                    subsidiaryLedgers.append(sl)
                if (index == len(dicts) - 1):
                    for k in range(len(subsidiaryLedgers)):

                        if subsidiaryLedgers[k].summary == '本年累计' and subsidiaryLedgers[k].direction == '平':
                            continue
                    listsApi[dicts[index]['accountCode']] = subsidiaryLedgers
                    # log.d('最后一次', len(lists))
                    subsidiaryLedgers = []
                lastKmCode = dicts[index]['accountCode']
            return 0,listsApi
        else:

            log.e('API 明细账获取失败：', response.text)
            return 1
    else:
        log.e('API 明细账获取失败HTTP：', response.status_code)
        return 1


def run(driver):
    log.d('明细账')
    try:

        retCode, listsApi =  subsidiaryLedgerListFromApi()
        if retCode != 0:
            time.sleep(config.FAIL_WAIT_SLEEP)
            return 1
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            time.sleep(config.FAIL_WAIT_SLEEP)
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/cer/subsidiaryLedger/subsidiaryLedgerList"):
            return 1

        driver.find_element_by_id('startMonth').find_elements_by_tag_name("option")[
            config.caseCurrentAccountMonth - 1].click()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        driver.find_element_by_id('endMonth').find_elements_by_tag_name("option")[
            config.caseCurrentAccountMonth - 1].click()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        shutil.rmtree(config.FILE_DOWNLOAD)
        os.mkdir(config.FILE_DOWNLOAD)
        driver.find_element_by_id('downloadBtnAll').click()
        times = 0
        maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
        while times < maxTimes:
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
            if '数据导出并下载成功' in driver.find_element_by_class_name('bootbox-body').text:
                driver.find_element_by_class_name('btn-primary').click()
                break
            if times == maxTimes:
                log.e("明细账-明细账批量下载超时")
                return 1
            times = times + 1

        retCode, listsDownload = excelTools.read_subsidiaryLedgerList()
        if retCode != 0:
            time.sleep(config.FAIL_WAIT_SLEEP)
            log.e('明细账批量下载失败：' )
            return 1
        if len(listsDownload)!=len(listsApi):
            log.e('API明细账数量与批量下载数量不一致 listsDownload:',str(len(listsDownload)),'listsApi:',str(len(listsApi)))

            return 1
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        for subsidiaryLedger in listsDownload:
            if len(subsidiaryLedger) > 4:
                continue
            driver.find_element_by_id('select2-km-container').click()
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            driver.find_element_by_class_name('select2-search__field') .send_keys(subsidiaryLedger)
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            while 1:
                if driver.find_element_by_class_name('select2-results__option--highlighted').text.split(' ')[0]==subsidiaryLedger:
                    driver.find_element_by_class_name('select2-search__field').send_keys(Keys.ENTER)
                    break
                else:

                    driver.find_element_by_class_name('select2-search__field').send_keys(Keys.DOWN)
                    time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            driver.find_element_by_id('doFind').click()
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
            rows = driver.find_elements_by_xpath("//table[@id='customerTable']/tbody/tr")
            accountCode = driver.find_element_by_id('select2-km-container').text.split(' ')[0]
            accountName = driver.find_element_by_id('select2-km-container').text.split(' ')[1]
            for i in range(len(rows)):
                tdsSum = rows[i].find_elements_by_tag_name("td")

                date = tdsSum[0].text
                voucherNo = tdsSum[1].text
                summary = tdsSum[2].text
                debitAmount = '0.00' if (tdsSum[3].text == '') else tdsSum[3].text.replace(',','')

                creditAmount = '0.00' if (tdsSum[4].text == '') else tdsSum[4].text.replace(',','')
                direction = tdsSum[5].text

                qmYue = '0.00' if (tdsSum[6].text == '') else tdsSum[6].text.replace(',','')
                # sl=SubsidiaryLedger(kmCode, kmName, date, voucherNo, summary, debitAmount, creditAmount, direction, qmYue)
                # log.d('页面\t', accountCode, accountName, date, voucherNo, summary, debitAmount, creditAmount, direction, qmYue)
                api = listsApi[accountCode][i]

                # log.d('API\t', api.accountCode, api.accountName, api.date, api.voucherNo,
                #       api.summary, api.debitAmount, api.creditAmount, api.direction, api.qmYue)

                excel = listsDownload[accountCode][i]

                # log.d('excel\t', excel.accountCode, excel.accountName, excel.date, excel.voucherNo,
                #       excel.summary, excel.debitAmount, excel.creditAmount, excel.direction, excel.qmYue)

                if not(date == excel.date == api.date )or not( direction == excel.direction == api.direction) or not( summary == excel.summary == api.summary):
                    log.e('明细账对比失败')
                    return 1
                elif not(voucherNo == excel.voucherNo == api.voucherNo):
                    log.e('明细账对比失败 voucherNo')
                    return 1
                elif not(float(debitAmount) == excel.debitAmount == api.debitAmount):
                    log.e('明细账对比失败 debitAmount')
                    return 1
                elif not(float(creditAmount) == excel.creditAmount == api.creditAmount):
                    log.e('明细账对比失败 creditAmount')
                    return 1
                elif not(float(qmYue) == excel.qmYue== api.qmYue):
                    log.e('明细账对比失败 qmYue')
                    return 1
            log.i('页面接口对比通过',subsidiaryLedger)
        log.i('页面接口对比通过')
        return 0
    except:

        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('明细账', r.status_code)

        return 1


if __name__ == "__main__":
    print('main')

    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        option = webdriver.ChromeOptions()
        # dir = os.path.dirname(__file__)
        # parent_path = os.path.dirname(dir)
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

            run(driver)
            time.sleep(5)

            driver.quit()
