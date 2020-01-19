import random
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird
from tools import log, commonSelenium


def run(driver, companyName, taxId, type):
    '''

    :param driver:
    :param type: 审核 1  取消审核  2 全部删除 3
    :return: 成功 0 失败 1

    '''
    log.d('凭证列表-批量处理', type)
    if toThird.run(driver, companyName, taxId):
        print('进账簿失败', ret)
        return 1
    try:
        if commonSelenium.toPage(driver, config.domain + "/cs-third/cer/certificate/certificateList"):
            return 1

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        if driver.find_element_by_id('span_pz_count') == '0':
            log.i('没有凭证')
            return 0

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        driver.find_element_by_class_name('getAll').click()

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        iCheck = driver.find_element_by_class_name('checkAll')

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        documents = driver.find_elements_by_xpath("//div[@class='pz-list']/table")
        documentsCountOnPage = int(
            driver.find_element_by_class_name('total-pz').text.replace('共计', '').replace('张凭证', ''))
        if (len(documents) != documentsCountOnPage + 1):
            log.i('全部加载失败', len(documents), documentsCountOnPage + 1)
            return 1
        if documentsCountOnPage==0:
            log.i('凭证列表-没有凭证需要批量处理' )
            return 0
        iCheck.send_keys(Keys.SPACE)
        if not iCheck.is_selected():
            iCheck.send_keys(Keys.SPACE)
        daishenhe = 0
        yishenhe = 0
        for i in range(documentsCountOnPage):

            if driver.find_element_by_xpath(
                    "//div[@class='pz-list']/table[" + str(i + 2) + "]/tbody/tr[1]/td[1]/div/input").is_selected():
                if driver.find_element_by_xpath(
                        "//div[@class='pz-list']/table[" + str(i + 2) + "]/tbody/tr[1]/td[2]/span").text == '待审核':
                    daishenhe = daishenhe + 1
                else:
                    yishenhe = yishenhe + 1
            else:
                log.e('凭证列表-全选未选中')
                return 1
        if type == 1:
            if daishenhe == 0:  # 批量审核  待审核为0
                log.i('批量审核  待审核为0')
                return 0
            else:
                log.d('批量审核  待审核:', daishenhe)
        elif type == 2:  # 批量取消审核  已审核为0
            if yishenhe == 0:
                log.i('批量取消审核  已审核为0')
                return 0
            else:
                log.d('批量取消审核  已审核：', daishenhe)


        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        if type == 1:
            element = driver.find_element_by_class_name('uploadMul')
            element.click()
            if waitNotice(driver, element):
                log.i('凭证列表-批量审核成功')
            # else:
            #     log.e('凭证列表-批量审核等待超时')
            return 0
        elif type == 2:
            element = driver.find_element_by_id('qxsh')
            element.click()
            if waitNotice(driver, element):
                log.i('凭证列表-批量取消审核成功')
            # else:
            #     log.e('凭证列表-批量取消审核等待超时')
            return 0
        elif type == 3:
            element = driver.find_element_by_class_name('deleteMul')
            element.click()

            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
            btnPrimarys = driver.find_elements_by_class_name('btn-primary')

            for btn in btnPrimarys:
                if btn.text == 'OK':
                    btn.click()
            if waitNotice(driver, element):
                log.i('凭证列表-批量删除成功')
            # else:
            #     log.e('凭证列表-批量删除等待超时')
            return 0

        return 1
    except:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('凭证列表-批量处理异常', type, r.status_code)

        return 1


def waitNotice(driver, element):
    for i in range(10):
        try:
            element.tag_name
            alert = WebDriverWait(driver, 1, poll_frequency=0.2).until(
                lambda x: x.find_element_by_id("gritter-notice-wrapper"))
            log.w(alert.text)
            return 0
        except StaleElementReferenceException:
            # log.w('StaleElementReferenceException')
            return 1

        except TimeoutException:
            continue
        except:
            log.exception('凭证列表-批量处理等待异常')
            return 0
        time.sleep(0.1)
    log.w('凭证列表-批量处理等待超时')
    return 0


if __name__ == "__main__":
    print('main')

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
            if toThird.run(driver, '回归测试2', 'taxidCode000000002'):
                print('进账簿失败')
                time.sleep(config.FAIL_WAIT_SLEEP)
            else:
                # for i in range(10):
                #     run(driver, random.randint(1, 2))
                #     time.sleep(3)
                run(driver, '回归测试2', 'taxidCode000000002', 1)
            time.sleep(5)

            driver.quit()
