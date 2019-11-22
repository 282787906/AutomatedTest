import pyperclip as pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from conf import config
from tools import log, mySqlHelper, commonSelenium


def main():
    # while 1:
    #     log.i('选择项目(crm,third,)','\n')
    #     table = input()
    #     if table == 'crm' or table == 'third':
    #         break
    while 1:
        log.i('输入id','\n')
        id = input()
        try:
            id = int(id)
            break
        except:
            log.w('输入id转换失败\n')
    # log.i('参数：', table, str(id))
    ret ,af,bf,msg=mySqlHelper.getThirdLog(id)
    if ret!=0:
        return 1
    log.i('参数：', af, bf )
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=option)
    driver.set_window_size(config.window_size_w, config.window_size_h)
    driver.implicitly_wait(5)
    commonSelenium.toPage(driver,'https://www.sojson.com/jsondiff.html')

    ActionChains(driver).move_to_element(driver.find_elements_by_class_name('CodeMirror-sizer')[0]).double_click().perform()
    commonSelenium.clearElement(driver.switch_to.active_element)
    pyperclip.copy(af )
    driver.switch_to.active_element.send_keys(Keys.Ct)

    ActionChains(driver).move_to_element(
        driver.find_elements_by_class_name('CodeMirror-sizer')[1]).double_click().perform()
    commonSelenium.clearElement(driver.switch_to.active_element)
    driver.switch_to.active_element.send_keys(bf)

    log.i('参数：', af, bf )



if __name__ == "__main__":
    print('main')
    # config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        main()
