import os
import time

from selenium import webdriver

from conf.config import window_size_w, window_size_h
from functionPage import toCertificateInput, addCertificate, login
from tools import log

if __name__=="__main__":
    print('main')
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=option)
    driver.set_window_size(window_size_w, window_size_h)
    driver.implicitly_wait(5)
    ret = login.run(driver, 'lxhw', '12344321')
    if (ret != 0):

        time.sleep(60)
        print('登陆失败')
    # ret = toCertificateInput.run(driver)
    # if (ret != 0):
    #     time.sleep(60)
    #     log.e('凭证录入失败', ret)

    ret = addCertificate.run(driver)
    if (ret != 0):
        time.sleep(60)
        log.e('新增凭证失败', ret)
    time.sleep(5)
    driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
