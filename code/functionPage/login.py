import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from conf import config
from conf.config import ACTION_WAIT_SLEEP_LONG, LOAD_PAGE_TIMEOUT, WHILE_WAIT_SLEEP
from tools.commonSelenium import toPage
from tools import log

def run(driver ):
    log.d('CRM登录',config.domain + "/#/login")
    try:
        if toPage(driver, config.domain + "/#/login"):
            log.e('CRM登录失败-进入CRM登录页超时')
            return 1
        driver.find_element_by_name('username').send_keys(config.userName)
        driver.find_element_by_name('password').send_keys(config.userPwd)
        time.sleep(ACTION_WAIT_SLEEP_LONG)
        driver.find_element_by_name('btn_login').send_keys(Keys.ENTER)

        times = 0
        maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
        while times < maxTimes:
            if driver.current_url == config.domain + "/#/dashboard":
                time.sleep(ACTION_WAIT_SLEEP_LONG)
                log.i('CRM登录成功')
                return 0
            times = times + 1
            time.sleep(WHILE_WAIT_SLEEP)
        log.e('CRM登录失败-登录超时')
        return 1
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)

        log.exception('CRM登录异常',r.status_code )
        return 1
if __name__=="__main__":
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
        ret = run(driver)
        if (ret != 0):

            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
        driver.quit()
