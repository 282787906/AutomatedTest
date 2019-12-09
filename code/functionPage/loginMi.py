import time

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from conf import config
from conf.config import ACTION_WAIT_SLEEP_LONG, LOAD_PAGE_TIMEOUT, WHILE_WAIT_SLEEP
from tools.commonSelenium import toPage
from tools import log

def run(driver ):

    try:
        log.d(' 进入首页')
        if toPage(driver, 'https://www.mi.com/'):
            log.e(' 进入首页超时')
            return 1
        driver.find_element_by_xpath("//div[@id = 'J_siteUserInfo']/a[1]").click()

        driver.find_element_by_class_name('btn-primary').click()

        log.d(' 进入登录')

        driver.find_element_by_id('username').send_keys('282787906@qq.com')
        driver.find_element_by_id('pwd').send_keys('lqg346353848')

        driver.find_element_by_id('login-button').send_keys(Keys.ENTER)

        log.d(' 进入进入购物车')
        # driver.find_element_by_id('J_miniCartBtn').click()
        time.sleep(2)
        ActionChains(driver).move_to_element(driver.find_element_by_id('J_miniCartBtn')).perform()
        # if toPage(driver, 'https://static.mi.com/cart/'):
        #     log.e('进入购物车超时')
        #     return 1

        driver.refresh()
        cartListBody= driver.find_element_by_id('J_cartListBody').text
        log.i('购物车列表:',cartListBody)
        totalPrice = driver.find_element_by_id('J_cartTotalPrice').text


        log.i('总价:',totalPrice)
        return 1
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)

        log.exception('查询异常',r.status_code )
        return 1
if __name__=="__main__":
    print('main')

    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')

    # 不打开浏览器
    # option.add_argument('--headless')
    # option.add_argument('--disable-gpu')
    # 不加载图片
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # option.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=option)
    driver.set_window_size(config.window_size_w, config.window_size_h)
    driver.implicitly_wait(5)
    ret = run(driver)
    if (ret != 0):
        print('失败')
        time.sleep(config.FAIL_WAIT_SLEEP)
    driver.quit()