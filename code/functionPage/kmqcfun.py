import time

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains

from conf import config
from functionPage import login, toThird
from tools import log, commonSelenium


def runInit(driver):
    log.d('科目期初')
    try:
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/km/kmqc/kmqcfun"):
            return 1
        dels = driver.find_elements_by_xpath("//span[@class='remove-km']/..")

        while len(dels) > 0:
            # js=delSpans[i].get_attribute('onclick')
            # js1 = "document.documentElement.scrollTop=500"
            # driver.execute_script(document.documentElement.scrollTop=500)
            # driver.execute_script('arguments[0].scrollIntoView();', delSpans[0])
            scrollTop = dels[0].location['y'] - driver.find_element_by_class_name('t-body-div').location['y']
            driver.execute_script('document.getElementsByClassName("t-body-div")[0].scrollTop=' + str(scrollTop))
            # ActionChains.move_to_element()
            dels = driver.find_elements_by_xpath("//span[@class='remove-km']/..")

            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            x = dels[0].location['x']
            y = dels[0].location['y'] + dels[0].size['height'] / 2
            # ActionChains(driver).move_to_element(delSpans[0]).perform()
            commonSelenium.mouseMove(driver, x, y)
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            commonSelenium.mouseLeftClick(driver, x, y)
            times = 0
            maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
            while times < maxTimes:
                time.sleep(config.ACTION_WAIT_SLEEP_LONG)

                if driver.find_element_by_class_name('bootbox-body').text == '确认删除吗?':
                    btns = driver.find_elements_by_class_name('btn-primary')
                    for btn in btns:
                        if btn.text == 'OK':
                            btn.click()

                            log.i("科目期初- 删除科目", dels[0].text.replace('\n', '\t'))
                    break
                if times == maxTimes:
                    log.e("科目期初-删除科目等待确认超时")
                    return 1
                times = times + 1

            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
            dels = driver.find_elements_by_xpath("//span[@class='remove-km']/..")

        log.i("科目期初- 删除科目完成")
        return 0

    except:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('期末结转', r.status_code)

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
            runInit(driver)
            time.sleep(5)
        driver.quit()
