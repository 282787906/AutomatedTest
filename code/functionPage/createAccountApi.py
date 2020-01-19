import json
import time

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from conf import config
from functionPage import toThird, loginNew
from tools import log


def run():

    log.d('建账')
    try:
        params = {'companyName': config.caseCompanyName,
                  'taxidCode': config.caseTaxId,
                  'startDate': str(config.caseCurrentAccountYear)+'-'+str(config.caseCurrentAccountMonth),

                  'accountSystem': '20191227-145623-870-66558' ,
                  'orgId': 1,
                  'auditerName': "shyuan",
                  'inputUserName': "lryuan",
                  'taxType': 2}
        log.i('API 建账', config.domain)
        response = requests.get(config.domain + '/cs-third/mod/customer/jz', params=params, allow_redirects=False)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            ret = json.loads(response.text)
            if str(ret['code']) == '200':

                log.i('API 建账成功：', response.text)
            else:
                log.e('API 建账失败：', response.text)
                return 1
        else:
            log.e('API 建账失败HTTP：', response.status_code)
            return 1


        return 0
    except:


        log.exception('API 建账', r.status_code)

        return 1


if __name__ == "__main__":
    print('main')
    # config.set_host(config.HOST_SOURCE_PRE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        ret = run()
        if (ret != 0):

            print('失败')
        else:
            option = webdriver.ChromeOptions()
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': config.FILE_DOWNLOAD}

            option.add_experimental_option('prefs', prefs)
            option.add_argument('disable-infobars')
            driver = webdriver.Chrome(options=option)
            driver.set_window_size(config.window_size_w, config.window_size_h)
            driver.implicitly_wait(5)
            ret = loginNew.run(driver)
            if (ret != 0):
                print('登陆失败')
                time.sleep(config.FAIL_WAIT_SLEEP)
                driver.quit()
            else:

                if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
                    time.sleep(config.FAIL_WAIT_SLEEP)

                time.sleep(5)
                driver.quit()