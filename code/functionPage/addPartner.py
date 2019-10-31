import time

from pip._vendor import requests
from selenium import webdriver

from conf import config
from functionPage import login, toThird
from tools import log, commonSelenium


def run(driver, partnerName):
    log.d('新增往来单位')
    try:
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
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.e('新增往来单位异常',r.status_code,e)

        return 1
if __name__=="__main__":
    print('main')
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
        if  toThird.run(driver, '上海明创物流有限公司', '913101167989494335'):
            print('进账簿失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
        else:
            if run(driver, '上海明创物流有限公司1' ):

                time.sleep(config.FAIL_WAIT_SLEEP)
        time.sleep(5)

        driver.quit()