import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird, loginNew
from tools import log, commonSelenium


def run(driver):
    log.d('结账')
    try:
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            time.sleep(config.FAIL_WAIT_SLEEP)
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/st/settle/toSettleAccounts"):
            return 1

        lastSettleMonth = driver.find_element_by_class_name('marked_words').text
        if lastSettleMonth != '上次结账: 无数据' and int(lastSettleMonth.split('-')[1]) >= config.caseCurrentAccountMonth:
            log.w(lastSettleMonth, "不需结账")
            return 0
        driver.find_element_by_id('checkBtn').click()

        times = 0
        maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
        while times < maxTimes:
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)

            if driver.find_element_by_id('checkBtn').text == '继续结账':
                driver.find_element_by_id('checkBtn').click()

                time.sleep(config.ACTION_WAIT_SLEEP_LONG)
                alert = driver.find_element_by_class_name('bootbox-body')

                if alert.text == '结账成功':
                    log.i("结账成功")
                    btns = driver.find_elements_by_class_name('btn-primary')
                    for btn in btns:
                        if btn.text == 'OK':
                            btn.click()
                    return 0
                else:

                    log.i("结账成功22222", alert.text)
            elif driver.find_element_by_id('checkBtn').text == '重新检查':

                log.e("马上检查未通过")
                lis = driver.find_elements_by_xpath("//div[@class='ckPannel']/div[3]/div/ul/li")
                for i in range(len(lis)):
                    li = driver.find_element_by_xpath("//div[@class='ckPannel']/div[3]/div/ul/li[" + str(i + 1) + "]/i")
                    if li.get_attribute('class') == 'describe_i error':
                        log.w(driver.find_element_by_xpath(
                            "//div[@class='ckPannel']/div[3]/div/ul/li[" + str(i + 1) + "]/span[1]").text,
                              driver.find_element_by_xpath(
                                  "//div[@class='ckPannel']/div[3]/div/ul/li[" + str(i + 1) + "]/span[2]").text)
                return 1
            if times == maxTimes:
                log.e("结账失败-马上检查超时")
                return 1
            times = times + 1

    except:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('结账', r.status_code)

        return 1


def runBack(driver):
    log.d('反结账')
    try:
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            time.sleep(config.FAIL_WAIT_SLEEP)
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/st/settle/toSettleAccounts"):
            return 1
        lastSettleDate = driver.find_element_by_class_name('marked_words').text

        if lastSettleDate == '上次结账: 无数据':
            log.i(lastSettleDate, '测试会计月:',config.caseCurrentAccountMonth)
            return 0
        lastSettleDate=lastSettleDate.replace('上次结账至:','')
        driver.find_element_by_id('dateTime').click()
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        # years = document[0].year - int(driver.find_elements_by_class_name('datepicker-switch')[1].text)
        #
        # if years < 0:
        #     for i in range(-1 * years):  # <<
        #         ActionChains(driver).move_to_element(driver.find_elements_by_class_name('prev')[1]).click().perform()
        #         time.sleep(ACTION_WAIT_SLEEP_SHORT)
        # if years > 0:
        #     for i in range(years):  # >>
        #         ActionChains(driver).move_to_element(driver.find_elements_by_class_name('next')[1]).click().perform()
        #         time.sleep(ACTION_WAIT_SLEEP_SHORT)

        lastSettleYear = int(lastSettleDate.split('-')[0])
        lastSettleMonth = int(lastSettleDate.split('-')[1])
        months = driver.find_elements_by_class_name('month')
        if config.caseCurrentAccountYear*100000+config.caseCurrentAccountMonth<=lastSettleYear*100000+ lastSettleMonth:

            for month in months:
                if str(lastSettleMonth) + '月' in month.text:
                    ActionChains(driver).move_to_element(month).click().perform()
                    times = 0
                    maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
                    while times < maxTimes:
                        time.sleep(config.ACTION_WAIT_SLEEP_LONG)

                        if driver.find_element_by_id('checkBtn').text == '反结账':
                            driver.find_element_by_id('checkBtn').click()

                            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
                            alert = driver.find_element_by_class_name('bootbox-body')

                            if alert.text == '反结账成功':
                                log.i("反结账成功", str(lastSettleDate), '月')
                                btns = driver.find_elements_by_class_name('btn-primary')
                                for btn in btns:
                                    if btn.text == 'OK':
                                        btn.click()
                                if runBack(driver)==0:
                                    return 0

                        else:
                            log.w(driver.find_element_by_id('checkBtn').text)
                        times = times + 1
                        if times == maxTimes:
                            log.e( '反结账月份选择后等待超时' )
                            return 1
        else:
            log.w(lastSettleDate, "反结账")
            return 0

        return 1


    except:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('反结账', r.status_code)

        return 1


if __name__ == "__main__":
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
        ret = loginNew.run(driver)
        if (ret != 0):
            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:

            # for i in range(10):
            # run(driver)
            runBack(driver)
            # drivr.refresh()
            # time.sleep(1)
            time.sleep(5)

            driver.quit()
