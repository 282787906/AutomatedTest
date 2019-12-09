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

        if (ret == 0):
            ret = toCertificateInput.run(driver)
            if (ret != 0):
                log.e('凭证录入失败', ret)
                time.sleep(60)
        if (ret == 0):
            ret = addCertificate.run(driver)
            if (ret != 0):
                log.e('新增凭证失败', ret)
                time.sleep(60)


        log.e('测试完成')
        time.sleep(5)
        driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
