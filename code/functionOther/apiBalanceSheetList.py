import json
import os
import shutil
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from functionPage import login, toThird, loginNew
from module import Kemuyueb
from module.Kemuyueb import dict2Kemuyueb
from tools import log, commonSelenium, excelTools


def run(driver):
    log.d('资产负债表')
    dictsApi = {}
    try:
        params = {'origin': 'zidh',
                  'taxNo': config.caseTaxId,
                  'year': config.caseCurrentAccountYear,
                  'month': config.caseCurrentAccountMonth}

        log.i('API 资产负债表获取',config.domain_api)
        response = requests.get(config.domain_api + '/api/report/balancesheet', params=params, allow_redirects=False)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            ret = json.loads(response.text)
            if str(ret['code']) == '200':
                dictsApi = ret['data']
            else:

                log.e('API 资产负债表获取失败：', response.text)
                return 1
        else:
            log.e('API 资产负债表获取失败HTTP：', response.status_code)
            return 1
        log.i('API 资产负债表获取成功')
        if toThird.run(driver, config.caseCompanyName, config.caseTaxId):
            time.sleep(config.FAIL_WAIT_SLEEP)
            return 1
        if commonSelenium.toPage(driver, config.domain + "/cs-third/cer/balanceSheet/balanceSheetList"):
            return 1

        driver.find_element_by_id('currentDate').click()
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)

        months = driver.find_elements_by_class_name('month')
        for month in months:
            if str(config.caseCurrentAccountMonth) + '月' in month.text:
                ActionChains(driver).move_to_element(month).click().perform()
                time.sleep(config.ACTION_WAIT_SLEEP_LONG)
                break

        time.sleep(config.ACTION_WAIT_SLEEP_SHORT)
        shutil.rmtree(config.FILE_DOWNLOAD)
        os.mkdir(config.FILE_DOWNLOAD)
        driver.find_element_by_id('downloadBtn').click()
        times = 0
        maxTimes = int(config.LOAD_PAGE_TIMEOUT / config.WHILE_WAIT_SLEEP)
        while times < maxTimes:
            time.sleep(config.ACTION_WAIT_SLEEP_LONG)
            if '数据导出并下载成功' in driver.find_element_by_class_name('bootbox-body').text:
                btns = driver.find_elements_by_class_name('btn-primary')
                for btn in btns:
                    if btn.text == "OK":
                        btn.click()
                break
            if times == maxTimes:
                log.e("资产负债表-资产负债表下载超时")
                return 1
            times = times + 1

            log.w("资产负债表-资产负债表下载等待", times)
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        retCode, dictsDownload = excelTools.read_balanceSheetList()
        if retCode != 0:
            time.sleep(config.FAIL_WAIT_SLEEP)
            log.e('资产负债表下载失败：')
            return 1
        if len(dictsDownload)  != len(dictsApi)-1:
            log.e('API资产负债表数量与下载数量不一致 dictsDownload:', str(len(dictsDownload)), 'listsApi:', str(len(dictsApi)))

            return 1

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)

        time.sleep(config.ACTION_WAIT_SLEEP_LONG)
        rows = driver.find_elements_by_xpath("//table[@id='customerTable']/tbody/tr")
        for i in range(len(rows)):
            if i < 1:
                continue
            tdsSum = rows[i].find_elements_by_tag_name("td")

            if tdsSum[1].text != '' and tdsSum[1].text != '11':
                line = tdsSum[1].text
                qm = tdsSum[2].text.replace(',', '')
                nc = tdsSum[3].text.replace(',', '')
                # log.e('tdsSum[1]：\t', line)
                if  dictsApi['r' + line + 'qm'] == dictsDownload['r' + line + 'qm'] == qm=='' and dictsApi[
                    'r' + line + 'nc'] == dictsDownload['r' + line + 'nc'] == nc=='' :
                    pass
                elif not ( float(dictsApi['r' + line + 'qm']) ==float( dictsDownload['r' + line + 'qm']) == float(qm )and float(dictsApi[
                    'r' + line + 'nc'] )== float(dictsDownload['r' + line + 'nc'] )==float( nc)):
                    log.e('比较失败——行次', line, '\n页面：\t' '期末余额', qm, '年初余额', nc,
                          '\nAPI：\t', dictsApi['r' + line + 'qm'], '年初余额', dictsApi['r' + line + 'nc'],
                          '\n文件：\t', dictsDownload['r' + line + 'qm'], '年初余额', dictsDownload['r' + line + 'nc'])

                    return 1
                # else:
                #     log.d('行次',line,'期末余额', qm, '年初余额', nc )
            if tdsSum[5].text != '':
                line = tdsSum[5].text
                qm = tdsSum[6].text.replace(',', '')
                nc = tdsSum[7].text.replace(',', '')

                # log.e('tdsSum[5]：\t', line)
                if dictsApi['r' + line + 'qm'] == dictsDownload['r' + line + 'qm'] == qm == '' and dictsApi[
                    'r' + line + 'nc'] == dictsDownload['r' + line + 'nc'] == nc == '':
                    pass
                elif not (float(dictsApi['r' + line + 'qm']) == float(dictsDownload['r' + line + 'qm']) == float(
                        qm) and float(dictsApi[
                                          'r' + line + 'nc']) == float(dictsDownload['r' + line + 'nc']) == float(nc)):
                    log.e('比较失败——行次', line, '\n页面：\t' '期末余额', qm, '年初余额', nc,
                          '\nAPI：\t', dictsApi['r' + line + 'qm'], '年初余额', dictsApi['r' + line + 'nc'],
                          '\n文件：\t', dictsDownload['r' + line + 'qm'], '年初余额', dictsDownload['r' + line + 'nc'])

                    return 1
                # else:
                #     log.d('行次', line, '期末余额', qm, '年初余额', nc)
        if dictsApi['r30qm'] != dictsApi['r53qm'] or dictsApi['r30nc'] != dictsApi['r53nc']:
            log.e('资产负债不平衡')

            return 1
        log.i('资产负债表页面接口对比通过')
        return 0
    except:

        r = requests.get(driver.current_url, allow_redirects=False)
        log.exception('资产负债表', r.status_code)

        return 1


if __name__ == "__main__":
    print('main')
    config.set_host(config.HOST_SOURCE_ON_LINE)
    if (config.hostSource == None):
        log.e('未设置数据源')
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': config.FILE_DOWNLOAD}

        option.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(config.window_size_w, config.window_size_h)
        driver.implicitly_wait(5)
        ret = loginNew.run(driver)
        if (ret != 0):
            print('登陆失败')
            time.sleep(config.FAIL_WAIT_SLEEP)
            driver.quit()
        else:

            for i in range(20):
                run(driver)

                print('run',i)
            time.sleep(5)

            driver.quit()
