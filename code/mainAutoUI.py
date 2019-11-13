import os
import sys
import time
import unittest
from HTMLTestRunner import HTMLTestRunner
from lib2to3.pgen2 import driver

from selenium import webdriver

from conf import config
from conf.config import window_size_w, window_size_h
from functionPage import login, toCertificateInput, addCertificate
from tools import log


class AutoUI(unittest.TestCase):
    def setUp(self):
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        if config.showUI==config.SHOW_UI_FALSE:
            log.i('不显示界面')
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
        else:
            log.i('显示界面')

        self.driver = webdriver.Chrome(options=option)
        self.driver.set_window_size(window_size_w, window_size_h)
        self.driver.implicitly_wait(5)
    def login(self):

        ret = login.run(self.driver)
        if (ret != 0):
            time.sleep(60)
            print('登陆失败')
        # ret = toCertificateInput.run(driver)
        # if (ret != 0):
        #     time.sleep(60)
        #     log.e('凭证录入失败', ret)
        # ret = addCertificate.run(driver)
        # if (ret != 0):
        #     time.sleep(60)
        #     log.e('新增凭证失败', ret)
    def add(self):
        ret = login.run(self.driver)
        if (ret != 0):
            time.sleep(60)
            print('登陆失败')
        ret = addCertificate.run(self.driver)
        if (ret != 0):
            time.sleep(60)
            log.e('新增凭证失败', ret)
    # def tearDown(self):
        # self.driver.quit()
def paramInfo():
    str = os.path.basename(__file__) + '数据库状态监控'
    str = str + '\n参数说明:'
    str = str + '\n' + 'runWith:\t0-default;1-pycharm;2-Cmd'
    str = str + '\n' + 'host:\tonline-生产环境;pre-预发布环境'
    str = str + '\n' + 'showUI:\t1-显示界面;0-不显示界面'
    return str


if __name__ == "__main__":
    print('main')

    if len(sys.argv) == 4 and (sys.argv[1] == '0' or sys.argv[1] == '1' or sys.argv[1] == '2') \
            and (sys.argv[2] == 'online' or sys.argv[2] == 'pre' and (sys.argv[3] == '1' or sys.argv[3] == '0')):

        config.set_runWith(sys.argv[1])
        config.set_host(sys.argv[2])
        config.set_showUI(sys.argv[3])

    else:
        print(paramInfo())
        config.set_runWith(config.RUN_WITH_UNKNOW)
        config.set_host(config.HOST_SOURCE_PRE)
        # config.set_showUI(sys.argv[3])

    # 构造测试套件
    testsuit = unittest.TestSuite()
    testsuit.addTest(AutoUI('login'))
    testsuit.addTest(AutoUI("add"))
    # 按照一定格式获取当前时间,%Y表示带世纪的年（2019），%y表示不带世纪的年（19），time.strftime()表示获得当前时间并格式化字符串
    now = time.strftime("%Y%m%d_%H%M%S")
    # 将当前时间加入到报告文件名称中
    filename = './' + now + 'result.html'
    # 定义测试报告存放路径，通过open()方法以二进制写模式('wb')打开当前目录下的result.heml，如果没有，则自动创建。
    fp = open('./result.html', 'wb')
    # 定义测试报告，调用HTMLTestRunner模块下的HTMLTestRunner类，stream 指定测试报告文件，title 定义测试报告的标题，description 定义测试报告的副标题
    runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='用例执行情况：')
    # 通过HTMLTestRunner的run()方法来运行测试套件中的测试用例
    runner.run(testsuit)
    # 关闭测试报告
    fp.close()
