import json
import os
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird, loginNew
from module import Kemuyueb
from module.Kemuyueb import dict2Kemuyueb
from module.SubsidiaryLedger import SubsidiaryLedger
from tools import log, commonSelenium


def run(driver):
    log.d('明细账')
    kemuyueb_dicts = {}
    try:
        # params = {'origin': 'zidh',
        #           'taxNo': config.caseTaxId,
        #           'year': config.caseCurrentAccountYear,
        #           'startMonth': config.caseCurrentAccountMonth,
        #           'endMonth': config.caseCurrentAccountMonth}
        #
        # response = requests.get(config.domain + '/api/report/balance', params=params, allow_redirects=False)
        # response.encoding = 'utf-8'
        # if response.status_code == 200:
        #     ret = json.loads(response.text)
        #     if str(ret['code']) == '200':
        #         dicts = ret['data']
        #         for dict in dicts:
        #             km = dict2Kemuyueb(dict)
        #             kemuyueb_dicts[km.accountCode] = km
        #     else:
        #
        #         log.e('API 明细账获取失败：', response.text)
        #         return 1
        # else:
        #     log.e('API 明细账获取失败HTTP：', response.status_code)
        #     return 1

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
        driver.find_element_by_id('doFind').click()

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        rows = driver.find_elements_by_xpath("//table[@id='customerTable']/tbody/tr")
        for i in range(len(rows)):

            tdsSum = rows[i].find_elements_by_tag_name("td")
            kmCode=driver.find_element_by_id('select2-km-container').text.split('_')[0]
            kmName=driver.find_element_by_id('select2-km-container').text.split('_')[1]
            date =   tdsSum[0].text
            voucherNo = tdsSum[1].text
            summary =   tdsSum[2].text
            debitAmount = '0.00' if (tdsSum[3].text == '') else tdsSum[3].text

            creditAmount = '0.00' if (tdsSum[4].text == '') else tdsSum[4].text
            direction =   tdsSum[5].text

            qmYue = '0.00' if (tdsSum[6].text == '') else tdsSum[6].text
            sl=SubsidiaryLedger(kmCode, kmName, date, voucherNo, summary, debitAmount, creditAmount, direction, qmYue)
            log.i(kmCode,kmName,date, voucherNo, summary, debitAmount, creditAmount, direction, qmYue)

        driver.find_element_by_id('downloadBtnAll').click()

        log.i('页面接口对比通过')
        return 0
    except:

        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('明细账', r.status_code)

        return 1


if __name__ == "__main__":
    print('main')
    config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        option = webdriver.ChromeOptions()
        dir = os.path.dirname(__file__)
        parent_path = os.path.dirname(dir)
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
