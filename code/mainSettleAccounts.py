import os
import time

from selenium import webdriver

from conf import config
from conf.config import window_size_w, window_size_h
from functionOther import apiBalanceList
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
        ret = initqmjz.run(driver)
        if (ret != 0):
            log.e('期末结转失败', ret)
            time.sleep(60)
        if (ret == 0):
            ret = certificateList.run(driver, config.caseCompanyName, config.caseTaxId, 1)
            if (ret != 0):
                log.e('审核凭证失败', ret)
                time.sleep(60)
        if (ret == 0):
            ret = toSettleAccounts.run(driver)
            if (ret != 0):
                log.e('结账失败', ret)
                time.sleep(60)
        if (ret == 0):
            ret = apiBalanceList.run(driver)
            if (ret != 0):
                log.e('余额表对比失败', ret)
                time.sleep(60)
        log.i('测试完成')
        time.sleep(5)
        driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
