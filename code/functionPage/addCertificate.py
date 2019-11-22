import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from conf import config
from conf.config import LOAD_PAGE_TIMEOUT, WHILE_WAIT_SLEEP, ACTION_WAIT_SLEEP_LONG
from functionPage import login, toThird, certificateList
from tools import log
from tools.commonSelenium import  toPage, mouseLeftDoubleClick, clearElement
from tools.excelTools import read_documentAdd


def run(driver):
    log.d('新增凭证') 
    ret, documents, msg = read_documentAdd()
    if ret != 0:
        log.e('加载凭证文件失败', msg)
        return 1
    if len(documents) == 0:
        log.w('加载凭证文件数量为0')
        return 1
    # if toThird.run(driver, documents[0][0].company_name, documents[0][0].tax_id):
    if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
        print('进账簿失败', ret)
        return 1
    if toPage(driver,config.domain + "/cs-third/cer/certificate/toAddCertificate"):
        return 1
    # alertDiv = driver.find_element_by_id('alertDiv')
    # startX = alertDiv.location['x'] + 100 + 135
    # startY = alertDiv.location['y'] + 150


    for document in documents:


        # mouseLeftDoubleClick(driver, startX, startY)
        # driver.find_element_by_class_name('zy-text').d
        # driver.find_elements_by_class_name('zy-text')[0].

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        ActionChains(driver).move_to_element(driver.find_elements_by_class_name('zy-text')[0]).double_click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        for index in range(len(document)):
            documentDetail = document[index]
            clearElement(driver.switch_to.active_element)
            driver.switch_to.active_element.send_keys(documentDetail.summary)
            driver.switch_to.active_element.send_keys(Keys.TAB)

            driver.switch_to.active_element.send_keys(documentDetail.account_code)

            elements=driver.find_elements_by_class_name('select2-results__option')
            if len(elements)==0:
                log.e('科目不存在',documentDetail.account_code)
                return 1
            for element in elements:
                if element.text.split(' ')[0]==documentDetail.account_code:
                    element.click()
            # driver.switch_to.active_element.send_keys(Keys.TAB)
            if documentDetail.partner_name != '\\N':  # 往来类型
                time.sleep(config.ACTION_WAIT_SLEEP_LONG)
                # driver.find_element_by_id('select2-wldw-container').click()
                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                ActionChains(driver).move_to_element(driver.find_element_by_id('select2-wldw-container')).click().perform()

                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                driver.find_element_by_class_name('select2-search__field').send_keys(documentDetail.partner_name)
                elements = driver.find_elements_by_class_name('select2-results__option')
                if len(elements) == 0 or (len(elements) == 1 and elements[0].text=='No results found'):
                    log.w('往来单位不存在', documentDetail.account_code,documentDetail.partner_name)

                    driver.find_element_by_id('add_wldw').click()

                    time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                    driver.find_element_by_id('partnerName').send_keys(documentDetail.partner_name)

                    time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                    driver.find_element_by_id('add_wldw_sub').click()
                    # return 1
                else:
                    for element in elements:
                        if element.text == documentDetail.partner_name:
                            element.click()

                driver.find_element_by_id('wldw_sub').click()


            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
            # driver.switch_to.active_element.send_keys(Keys.TAB)
            if documentDetail.debit_amount != '\\N':  # 钱在借方
                elements = driver.find_elements_by_class_name('jf-je-text')
                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                elements[index]. click()
                clearElement(driver.switch_to.active_element)
                driver.switch_to.active_element.send_keys(str(documentDetail.debit_amount))  # 如果钱在借方。 tab时直接换行
            else:
                elements = driver.find_elements_by_class_name('df-je-text')
                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                elements[index]. click()
                # clearElement(driver.switch_to.active_element)  # 清空借方默认金额
                # driver.switch_to.active_element.send_keys(Keys.TAB)
                clearElement(driver.switch_to.active_element)
                driver.switch_to.active_element.send_keys(str(documentDetail.credit_amount))
            if (index != len(document) - 1):
                driver.switch_to.active_element.send_keys(Keys.TAB)

        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        driver.find_element_by_id('btn_xzpz_add_and_save').send_keys(Keys.ENTER)
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        times = 0
        maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
        while (times < maxTimes):
            if ('零元整' == driver.find_element_by_id('hjjesx').text):
                break
            times = times + 1
            if times == maxTimes:
                log.e('新增凭证保存等待 超时')
                return 1
            time.sleep(WHILE_WAIT_SLEEP)

    log.i('新增凭证完成')
    return 0
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

            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:

            ret = run(driver)
            if (ret != 0):
                log.e('新增凭证失败', ret)
                time.sleep(config.FAIL_WAIT_SLEEP)
            time.sleep(5)
            driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.