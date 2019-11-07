import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from conf.config import ACTION_WAIT_SLEEP_LONG, LOAD_PAGE_TIMEOUT, WHILE_WAIT_SLEEP, ACTION_WAIT_SLEEP_SHORT
from functionOther import csInfoFileUpload
from functionPage import login

from tools import log, commonSelenium
from tools.commonBusiness import getFeatureCdByCode
from tools.commonSelenium import clearElement
from tools.excelTools import read_documentInput
from tools.mySqlHelper import getTemplateSubjectById


def run(driver):

    log.d('录入凭证')
    try:
        ret, documents, msg = read_documentInput( )
        if ret != 0:
            log.e('加载凭证文件失败', msg)
            return 1
        if len(documents) == 0:
            log.w('加载凭证文件数量为0')
            return 1
        spCount = 0
        cpCount = 0
        nblzCount = 0
        for document in documents:
            if document[0].type == 1:
                spCount = spCount + 1
            if document[0].type == 2:
                cpCount = cpCount + 1
            if document[0].type == 3:
                nblzCount = nblzCount + 1

        document = documents[0]
        if commonSelenium.toPage(driver, config.domain + "/cs-third/cer/certificate/toCertificateInput"):

            log.w('加载凭证录入页面超时')
            return 1

        driver.find_element_by_id('uniformCreditCode').send_keys(document[0].tax_no)
        driver.find_element_by_id('currentDate').click()
        years = document[0].year - int(driver.find_elements_by_class_name('datepicker-switch')[1].text)

        if years < 0:
            for i in range(-1 * years):  # <<
                ActionChains(driver).move_to_element(driver.find_elements_by_class_name('prev')[1]).click().perform()
                time.sleep(ACTION_WAIT_SLEEP_SHORT)
        if years > 0:
            for i in range(years):  # >>
                ActionChains(driver).move_to_element(driver.find_elements_by_class_name('next')[1]).click().perform()
                time.sleep(ACTION_WAIT_SLEEP_SHORT)
        months = driver.find_elements_by_class_name('month')
        for month in months:
            if str(document[0].month) in month.text:
                ActionChains(driver).move_to_element(month).click().perform()
                break
        isOpenOriginCertificate = 0
        for documentIndex in range(len(documents)):

            document = documents[documentIndex]
            ActionChains(driver).move_to_element(
                driver.find_elements_by_class_name('iCheck-helper')[document[0].type - 1]).click().perform()

            driver.find_element_by_class_name("btn-success").send_keys(Keys.ENTER)
            # print('原始凭证',driver.find_element_by_class_name('allcount').text.split('   ')[1] )

            if isOpenOriginCertificate == 0:  # 打开原始凭证
                isOpenOriginCertificate = 1
                driver.find_element_by_id("originCertificate").send_keys(Keys.ENTER)
                driver.find_element_by_id("originCertificateConfirm").send_keys(Keys.ENTER)
                handles = driver.window_handles
                time.sleep(ACTION_WAIT_SLEEP_LONG)

                driver.switch_to.window(handles[0]);  # switch back to main screen

                time.sleep(ACTION_WAIT_SLEEP_LONG)
            count = int(driver.find_element_by_class_name('allcount').text.split('   ')[1][4:])

            if document[0].type == 1 and count < spCount:
                log.e('原始凭证收票数量不足', count, spCount)
                if csInfoFileUpload.run( document[0].tax_no, document[0].type,spCount-count): #文件上传失败
                    return 1
            if document[0].type == 2 and count < cpCount:
                log.e('原始凭证出票数量不足', count, cpCount)
                if csInfoFileUpload.run(document[0].tax_no, document[0].type,cpCount-count): #文件上传失败
                    return 1
            if document[0].type == 3 and count < nblzCount:
                log.e('原始凭证内部流转数量不足', count, nblzCount)
                if csInfoFileUpload.run(document[0].tax_no, document[0].type,nblzCount-count): #文件上传失败
                    return 1
            divBtn = driver.find_element_by_id('divBtn')
            ActionChains(driver).move_to_element(divBtn).perform()
            time.sleep(ACTION_WAIT_SLEEP_LONG)

            smallClasses = driver.find_elements_by_xpath("//ul[@class = 'dropspan-ul']/li")
            for i in range(len(smallClasses)):
                ActionChains(driver).move_to_element(smallClasses[i]).perform()
                templates = driver.find_elements_by_xpath("//ul[@class = 'dropspan-ul']/li[" + str(i + 1) + "]/ul/li")
                isbreak = 0
                for j in range(len(templates)):
                    if templates[j].text == document[0].TEMPLATED_NAME:
                        ActionChains(driver).move_to_element(templates[j]).click().perform()
                        isbreak = 1
                        break
                if isbreak == 1:
                    break
                if i == len(smallClasses) - 1:
                    print('模板未找到', document[0].TEMPLATED_NAME)
                    return 1, '模板未找到', document[0].TEMPLATED_NAME
                time.sleep(ACTION_WAIT_SLEEP_SHORT)
            time.sleep(ACTION_WAIT_SLEEP_LONG)

            ret_getFile, dataTemplates, msg = getTemplateSubjectById(document[0].TEMPLATED_ID)
            if ret_getFile != 0 or len(dataTemplates) == 0:
                log.e('加载模板失败', msg)
                return 1
            # ActionChains(driver).move_to_element(
            #     driver.find_element_by_class_name('sz-zkm')).click().perform()
            # time.sleep(ACTION_WAIT_SLEEP_LONG)

            sj = 1
            hasBank = 0
            for detail in document:
                for template in dataTemplates:
                    isSum = 0
                    if template.kmCode in detail.account_code:
                        if (template.subjectType == 1 or template.subjectType == 2) and template.jdType == 0:
                            isSum = 1
                        if template.subjectType == 3 and template.jdType == 1:
                            isSum = 1
                        if (template.subjectType == 4 or template.subjectType == 5) and sj == 1:
                            isSum = 1
                            sj == 0
                        id = 'ts' + str(template.tsId)
                        if isSum == 0:
                            elementInput = driver.find_element_by_id(id)
                            # if elementInput.text!='':
                            clearElement(elementInput)
                            if template.jdType == 0:
                                elementInput.send_keys(str(detail.credit_amount))
                            else:
                                elementInput.send_keys(str(detail.debit_amount))
                        # else:
                        if getFeatureCdByCode(template.kmCode) == 2:  # 银行
                            # sz_zkm=driver.find_element(By.CLASS_NAME,'sz-zkm')
                            sz_zkm = driver.find_element_by_class_name('sz-zkm')
                            print('location', driver.find_element_by_class_name('sz-zkm').location['x'],
                                  driver.find_element_by_class_name('sz-zkm').location['y'])
                            # mouseRightClick(driver,driver.find_element_by_class_name('sz-zkm').location['x'],
                            #       driver.find_element_by_class_name('sz-zkm').location['y'])
                            # driver.execute_script(
                            #     "arguments[0].setAttribute('style', arguments[1]);",
                            #     driver.find_element_by_class_name('sz-zkm'),
                            #     "border: 1px solid red;"  # 边框border:2px; red红色
                            # )
                            # ActionChains(driver).move_to_element(
                            #     driver.find_element_by_class_name('sz-zkm')).context_click().perform()
                            time.sleep(ACTION_WAIT_SLEEP_LONG)
                            driver.find_element_by_class_name('sz-zkm').click()
                            time.sleep(ACTION_WAIT_SLEEP_LONG)
                            while (count < LOAD_PAGE_TIMEOUT):
                                time.sleep(ACTION_WAIT_SLEEP_LONG)
                                select2ZzkmContainer = driver.find_element_by_id('select2-zkm-container')
                                if select2ZzkmContainer != None:
                                    break
                                # elements = driver.find_elements_by_class_name('select2-selection')
                                count = count + 1
                                if count == LOAD_PAGE_TIMEOUT:
                                    log.e("等待弹出框超时——选择银行")
                                    return 1
                                time.sleep(WHILE_WAIT_SLEEP)
                                # ActionChains(driver).move_to_element(
                                #     driver.find_element_by_class_name('sz-zkm')).click().perform()

                                driver.find_element_by_class_name('sz-zkm').click()
                            driver.find_element_by_id('select2-zkm-container').click()

                            time.sleep(ACTION_WAIT_SLEEP_LONG)
                            driver.find_element_by_class_name('select2-search__field').send_keys(detail.account_code)
                            hasBank = 1
                            count = 0
                            while (count < LOAD_PAGE_TIMEOUT):
                                if detail.account_code + '--' in driver.find_element_by_class_name(
                                        'select2-results__option').text:
                                    driver.switch_to_active_element().send_keys(Keys.DOWN)
                                    driver.switch_to_active_element().send_keys(Keys.ENTER)
                                    break
                                count = count + 1
                                time.sleep(WHILE_WAIT_SLEEP)
                            driver.find_element_by_id('zkm_sub').click()
                        elif getFeatureCdByCode(template.kmCode) == 4 or getFeatureCdByCode(template.kmCode) == 5:  # 往来
                            count = 0
                            # ActionChains(driver).move_to_element(
                            #     driver.find_element_by_class_name('sz-wldw')).click().perform()
                            element = driver.find_element_by_css_selector('div[class*="sz-wldw"]')
                            driver.execute_script("arguments[0].click();", element)
                            # driver.find_element_by_class_name('sz-wldw').click()
                            time.sleep(ACTION_WAIT_SLEEP_LONG)
                            if hasBank == 1:
                                elements = driver.find_elements_by_class_name('select2-selection')
                                while (count < LOAD_PAGE_TIMEOUT):
                                    time.sleep(WHILE_WAIT_SLEEP)

                                    if len(elements) == 2:
                                        break
                                    elements = driver.find_elements_by_class_name('select2-selection')
                                    count = count + 1
                                    if count == LOAD_PAGE_TIMEOUT:
                                        log.e("等待弹出框超时——选择往来")
                                        return 1
                                    time.sleep(WHILE_WAIT_SLEEP)
                                for i in range(len(elements)):
                                    aria_labelledby = elements[i].get_attribute('aria-labelledby')
                                    if aria_labelledby == 'select2-wldw-container':
                                        ActionChains(driver).move_to_element(elements[i]).click().perform()
                            else:
                                select2_selection = driver.find_element_by_class_name('select2-selection')
                                ActionChains(driver).move_to_element(
                                    driver.find_element_by_class_name('select2-selection')).click().perform()

                            # select2_selection= WebDriverWait(driver,10).until(lambda driver:driver.find_element_by_class_name('select2-selection'))
                            # ActionChains(driver).move_to_element(select2_selection).click().perform()
                            # driver.find_element_by_id('select2-wldw-container').click()
                            # WebDriverWait(driver, 10).until(
                            #     lambda driver: driver.find_element_by_id('select2-wldw-container')).click()

                            time.sleep(ACTION_WAIT_SLEEP_LONG)
                            driver.find_element_by_class_name('select2-search__field').send_keys(detail.partner_name)
                            time.sleep(ACTION_WAIT_SLEEP_LONG)
                            count = 0
                            while (count < LOAD_PAGE_TIMEOUT):
                                partner=driver.find_element_by_class_name('select2-results__option').text
                                if detail.partner_name ==partner or '公司--'+detail.partner_name ==partner :
                                    driver.switch_to.active_element.send_keys(Keys.DOWN)
                                    driver.switch_to.active_element.send_keys(Keys.ENTER)
                                    break
                                if partner == 'No results found' :
                                    log.w('往来单位不存在', detail.partner_name)

                                    ActionChains(driver).move_to_element(
                                        driver.find_element_by_class_name('select2-selection')).click().perform()

                                    time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                                    driver.find_element_by_id('wldw_add_sub').click()

                                    time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                                    driver.find_element_by_id('partnerName').send_keys(detail.partner_name)

                                    time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
                                    driver.find_element_by_id('add_wldw_sub').click()
                                    break
                                count = count + 1
                                time.sleep(WHILE_WAIT_SLEEP)
                            driver.find_element_by_id('wldw_sub').click()
            currentImgIdOld = driver.get_cookie('current_img_id')['value']
            driver.find_element_by_id("remark").send_keys("selenium 录入")

            time.sleep(ACTION_WAIT_SLEEP_LONG)
            driver.find_element_by_id('save').click()

            time.sleep(ACTION_WAIT_SLEEP_LONG)
            times = 0
            maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
            while times < maxTimes:
                try:
                    alert = WebDriverWait(driver, 1, poll_frequency=0.2).until(
                        lambda x: x.find_element_by_id("gritter-notice-wrapper"))
                    # log.w(alert.text)
                    if '保存成功' in alert.text:
                        log.i(documentIndex, '录入凭证成功', detail.document_id)
                        break

                except TimeoutException:
                     pass
                except:
                    log.exception('录入凭证异常')
                    return 1
                currentImgIdNew = driver.get_cookie('current_img_id')['value']

                log.d('点击保存等待', count, 'currentImgIdNew', currentImgIdNew, 'currentImgIdOld', currentImgIdOld)
                if currentImgIdNew != currentImgIdOld:
                    # print('currentImgIdNew', currentImgIdNew, 'currentImgIdOld', currentImgIdOld)
                    log.i(documentIndex, '录入凭证成功', detail.document_id)
                    break
                times = times + 1
                if count == LOAD_PAGE_TIMEOUT:
                    log.e(documentIndex, '录入凭证保存等待超时', detail.document_id)
                    return 1
                time.sleep(WHILE_WAIT_SLEEP)

            time.sleep(ACTION_WAIT_SLEEP_LONG)

        log.i('录入凭证结束')
        return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('录入凭证异常',r.status_code )
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
        driver.implicitly_wait(5)
        ret = login.run(driver, 'lxhw', '12344321')
        if (ret != 0):

            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:
            ret = run(driver)
            if (ret != 0):
                log.e('凭证录入失败', ret)
                time.sleep(config.FAIL_WAIT_SLEEP)

            time.sleep(5)
            driver.quit()

