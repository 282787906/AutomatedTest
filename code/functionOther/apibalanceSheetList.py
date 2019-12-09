import json
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird, loginNew
from module import Kemuyueb
from module.Kemuyueb import dict2Kemuyueb
from tools import log, commonSelenium


def run(driver):
    log.d('资产负债表')
    dicts=dict
    try:
        params = {'origin': 'zidh',
                  'taxNo': config.caseTaxId,
                  'year': config.caseCurrentAccountYear,
                  'month': config.caseCurrentAccountMonth}

        response = requests.get(config.domain + '/api/report/balancesheet', params=params, allow_redirects=False)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            ret = json.loads(response.text)
            if str(ret['code']) == '200':
                dicts = ret['data']
            else:

                log.e('API 资产负债表获取失败：', response.text)
                return 1
        else:
            log.e('API 资产负债表获取失败HTTP：', response.status_code)
            return 1

        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            time.sleep(config.FAIL_WAIT_SLEEP)
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/cer/balanceSheet/balanceSheetList"):
            return 1

        driver.find_element_by_id('currentDate').click()
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)

        months = driver.find_elements_by_class_name('month')
        for month in months:
            if str(config.caseCurrentAccountMonth) + '月' in month.text:
                ActionChains(driver).move_to_element(month).click().perform()
                time.sleep(config.ACTION_WAIT_SLEEP_LONG)
                break


        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        rows = driver.find_elements_by_xpath("//table[@id='customerTable']/tbody/tr")
        for i in range(len(rows)):
            if i < 1:
                continue
            tdsSum = rows[i].find_elements_by_tag_name("td")
             
            if tdsSum[1].text!= '' and tdsSum[1].text!= '11':
                line=tdsSum[1].text
                qm=tdsSum[2].text.replace(',','')
                nc=tdsSum[3].text.replace(',','')
                
                if dicts['r'+line+'qm']!=qm or dicts['r'+line+'nc']!=nc:
                    log.e('比较失败——行次', line, '期末余额', qm, '年初余额', nc)
                    log.e( '期末余额', dicts['r'+line+'qm'], '年初余额', dicts['r'+line+'nc'])

                    return 1
                else:
                    log.d('行次',line,'期末余额', qm, '年初余额', nc )
            if tdsSum[5].text != '':
                line = tdsSum[5].text
                qm = tdsSum[6].text.replace(',', '')
                nc = tdsSum[7].text.replace(',', '')

                if dicts['r' + line + 'qm'] != qm or dicts['r' + line + 'nc'] != nc:
                    log.e('比较失败——行次', line, '期末余额', qm, '年初余额', nc)
                    log.e('期末余额', dicts['r' + line + 'qm'], '年初余额', dicts['r' + line + 'nc'])

                    return 1
                else:
                    log.d('行次', line, '期末余额', qm, '年初余额', nc)
        if dicts['r30qm'] != dicts['r53qm'] or dicts['r30nc'] != dicts['r53nc']:

            log.e('资产负债不平衡' )

            return 1
        log.i('资产负债表页面接口对比通过')
        return 0
    except:

        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('资产负债表', r.status_code)

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
        ret = loginNew.run(driver)
        if (ret != 0):
            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:

            run(driver)

            time.sleep(5)

            driver.quit()
