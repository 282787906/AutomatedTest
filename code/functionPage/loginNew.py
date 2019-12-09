import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from conf import config
from conf.config import ACTION_WAIT_SLEEP_LONG, LOAD_PAGE_TIMEOUT, WHILE_WAIT_SLEEP
from tools.commonSelenium import toPage
from tools import log

def run(driver ):
    log.d('第三方跳转登录', config.caseCompanyName+","+config.caseTaxId+","+config.userName)
    sso=''
    try:
        params = {"params": config.caseCompanyName+","+config.caseTaxId+","+config.userName }

        response = requests.get(config.domain + "/cs-third/ignore/en", params=params, allow_redirects=False)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            ret = json.loads(json.loads(response.text))
            if str(ret['result']) == '1':
                sso=ret['data']
                log.i('加密成功 sso：', sso)
            else:

                log.e('加密失败：', ret['message'])

        else:
            log.e('加密请求失败：', response.status_code)

        if len(sso)>0:
            driver.get(config.domain + "/cs-third/ignore/simulatedLogin?sso="+sso)
        else:
            driver.get(config.domain + "/cs-third/ignore/test?taxNo="+config.caseTaxId+"&userName="+config.userName+"&rb=jdtj")

        times = 0
        maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
        while times < maxTimes:
            if 'cs-third/cer/certificate/jdtj' in driver.current_url:
                header = driver.find_element_by_xpath("//div[@class = 'container-fluid']/div[1]/div")
                if header.get_attribute("class") == 'third-nav' and config.caseTaxId == driver.get_cookie('tax_code')[
                    'value'] and config.caseCompanyName == driver.find_element_by_class_name('company-name').text:
                    time.sleep(3)
                    log.i('第三方跳转登录-登录成功')
                    return 0

            times = times + 1

            log.d('第三方跳转登录-登录等待',driver.current_url)
            time.sleep(WHILE_WAIT_SLEEP)
        log.e('第三方跳转登录失败-登录超时')
        return 1
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)

        log.exception('第三方跳转登录异常',r.status_code )
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
        driver.implicitly_wait(10)
        ret = run(driver)
        if (ret != 0):

            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
        driver.quit()
