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
    alert=None
    try:
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):

            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/jz/qmjz/initqmjz"):
            return 1
        driver.find_element_by_class_name('calculationthismonth').click()
    
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        driver.find_element_by_class_name('btn-primary').click()

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)

        # try:
        #     alert = WebDriverWait(driver, 10, poll_frequency=0.5).until(
        #         lambda x: x.find_element_by_class_name('btn-primary'))
        #
        #     alert.click()
        #     return 0
        # except TimeoutException:
        #     log.w('TimeoutException')
        #     return 1
        # except:
        #     log.exception('期末结转异常')
        #     return 1

        times = 0
        maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
        while times < maxTimes:
            btn = driver.switch_to.active_element
            if btn.tag_name == 'button' and btn.text == '确定':
                btn.click()
                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                break
            if times == maxTimes:
                log.e("期末结转等待确认超时")
                return 1
            times = times + 1
        log.i("期末结转完成")
        return 0
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

            for i in range (100):
                log.e('xunhuan',str(i))
                run(driver )
                driver.refresh()
                time.sleep(1)
            time.sleep(5)

            driver.quit()