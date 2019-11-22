import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from conf.config import ACTION_WAIT_SLEEP_LONG, LOAD_PAGE_TIMEOUT, WHILE_WAIT_SLEEP, ACTION_WAIT_SLEEP_SHORT
from functionOther import csInfoFileUpload
from functionPage import login

from tools import log, commonSelenium

def runDelete(driver):
    log.d('原始凭证-删除凭证')
    try:

        if commonSelenium.toPage(driver, config.domain + "/cs-third/cer/certificate/toCertificateInput"):
            log.w('加载凭证录入页面超时')
            return 1

        driver.find_element_by_id('uniformCreditCode').send_keys(config.caseTaxId)
        driver.find_element_by_id('currentDate').click()
        years = config.caseCurrentAccountYear - int(driver.find_elements_by_class_name('datepicker-switch')[1].text)

        if years < 0:
            for i in range(-1 * years):  # <<
                ActionChains(driver).move_to_element(driver.find_elements_by_class_name('prev')[1]).click().perform()
                time.sleep(ACTION_WAIT_SLEEP_SHORT)
        if years > 0:
            for i in range(years):  # >>
                ActionChains(driver).move_to_element(driver.find_elements_by_class_name('next')[1]).click().perform()
                time.sleep(ACTION_WAIT_SLEEP_SHORT)
        months = driver.find_elements_by_class_name('month')
        for month in months:
            if str(config.caseCurrentAccountMonth) in month.text:
                ActionChains(driver).move_to_element(month).click().perform()
                break
        isOpenOriginCertificate = 0
        for type in range(3):


            ActionChains(driver).move_to_element(
                driver.find_elements_by_class_name('iCheck-helper')[type ]).click().perform()

            driver.find_element_by_class_name("btn-success").send_keys(Keys.ENTER)
            count = int(driver.find_element_by_class_name('allcount').text.split('   ')[1][4:])

            if count==0:
                continue
            mainWindow = driver.current_window_handle  # 保存主页面句柄

            if isOpenOriginCertificate == 0:  # 打开原始凭证
                isOpenOriginCertificate = 1
                driver.find_element_by_id("originCertificate").send_keys(Keys.ENTER)
                driver.find_element_by_id("originCertificateConfirm").send_keys(Keys.ENTER)

                time.sleep(ACTION_WAIT_SLEEP_LONG)

            toHandle = driver.window_handles
            for handle in toHandle:
                if handle == mainWindow:
                    continue
                driver.switch_to.window(handle)

            for i in range(count):
                driver.find_element_by_class_name('delete').click()

                times = 0
                maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
                while times < maxTimes:
                    time.sleep(config.ACTION_WAIT_SLEEP_LONG)
                    btn = driver.switch_to.active_element
                    if btn.tag_name == 'button' and btn.text == 'OK':

                        btn.click()
                        break
                    if times == maxTimes:
                        log.e("原始凭证-删除凭证等待确认超时")
                        return 1
                    times = times + 1
                time.sleep(ACTION_WAIT_SLEEP_LONG)
            driver.close()
            isOpenOriginCertificate = 0
            driver.switch_to.window(mainWindow)
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)

        log.i('原始凭证-删除凭证结束')
        return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('原始凭证-删除凭证异常', r.status_code)
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
            ret = runDelete(driver)
            if (ret != 0):
                log.e('原始凭证-删除凭证失败', ret)
                time.sleep(config.FAIL_WAIT_SLEEP)

            time.sleep(5)
            driver.quit()
