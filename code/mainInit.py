import os
import time

from selenium import webdriver

from conf import config
from conf.config import window_size_w, window_size_h
from functionOther import apiBalanceSheetList
from functionPage import login, toCertificateInput, addCertificate, certificateList, toThird, initqmjz, \
    toSettleAccounts, originCertificate, kmqcfun, contactsunitlist
from tools import log, commonSelenium

if __name__ == "__main__":
    print('main')
    # config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(window_size_w, window_size_h)
        driver.implicitly_wait(5)
        ret = login.run(driver)
        if (ret != 0):
            time.sleep(60)
            print('登陆失败')
        if (ret == 0):
            ret = toSettleAccounts.runBack(driver)
            if (ret != 0):
                log.e('反结账失败', ret)
                time.sleep(60)
        if (ret == 0):
            ret = certificateList.run(driver, config.caseCompanyName, config.caseTaxId, 2)
            if (ret != 0):
                log.e('批量凭证取消审核', ret)
                time.sleep(60)
        if (ret == 0):
            ret = certificateList.run(driver, config.caseCompanyName, config.caseTaxId, 3)
            if (ret != 0):
                log.e('清空凭证失败', ret)
                time.sleep(60)
        if (ret == 0):
            ret = kmqcfun.runInit(driver)
            if (ret != 0):
                log.e('清空新增科目失败', ret)
                time.sleep(60)
        if (ret == 0):
            ret = contactsunitlist.runClear(driver)
            if (ret != 0):
                log.e('清空往来失败', ret)
                time.sleep(60)
        if (ret == 0):
            ret = originCertificate.runDelete(driver)
            if (ret != 0):
                log.e('删除原始凭证失败', ret)
                time.sleep(60)

        log.e('测试完成')
        time.sleep(5)
        driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
