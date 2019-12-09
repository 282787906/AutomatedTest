import os
import sys
import time

from selenium import webdriver

from conf import config
from conf.config import window_size_w, window_size_h
from functionOther import apiBalanceList
from functionPage import login, toCertificateInput, addCertificate, certificateList, toThird, initqmjz, \
    toSettleAccounts, originCertificate, kmqcfun, contactsunitlist, loginNew
from tools import log, commonSelenium
def paramInfo():
    str = os.path.basename(__file__) + '数据库状态监控'
    str = str + '\n参数说明:'
    str = str + '\n' + 'runWith:\t0-default;1-pycharm;2-Cmd'
    str = str + '\n' + 'host:\tonline-生产环境;pre-预发布环境'
    return str
if __name__ == "__main__":
    print('main')
    # config.set_host(config.HOST_SOURCE_PRE)

    print(paramInfo())
    if len(sys.argv) == 3 and (sys.argv[1] == '0' or sys.argv[1] == '1' or sys.argv[1] == '2') and (
            sys.argv[2] == 'online' or sys.argv[2] == 'pre'):
        config.set_runWith(sys.argv[1])
        config.set_host(sys.argv[2])
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(window_size_w, window_size_h)
        driver.implicitly_wait(5)
        # ret = login.run(driver)
        # if (ret != 0):
        #     time.sleep(60)
        #     print('登陆失败')
        # if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
        #     print('进账簿失败')

        ret = loginNew.run(driver)
        if (ret != 0):
            time.sleep(60)
            print('第三方跳转登陆失败')
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
        if (ret == 0):

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
        log.e('测试完成')
        time.sleep(5)
        driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
