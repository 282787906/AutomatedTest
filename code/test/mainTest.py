from selenium import webdriver
from HTMLTestRunner import HTMLTestRunner  # 导入HTMLTestRunner模块
import unittest, time


class BaiduIdeTest(unittest.TestCase):
    # 三引号表示doc string类型注释，用来描述函数、类和方法
    '''baidu search testing'''

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.baidu.com/"

    def test_baidu_ide(self):
        '''Search Keyword'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys("HTMLTestRunner")
        driver.find_element_by_id("su").click()
        time.sleep(1)
        self.assertEqual(u"HTMLTestRunner_百度搜索", driver.title)

    def test_baidu_ide1(self):
        '''Search Keyword'''
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys("python")
        driver.find_element_by_id("su").click()
        time.sleep(1)
        # self.assertEqual(u"HTMLTestRunner_百度搜索", driver.title)
    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    # 构造测试套件
    testsuit = unittest.TestSuite()
    testsuit.addTest(BaiduIdeTest("test_baidu_ide"))
    testsuit.addTest(BaiduIdeTest("test_baidu_ide1"))
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
