import time

import requests
from selenium import webdriver

from conf import config
from functionPage import login, toThird
from tools import log, commonSelenium


def runAdd(driver, partnerName):
    log.d('新增往来单位')
    try:
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/con/contactsunit/contactsunitlist"):
            return 1

        # driver.find_element_by_id('company').click()
        # driver.find_element_by_id('people').click()
        driver.find_element_by_id('add').click()

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        driver.find_element_by_id('partnerName').send_keys(partnerName)
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        driver.find_element_by_id('contactFormBtn').click()

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        count = 0
        while (count < config.LOAD_PAGE_TIMEOUT):
            names = driver.find_elements_by_class_name('kh-text')
            deletes = driver.find_elements_by_id('deleteContact')
            for index in range(len(names)):
                if names[index].text == partnerName:
                    log.i('新增往来单位成功')
                    return 0
            elementsError = driver.find_elements_by_class_name('error')
            if len(elementsError) == 2 and elementsError[1].text != '':
                log.e('新增往来单位失败', elementsError[1].text)
                break
            count = count + 1
            time.sleep(config.WHILE_WAIT_SLEEP)

        log.e('新增往来单位失败, 添加后未找到')
        return 1
    except:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('新增往来单位异常', r.status_code)

        return 1


def runClear(driver):
    log.d('清空往来单位')
    try:
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/con/contactsunit/contactsunitlist"):
            return 1
        while 1:
            dels = driver.find_elements_by_id('deleteContact')
            if len(dels) == 0:
                if 'active-kh' in driver.find_element_by_id('company').get_attribute('class'):
                    driver.find_element_by_id('people').click()
                    continue
                else:
                    break
            dels[0].click()
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
            times = 0
            maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
            while times < maxTimes:

                if driver.find_element_by_class_name('bootbox-body').text == '确认删除?':
                    btns = driver.find_elements_by_class_name('btn-primary')
                    for btn in btns:
                        if btn.text == 'OK':
                            btn.click()

                            log.i("往来单位- 删除", driver.find_element_by_class_name('kh-text').text)
                    break
                if times == maxTimes:
                    log.e("往来单位-删除等待确认超时")
                    return 1
                times = times + 1
                time.sleep(config.WHILE_WAIT_SLEEP)
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)

        log.i("往来单位-删除完成")
        return 0
    except:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('往来单位-删除异常', r.status_code)

        return 1


if __name__ == "__main__":
    print('main')
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
        # if runAdd(driver, '上海明创物流有限公司1'):
        #     time.sleep(config.FAIL_WAIT_SLEEP)
        if runClear(driver):
            time.sleep(config.FAIL_WAIT_SLEEP)

        driver.quit()
