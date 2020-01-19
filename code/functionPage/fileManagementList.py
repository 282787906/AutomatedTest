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
    log.d('信息采集')
    dicts=dict
    try:

        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            time.sleep(config.FAIL_WAIT_SLEEP)
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/fil/fileManagement/fileManagementList"):
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

        log.i('信息采集页面接口对比通过')
        return 0
    except:

        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('信息采集', r.status_code)

        return 1


if __name__ == "__main__":
    print('main')
    # config.set_host(config.HOST_SOURCE_PRE)
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
