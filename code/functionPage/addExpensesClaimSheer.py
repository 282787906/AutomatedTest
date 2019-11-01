import time

from pip._vendor import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from conf import config
from functionPage import login, toThird
from tools import log, commonSelenium


def run(driver):
    log.d('费用报销单')

    try:
        if commonSelenium.toPage(driver, config.domain + "/cs-third//third/expensesClaimSheer/list"):
            log.e('加载费用报销单页面超时')
            return 1

        for index in range (1) :

            inputs = driver.find_elements_by_class_name('summary')
            inputs[0].send_keys('123123123')
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys("123123")
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys('1')


            textOld=driver.find_elements_by_xpath("//table[@id = 'bankStatementTable']/tbody/tr[1]/td[1]")
            driver.find_element_by_id('save_btn').click()
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
            driver.refresh()
            textNew=driver.find_elements_by_xpath("//table[@id = 'bankStatementTable']/tbody/tr[1]/td[1]")
            if textNew!=textOld:
                log.d('费用报销单成功')


        log.d('费用报销单结束')
        return 0
    except  :
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('新增费用报销单异常', r.status_code )

        return 1


if __name__ == "__main__":
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
        if toThird.run(driver, '上海明创物流有限公司', '913101167989494335'):
            print('进账簿失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
        else:
            if run(driver):
                time.sleep(config.FAIL_WAIT_SLEEP)
        time.sleep(5)

        driver.quit()
