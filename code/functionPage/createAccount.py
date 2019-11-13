import time

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from conf import config
from functionPage import toThird, login
from module.AccountSetInfo import AccountSetInfo
from tools import log


def run(driver, accountSetInfo):

    log.d('建账')
    try:
        driver.get(config.domain + "/#/third/customer")

        driver.find_element_by_id('btn_company_add').send_keys(Keys.ENTER)
        driver.find_element_by_name('input_company_name').send_keys(accountSetInfo.companyName)

        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(accountSetInfo.taxidCode)
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        type = accountSetInfo.taxType
        if type == 0:
            driver.find_elements_by_class_name('el-radio')[0].click()  # 0小规模 1 一般纳税人 2申报周期 月 3 申报周期 季度
            driver.switch_to.active_element.send_keys(Keys.TAB)
        else:
            driver.find_elements_by_class_name('el-radio')[1].click()  # 0小规模 1 一般纳税人 2申报周期 月 3 申报周期 季度
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        yearStr = driver.find_elements_by_class_name('el-date-picker__header-label')[0].text
        monthStr = driver.find_elements_by_class_name('el-date-picker__header-label')[1].text
        year = int(yearStr.split(' ')[0])
        month = int(monthStr.split(' ')[0])
        lastYear = driver.find_element_by_class_name('el-icon-d-arrow-left')
        lastMonth = driver.find_elements_by_class_name('el-icon-arrow-left')[1]
        nextYear = driver.find_element_by_class_name('el-icon-d-arrow-right')
        nextMonth = driver.find_elements_by_class_name('el-icon-arrow-right')[1]

        years = accountSetInfo.startDateYear - year
        if years < 0:
            for i in range(-1 * years):  # <<
                ActionChains(driver).move_to_element(lastYear).click().perform()
                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        if years > 0:
            for i in range(years):  # >>
                ActionChains(driver).move_to_element(nextYear).click().perform()
                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        months = accountSetInfo.startDateMonth - month
        if months < 0:
            for i in range(-1 * months):  # <<
                ActionChains(driver).move_to_element(lastMonth).click().perform()
                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        if months > 0:
            for i in range(months):  # >>
                ActionChains(driver).move_to_element(nextMonth).click().perform()
                time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        driver.switch_to.active_element.send_keys(Keys.ENTER)
        print("mouseRightClick  Over")
        ActionChains(driver).move_to_element(driver.find_element_by_name("select_account_system")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        accountSystems = driver.find_elements_by_name('li_account_system')
        for i in range(len(accountSystems)):
            driver.find_element_by_name("select_account_system").send_keys(Keys.DOWN)
            if accountSystems[i].text == accountSetInfo.accountSystem:
                ActionChains(driver).move_to_element(accountSystems[i]).click().perform()
                break

            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_org_id")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        orgs = driver.find_elements_by_name('li_org_id')
        for i in range(len(orgs)):
            driver.find_element_by_name("select_org_id").send_keys(Keys.DOWN)
            if orgs[i].text == accountSetInfo.org:
                ActionChains(driver).move_to_element(orgs[i]).click().perform()
                break

            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_zx_center")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        zxCenters = driver.find_elements_by_name('li_zx_center')

        for i in range(len(zxCenters)):
            driver.find_element_by_name("select_zx_center").send_keys(Keys.DOWN)
            if zxCenters[i].text == accountSetInfo.zxCenter:
                ActionChains(driver).move_to_element(zxCenters[i]).click().perform()
                break
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_zcfzgs")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        zcfzgs = driver.find_elements_by_name('li_zcfzgs')
        for i in range(len(zcfzgs)):
            driver.find_element_by_name("select_zcfzgs").send_keys(Keys.DOWN)
            if zcfzgs[i].text == accountSetInfo.zcfzgs:
                ActionChains(driver).move_to_element(zcfzgs[i]).click().perform()
                break

            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_auditer_id")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        auditerIds = driver.find_elements_by_name('li_auditer_id')
        for i in range(len(auditerIds)):
            driver.find_element_by_name("select_auditer_id").send_keys(Keys.DOWN)
            if "审核员" in auditerIds[i].text:
                ActionChains(driver).move_to_element(auditerIds[i]).click().perform()
                driver.find_element_by_name("select_auditer_id").send_keys(Keys.ESCAPE)
                break
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_input_user_id")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        inputUserIds = driver.find_elements_by_name('li_input_user_id')
        for i in range(len(inputUserIds)):
            driver.find_element_by_name("select_input_user_id").send_keys(Keys.DOWN)
            if "录入员" in inputUserIds[i].text:
                ActionChains(driver).move_to_element(inputUserIds[i]).click().perform()
                driver.find_element_by_name("select_input_user_id").send_keys(Keys.ESCAPE)
                break
            time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_information_officer_id")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        informationOfficerIds = driver.find_elements_by_name('li_information_officer_id')
        ActionChains(driver).move_to_element(informationOfficerIds[0]).click().perform()
        driver.find_element_by_name("select_information_officer_id").send_keys(Keys.ESCAPE)
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_scanner_id")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        scannerIds = driver.find_elements_by_name('li_scanner_id')
        ActionChains(driver).move_to_element(scannerIds[0]).click().perform()
        driver.find_element_by_name("select_scanner_id").send_keys(Keys.ESCAPE)
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_declarer_id")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        declarerIds = driver.find_elements_by_name('li_declarer_id')
        ActionChains(driver).move_to_element(declarerIds[0]).click().perform()
        driver.find_element_by_name("select_declarer_id").send_keys(Keys.ESCAPE)
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        ActionChains(driver).move_to_element(driver.find_element_by_name("select_info_completion_id")).click().perform()
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        infoCompletionIds = driver.find_elements_by_name('li_info_completion_id')
        ActionChains(driver).move_to_element(infoCompletionIds[0]).click().perform()
        driver.find_element_by_name("select_info_completion_id").send_keys(Keys.ESCAPE)
        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)

        driver.find_element_by_name('input_sb_taxrate').send_keys('22')
        driver.find_element_by_name('input_sb_stock').send_keys('33')
        driver.find_element_by_name('input_scanning_date').send_keys('1')
        driver.find_element_by_name('input_checkout_date').send_keys('28')
        driver.find_element_by_name('input_sb_stock_proportion1').send_keys('1')
        driver.find_element_by_name('input_sb_stock_proportion2').send_keys('2')
        driver.find_element_by_name('input_sb_stock_proportion3').send_keys('3')
        driver.find_element_by_name('input_sb_stock_proportion4').send_keys('4')
        driver.find_element_by_name('input_sb_stock_proportion5').send_keys('5')
        driver.find_element_by_name('btn_save').send_keys(Keys.ENTER)
        if toThird.run(driver,accountSetInfo.companyName,accountSetInfo.taxidCode):
            log.e("建账后进账簿失败")
            return 1
        else:
            log.i("建账成功")
            return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('建账异常',r.status_code )
        return 1
if __name__=="__main__":
    print('createAccount')
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
            accountSetInfo = AccountSetInfo('回归测试2', 'taxidCode000000002', 1, 2019, 8, 1, '物流行业科目体系', '默认组',
                                            '伊文科技',
                                            '通用公式')
            ret = run(driver, accountSetInfo)
            if (ret != 0):
                print('建账失败')
                time.sleep(config.FAIL_WAIT_SLEEP)

            time.sleep(5)
            driver.quit()