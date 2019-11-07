import random
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from conf import config
from functionPage import login
from tools import log, commonSelenium


def run(driver, company, tax):
    '''

    :param driver:
    :param company:
    :param tax:
    :return: 0 成功 1 失败
    '''
    log.d('进账簿', company)
    try:
        if commonSelenium.toPage(driver, config.domain + "/#/third/customer"):
            log.e("进账簿失败-进入客户列表超时：", driver.current_url)
            return 1
        if company==None and tax==None:
            companys=driver.find_elements_by_xpath("//ul[@class ='el-pager']/li")
            companys[random.randint(0,len(companys)-1)].click()
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            elements = driver.find_elements_by_name('btn_to_third')
            elements_name = driver.find_elements_by_name('span_companyName')[0].text
            log.i("进账簿-随机进账簿",elements_name)
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            elements[0].send_keys(Keys.ENTER)

        else:
            driver.find_element_by_id('input_company').send_keys(company)
            driver.find_element_by_id('btn_company_sreach').send_keys(Keys.ENTER)
            times = 0
            maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
            while times < maxTimes:
                elements = driver.find_elements_by_name('btn_to_third')
                elements_name = driver.find_elements_by_name('span_companyName')
                if len(elements) == 1 and len(elements_name) == 1 and elements_name[0].text == company:
                    break
                times = times + 1
                if times == maxTimes:
                    log.e("进账簿-账套查询超时：", len(elements))
                    return 1
                time.sleep(config.WHILE_WAIT_SLEEP)
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            elements[0].send_keys(Keys.ENTER)

        times = 0
        config.LOAD_PAGE_TIMEOUT = 10
        maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
        while (times < maxTimes):
            if 'cs-third' in driver.current_url:
                break
            times = times + 1
            # log.d('页面加载等待', maxTimes, times)
            if times == maxTimes:
                log.e("进账簿超时：", len(elements))
                return 1
            time.sleep(config.WHILE_WAIT_SLEEP)
        if company == None and tax == None:
            if elements_name == driver.find_element_by_class_name('company-name').text:
                return 0  #随机进账簿
        if company == driver.find_element_by_class_name('company-name').text and \
                tax == driver.get_cookie('tax_code')['value']:
            return 0
        else:

            log.e("进账簿失败：", '公司名税号匹配失败')
            return 1
    except:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception(r.status_code)
        return 1


if __name__ == "__main__":
    print('toThird')
    config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(config.window_size_w, config.window_size_h)
        driver.implicitly_wait(5)
        ret = login.run(driver, 'lxhw', '12344321')
        if (ret != 0):

            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:
            # ret = run(driver, '上海明创物流有限公司', '913101167989494335')
            ret = run(driver, None, None)
            if (ret != 0):
                time.sleep(config.FAIL_WAIT_SLEEP)
            time.sleep(5)

            driver.quit()
