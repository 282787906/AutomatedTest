import json
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird
from module import Kemuyueb
from module.Kemuyueb import dict2Kemuyueb
from tools import log, commonSelenium


def run(driver):
    log.d('余额表')
    kemuyueb_dicts = {}
    try:
        params = {'origin': 'zidh',
                  'taxNo': config.caseTaxId,
                  'year': config.caseCurrentAccountYear,
                  'startMonth': config.caseCurrentAccountMonth,
                  'endMonth': config.caseCurrentAccountMonth}

        response = requests.get(config.domain + '/api/report/balance', params=params, allow_redirects=False)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            ret = json.loads(response.text)
            if str(ret['code']) == '200':
                dicts = ret['data']
                for dict in dicts:
                    km = dict2Kemuyueb(dict)
                    kemuyueb_dicts[km.accountCode] = km
            else:

                log.e('API 余额表获取失败：', response.status_code)
                return 1
        else:
            log.e('API 余额表获取失败HTTP：', response.status_code)
            return 1

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
        driver.find_element_by_id('doFind').click()

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        rows = driver.find_elements_by_xpath("//table[@id='customerTable']/tbody/tr")
        for i in range(len(rows)):
            if i < 2:
                continue
            tdsSum = rows[i].find_elements_by_tag_name("td")
            code = tdsSum[0].text
            name = tdsSum[1].text

            qcDebit = '0.00' if (tdsSum[2].text == '') else tdsSum[2].text
            qcCrebit = '0.00' if (tdsSum[3].text == '') else tdsSum[3].text

            bqDebit = '0.00' if (tdsSum[4].text == '') else tdsSum[4].text
            bqCrebit = '0.00' if (tdsSum[5].text == '') else tdsSum[5].text

            qmDebit = '0.00' if (tdsSum[6].text == '') else tdsSum[6].text
            qmCrebit = '0.00' if (tdsSum[7].text == '') else tdsSum[7].text
            if i == len(rows) - 1:
                if qcDebit != qcCrebit or bqDebit != bqCrebit or qmDebit != qmCrebit:
                    log.e('页面合计不平衡', qcDebit, qcCrebit, bqDebit, bqCrebit, qmDebit, qmCrebit)
                    return 1
                else:
                    log.i('页面合计', qcDebit, qcCrebit, bqDebit, bqCrebit, qmDebit, qmCrebit)
                break
            if kemuyueb_dicts.get(code).beginningBalanceDebit != str(qcDebit).replace(',', '') or kemuyueb_dicts.get(
                    code).beginningBalanceCrebit != str(qcCrebit).replace(',', '') or kemuyueb_dicts.get(
                code).currentAmountDebit != str(bqDebit).replace(',', '') or kemuyueb_dicts.get(
                code).currentAmountCrebit != str(bqCrebit).replace(',', '') or kemuyueb_dicts.get(
                code).endingBalanceDebit != str(qmDebit).replace(',', '') or kemuyueb_dicts.get(
                code).endingBalanceCrebit != str(qmCrebit).replace(',', ''):
                log.e('页面接口对比失败', code, '\n', '页面结果：', name, qcDebit, qcCrebit, bqDebit, bqCrebit, qmDebit, qmCrebit,
                      '\n', '接口结果:',
                      kemuyueb_dicts.get(code).beginningBalanceDebit,
                      kemuyueb_dicts.get(code).beginningBalanceCrebit,
                      kemuyueb_dicts.get(code).currentAmountDebit,
                      kemuyueb_dicts.get(code).currentAmountCrebit,
                      kemuyueb_dicts.get(code).endingBalanceDebit,
                      kemuyueb_dicts.get(code).endingBalanceCrebit
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
    config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(config.window_size_w, config.window_size_h)
        driver.implicitly_wait(5)
        ret = login.run(driver)
        if (ret != 0):
            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:

            run(driver)

            time.sleep(5)

            driver.quit()
