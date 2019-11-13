import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird
from tools import log, commonSelenium


def run(driver):
    log.d('期末结转')
    try:
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):

            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/jz/qmjz/initqmjz"):
            return 1
        driver.find_element_by_class_name('calculationthismonth').click()
    
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        driver.find_element_by_class_name('btn-primary').click()

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        try:
            alert = WebDriverWait(driver, 10, poll_frequency=0.5).until(
                lambda x: x.find_element_by_class_name('btn-primary'))

            alert.click()
            return 0
        except TimeoutException:
            log.w('TimeoutException')
            return 1
        except:
            log.exception('期末结转异常')
            return 1
        # driver.find_element_by_class_name('btn-primary').click()
        # driver.find_elements_by_xpath("//div[@class='bootbox-alert']/div/div/div[2]/button")
        #
        # textNew = driver.find_elements_by_xpath("//table[@id = 'bankStatementTable']/tbody/tr[1]/td[1]")
        # return 0
    except  :
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('期末结转',r.status_code )

        return 1
if __name__=="__main__":
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
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:

            for i in range (10):
                run(driver )
                driver.refresh()
                time.sleep(3)
            time.sleep(5)

            driver.quit()