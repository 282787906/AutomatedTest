import os
import time
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from conf import config
from conf.config import window_size_w, window_size_h, ACTION_WAIT_SLEEP_LONG, LOAD_PAGE_TIMEOUT, WHILE_WAIT_SLEEP, \
    ACTION_WAIT_SLEEP_SHORT, DOWNLOAD_TIMEOUT, WHILE_WAIT_SLEEP_LONG
from tools import log, commonSelenium
from tools.commonSelenium import toPage
from tools.mySqlHelper import insertMigCompany, getMigCompany, updateMigCompanyYear, getMigCompanyMaxSerNo, \
    getLangChaoCompany, updateMigCompanyGdStatus


def paramInfo():
    str = os.path.basename(__file__) + '数据库状态监控'
    str = str + '\n参数说明:'
    str = str + '\n' + 'runWith:\t0-default;1-pycharm;2-Cmd'
    str = str + '\n' + 'host:\tonline-生产环境;pre-预发布环境'
    return str


loginName = ''


def login(driver, userName, userPwd):
    try:
        if toPage(driver, "https://vip.eyun.cn/login/login.html"):
            log.e('CRM登录失败-进入CRM登录页超时')
            return 1

        time.sleep(ACTION_WAIT_SLEEP_LONG)

        driver.find_element_by_id('login-phone').send_keys(userName)
        driver.find_element_by_id('login-pass').send_keys(userPwd)

        driver.find_element_by_id('btn-login').click()
        time.sleep(ACTION_WAIT_SLEEP_LONG)

        # driver.find_element_by_class_name('sure-btn-qiye-submit').click()

        times = 0
        maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
        while times < maxTimes:
            if driver.current_url.startswith('https://vip.eyun.cn/eyun3/html/#/'):
                time.sleep(ACTION_WAIT_SLEEP_LONG)
                log.i('登录成功')
                return 0
            times = times + 1
            time.sleep(WHILE_WAIT_SLEEP)
        log.e('C登录失败-登录超时')
        return 1
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)

        log.exception('登录异常', r.status_code)
        return 1


def del_file(path, delSelf=False):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path, delSelf)
        else:
            os.remove(c_path)
    if delSelf:
        os.rmdir(path)


def getQc(driver):
    try:

        name = driver.find_element_by_xpath("//div[@class = 'mainLogo']/div[1]/span").text

        path = config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG + name + '\\'
        存在科目表 = False
        存在科目期初 = False
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            ls = os.listdir(path)
            for file in ls:

                if file.find('科目表') != -1:
                    log.i('科目表已存在')
                    存在科目表 = True
                if file.find('科目期初') != -1:
                    log.i('科目期初已存在')
                    存在科目期初 = True
        if 存在科目表 and 存在科目期初:
            return
        wait = WebDriverWait(driver, 20)
        设置 = wait.until(EC.presence_of_element_located((By.ID, 'moreBtn')))
        设置.click()
        log.i('菜单click')
        time.sleep(ACTION_WAIT_SLEEP_SHORT)
        # driver.find_element_by_link_text('余额表').click()
        科目期初 = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '科目期初')))
        科目期初.click()
        log.i('科目期初click')

        if not 存在科目表:
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            asd = driver.find_elements_by_class_name('icon-daoru')
            del_file(config.FILE_DOWNLOAD)

            导出 = asd[0]
            commonSelenium.mouseLocationReset(driver)
            commonSelenium.mouseMove(driver, 导出.location['x'], 导出.location['y'])
            commonSelenium.mouseMove(driver, 导出.location['x'] + 2, 导出.location['y'])
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            导出.click()
            log.i(asd[0].text, 'click')

            导出科目表 = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '导出科目表')))
            导出科目表.click()
            times = 0
            maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
            while (times < maxTimes):
                list = os.listdir(config.FILE_DOWNLOAD)
                if len(list) > 0 and list[0].endswith('.xls'):
                    os.rename(config.FILE_DOWNLOAD + "\\" + list[0],
                              path + list[0])

                    log.e('下载科目表完成')
                    break
                times = times + 1
                if times == maxTimes:
                    log.e('下载科目表等待 超时')
                    return 1
                time.sleep(WHILE_WAIT_SLEEP)
        if not 存在科目期初:
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            asd = driver.find_elements_by_class_name('icon-daoru')
            del_file(config.FILE_DOWNLOAD)

            导出 = asd[0]
            commonSelenium.mouseMove(driver, 导出.location['x'], 导出.location['y'])
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            导出.click()
            log.i(asd[0].text, 'click')

            导出科目期初 = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '导出科目期初')))
            导出科目期初.click()
            times = 0
            maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
            while (times < maxTimes):
                list = os.listdir(config.FILE_DOWNLOAD)
                if len(list) > 0 and list[0].endswith('.xls'):
                    os.rename(config.FILE_DOWNLOAD + "\\" + list[0],
                              path + list[0])

                    log.e('下载科目期初完成')
                    break
                times = times + 1
                if times == maxTimes:
                    log.e('下载科目期初等待 超时')
                    return 1
                time.sleep(WHILE_WAIT_SLEEP)
        return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)

        log.exception('下载科目期初异常', r.status_code)
        return 1


def getBalance(driver):
    try:
        name = driver.find_element_by_xpath("//div[@class = 'mainLogo']/div[1]/span").text
        path = config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG + name + '\\'
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            ls = os.listdir(path)
            for file in ls:
                if file.find('余额表') != -1:
                    log.i('余额表已存在')
                    # return

        wait = WebDriverWait(driver, 20)
        菜单 = wait.until(EC.presence_of_element_located((By.ID, 'costReport')))
        菜单.click()

        log.i('菜单click')
        time.sleep(ACTION_WAIT_SLEEP_LONG)

        余额表 = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '余额表')))
        余额表.click()

        log.i('余额表click')
        time.sleep(ACTION_WAIT_SLEEP_LONG)
        months = driver.find_elements_by_class_name('monthItem')

        for index in range(len(months)):
            if months[index].get_attribute('data-month') == '202001':
                months[index].click()
        del_file(config.FILE_DOWNLOAD)
        下载余额表 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-xiazai')))
        下载余额表 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'icon-xiazai')))

        下载余额表.click()
        log.i('下载余额表click')
        times = 0
        maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
        while (times < maxTimes):
            list = os.listdir(config.FILE_DOWNLOAD)
            if len(list) > 0 and list[0].endswith('.xls'):
                os.rename(config.FILE_DOWNLOAD + "\\" + list[0],
                          path + name + "_" + list[0])

                log.e('下载余额表完成')
                break
            times = times + 1
            if times == maxTimes:
                log.e('下载余额表等待 超时')
                return 1
            time.sleep(WHILE_WAIT_SLEEP)
        return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)

        log.exception('下载余额表异常', r.status_code)
        return 1


def getFixedAssets(driver):
    try:
        name = driver.find_element_by_xpath("//div[@class = 'mainLogo']/div[1]/span").text
        path = config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG + name + '\\'
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            ls = os.listdir(path)
            for file in ls:

                if file.find('固定资产') != -1:
                    log.i('固定资产已存在')
                    return
        wait = WebDriverWait(driver, 20)
        固定资产 = wait.until(EC.presence_of_element_located((By.ID, 'fixedAssets')))
        固定资产.click()

        log.i('菜单click')
        time.sleep(ACTION_WAIT_SLEEP_LONG)
        固定资产管理 = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '固定资产管理')))
        固定资产管理.click()

        log.i('固定资产管理click')
        time.sleep(ACTION_WAIT_SLEEP_LONG)

        # pagelistarea = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'page-list-area')))
        # if str(pagelistarea[0].text).startswith('每页') and str(pagelistarea[0].text).endswith('0条'):
        #     log.w('不存在固定资产')
        #     return 0
        del_file(config.FILE_DOWNLOAD)

        time.sleep(ACTION_WAIT_SLEEP_SHORT)
        下载固定资产 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'icon-xiazai')))
        #
        下载固定资产.click()
        log.i('下载固定资产表click')
        times = 0
        maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
        while (times < maxTimes):
            list = os.listdir(config.FILE_DOWNLOAD)
            if len(list) > 0 and list[0].endswith('.xls'):
                os.rename(config.FILE_DOWNLOAD + "\\" + list[0],
                          path + name + "_" + list[0])
                driver.find_elements_by_class_name('els_span newtipNode')
                log.e('下载固定资产完成')
                break
            times = times + 1
            if times == maxTimes:
                log.e('下载凭证表等待 超时')
                return 1
            time.sleep(WHILE_WAIT_SLEEP)
        return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)

        log.exception('下载固定资产异常', r.status_code)
        return 1


def 遍历账簿(driver):
    serNo = driver.find_elements_by_class_name('ser-no')
    names = driver.find_elements_by_class_name('cus-name')
    进账簿按钮集合 = driver.find_elements_by_class_name('goto-vm-btn')

    if len(names) != len(进账簿按钮集合):
        log.exception('len(names)!=len(进账簿按钮集合)', str(len(names)), str(len(进账簿按钮集合)))
        return 1

    for index in range(len(进账簿按钮集合)):
        try:
            path = config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG + names[index].text + '\\'
            存在科目表 = False
            存在科目期初 = False
            存在余额表 = False
            存在固定资产 = False
            存在凭证列表 = False
            if not os.path.isdir(path):
                os.mkdir(path)
            else:
                ls = os.listdir(path)
                for file in ls:

                    if file.find('科目表') != -1:
                        存在科目表 = True
                    elif file.find('科目期初') != -1:
                        存在科目期初 = True
                    # elif file.find('凭证列表_202001') != -1:
                    #     存在凭证列表 = True
                    elif file.find('固定资产') != -1:
                        存在固定资产 = True
                    elif file.find('余额表_202001-202001') != -1:
                        存在余额表 = True

            if 存在科目表 and 存在科目期初 and 存在凭证列表 and 存在固定资产 and 存在余额表:
                log.i(serNo[index].text, names[index].text, "所有文件下载完毕")
                continue
            log.i('进账簿', serNo[index].text, names[index].text)

            进账簿按钮集合[index].click()
            handles = driver.window_handles
            driver.switch_to.window(handles[1])
            getQc(driver)
            getBalance(driver)
            getFixedAssets(driver)
            driver.close()
            driver.switch_to.window(handles[0])
            # return 0
        except BaseException as e:
            r = requests.get(driver.current_url, allow_redirects=False)

            log.exception('遍历账簿异常', r.status_code)

    下一页按钮 = driver.find_elements_by_class_name('w-pagn-btn')[1]
    print(下一页按钮.text)

    if str(下一页按钮.get_attribute('class')).find('disable') == -1:
        wait = WebDriverWait(driver, 20)
        pagingJumpTo = wait.until(EC.presence_of_element_located((By.ID, 'pagingJumpTo')))
        pagingJumpToValue = pagingJumpTo.get_attribute('value')
        if pagingJumpToValue == '1':
            return 0
        下一页按钮.click()
        times = 0
        maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
        while (times < maxTimes):

            if wait.until(EC.presence_of_element_located((By.ID, 'pagingJumpTo'))).get_attribute(
                    'value') != pagingJumpToValue:
                break
            times = times + 1
            if times == maxTimes:
                log.e('翻页等待 超时')
                return 1
            time.sleep(WHILE_WAIT_SLEEP)
        return 遍历账簿(driver)
    else:
        return 0


def 归档(driver):
    try:
        name = driver.find_element_by_xpath("//div[@class = 'mainLogo']/div[1]/span").text
        path = config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG + name + '\\'
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            ls = os.listdir(path)
            for file in ls:
                if file.find('固定资产') != -1:
                    log.i('固定资产已存在')
                    return
        wait = WebDriverWait(driver, 20)
        设置 = wait.until(EC.presence_of_element_located((By.ID, 'moreBtn')))
        设置.click()

        log.i('菜单click')
        time.sleep(ACTION_WAIT_SLEEP_LONG)
        归档管理 = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '归档管理')))
        归档管理.click()

        log.i('归档管理.click()')
        time.sleep(ACTION_WAIT_SLEEP_LONG)
        years = driver.find_elements_by_class_name('year')
        del_file(path)
        for index in range(len(years)):
            years[index].click()
            # 归档
            归档 = driver.find_element_by_class_name('greenIconBtn')
            归档.click()
            log.i(years[index].text + '归档 ')
            maxTimes = int(DOWNLOAD_TIMEOUT / WHILE_WAIT_SLEEP_LONG)
            times = 0
            while (times < maxTimes):
                if 归档.text == '归档':
                    log.i(years[index].text + '归档完成')
                    break
                times = times + 1
                if times == maxTimes:
                    log.e(years[index].text + '归档等待 超时')
                    return 1
                else:
                    log.d(years[index].text + '归档等待  ' + str(times) + '/' + str(maxTimes))
                time.sleep(WHILE_WAIT_SLEEP_LONG)

            del_file(config.FILE_DOWNLOAD)
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            checkbox = driver.find_element_by_xpath("//table[@class = 'dgrid-row-table']/thead/tr/th/input")
            checkbox.click()
            下载Excel = driver.find_element_by_class_name('downloadExcelBtn')

            下载Excel.click()
            log.i(years[index].text + ' 下载Excel')
            times = 0
            while (times < maxTimes):
                list = os.listdir(config.FILE_DOWNLOAD)
                if len(list) > 0 and list[0].startswith(name) and list[0].endswith('.zip'):
                    log.i(years[index].text + ' 下载Excel完成 复制')
                    os.rename(config.FILE_DOWNLOAD + "\\" + list[0],
                              path + list[0])
                    driver.find_elements_by_class_name('els_span newtipNode')

                    log.i(years[index].text + ' 复制完成')
                    break
                times = times + 1
                if times == maxTimes:
                    log.e(years[index].text + '归档文件下载等待 超时')
                    break
                else:
                    log.d(years[index].text + '归档文件下载等待  ' + str(times) + '/' + str(maxTimes))
                time.sleep(WHILE_WAIT_SLEEP_LONG)
        log.i(name + '  ' + '   归档完成')
        return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)

        log.exception('归档异常', r.status_code)
        return 1


def 遍历账簿_归档(driver):
    serNo = driver.find_elements_by_class_name('ser-no')
    names = driver.find_elements_by_class_name('newGap')
    进账簿按钮集合 = driver.find_elements_by_class_name('action-left')

    if len(names) != len(进账簿按钮集合):
        log.exception('len(names)!=len(进账簿按钮集合)', str(len(names)), str(len(进账簿按钮集合)))
        return 1

    for index in range(len(进账簿按钮集合)):
        try:
            # path = config.FILE_DOWNLOAD_COMPANY + names[index].text + '\\'
            # 存在科目表 = False
            # 存在科目期初 = False
            # 存在余额表 = False
            # 存在固定资产 = False
            # 存在凭证列表 = False
            # if not os.path.isdir(path):
            #     os.mkdir(path)
            # else:
            #     ls = os.listdir(path)
            #     for file in ls:
            #
            #         if file.find('科目表') != -1:
            #             存在科目表 = True
            #         elif file.find('科目期初') != -1:
            #             存在科目期初 = True
            #         # elif file.find('凭证列表_202001') != -1:
            #         #     存在凭证列表 = True
            #         elif file.find('固定资产') != -1:
            #             存在固定资产 = True
            #         elif file.find('余额表_202001-202001') != -1:
            #             存在余额表 = True
            #
            # if 存在科目表 and 存在科目期初 and 存在凭证列表 and 存在固定资产 and 存在余额表:
            #     log.i(serNo[index].text, names[index].text, "所有文件下载完毕")
            #     continue
            log.i('进账簿', serNo[index].text, names[index].text)

            进账簿按钮集合[index].click()
            handles = driver.window_handles
            driver.switch_to.window(handles[1])
            归档(driver)

            driver.close()
            driver.switch_to.window(handles[0])
            # return 0
        except BaseException as e:
            r = requests.get(driver.current_url, allow_redirects=False)

            log.exception('遍历账簿异常', r.status_code)

    下一页按钮 = driver.find_elements_by_class_name('w-pagn-btn')[1]
    print(下一页按钮.text)

    if str(下一页按钮.get_attribute('class')).find('disable') == -1:
        wait = WebDriverWait(driver, 20)
        pagingJumpTo = wait.until(EC.presence_of_element_located((By.ID, 'pagingJumpTo')))
        pagingJumpToValue = pagingJumpTo.get_attribute('value')
        if pagingJumpToValue == '1':
            return 0
        下一页按钮.click()
        times = 0
        maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
        while (times < maxTimes):

            if wait.until(EC.presence_of_element_located((By.ID, 'pagingJumpTo'))).get_attribute(
                    'value') != pagingJumpToValue:
                break
            times = times + 1
            if times == maxTimes:
                log.e('翻页等待 超时')
                return 1
            time.sleep(WHILE_WAIT_SLEEP)
        return 遍历账簿_归档(driver)
    else:
        return 0


def 科目表_切换账簿(driver):
    try:

        # 菜单手动
        toPage(driver, "https://ykj.eyun.cn/eyun3/html/#/accountNumber")
        retCode, companies, msg = getLangChaoCompany()
        if retCode != 0:
            log.e(msg)

            return
        unFind = 0
        for index in range(len(companies)):
            jindu = str(index) + '/' + str(len(companies))
            name = companies[index].companyName.strip()
            path = config.FILE_DOWNLOAD_COMPANY_LANGCHAOYUN + name + '\\'
            #
            # list = os.listdir(path)
            # for index in range(len(companies)):
            #     log.e(list[index])
            # if path.endswith('*\\'):
            #     path = path.replace('*\\', '\\')
            # if not os.path.isdir(path):
            #     os.mkdir(path)
            # if companies[index].startYear == companies[index].currentYear and companies[index].startYear == 2020:
            #     log.i(jindu + '  ' + name + '  ' + str(companies[index].currentYear) + ' 跳过')
            #     continue
            # if not companies[index].currentYear == None:
            #     allFileExist = False
            #     for y in range(companies[index].startYear, companies[index].currentYear + 1):
            #         if y > 2020:
            #             log.i(jindu + '  ' + name + '  ' + str(y) + ' 跳过')
            #             allFileExist = True
            #             continue
            #         if y == 2020:
            #             log.i(jindu + '  ' + name + '  ' + str(y) + ' 临时跳过')
            #             allFileExist = True
            #             continue
            #         fileName = path + name.replace('*', '') + str(y) + '会计归档.zip'
            #         if os.path.exists(fileName):
            #             log.i(jindu + '  ' + name + '  ' + str(y) + ' 归档文件已存在')
            #             allFileExist = True
            #         else:
            #             allFileExist = False
            #             break
            #     if allFileExist:
            #         continue

            # 设置 = wait.until(EC.presence_of_element_located((By.ID, 'moreBtn')))
            findTxt = driver.find_elements_by_class_name('el-input__inner')[0]
            findTxt.click()
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            findTxt.send_keys(name)
            # findTxt.send_keys("北京天泽汇丰建筑工程有限公司濮阳分公司")
            # time.sleep(ACTION_WAIT_SLEEP_SHORT)
            ret = driver.find_elements_by_class_name('el-select-dropdown__item')
            if len(ret) == 0:
                log.e(jindu + '  ' + name + '  ' + ' 公司名模糊查询无结果')
                continue
            match = False
            for i in range(len(ret)):
                # if ret[i].get_attribute("style") =='display: none;':
                #     continue
                if ret[i].text == name:
                    ret[i].click()
                    match = True
                    break

            if not match:
                unFind = unFind + 1
                log.e(jindu + '  ' + name + '  ' + ' 公司名模糊查询结果无匹配  ' + str(unFind))
                continue
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            toPage(driver, "https://ykj.eyun.cn/eyun3/html/#/accountNumber")
            层级 = driver.find_element_by_class_name("cjps")
            log.i('层级  ' + 层级.text)

            下载Excel = driver.find_elements_by_class_name('el-button--default')

            下载Excel[1].click()

            maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
            times = 0
            while (times < maxTimes):
                list = os.listdir(config.FILE_DOWNLOAD)
                if len(list) > 0:
                    log.i(jindu + '  ' + name + ' 下载Excel完成 复制')
                    os.rename(config.FILE_DOWNLOAD + "\\" + list[0],
                              path + "科目表.xls")
                    log.i(jindu + '  ' + name + ' 复制完成')
                    break
                times = times + 1
                if times == maxTimes:
                    log.e(name + '文件下载等待 超时')
                    break
                else:
                    log.d(jindu + '  ' + name + '文件下载等待  ' + str(times) + '/' + str(
                        maxTimes))
                time.sleep(WHILE_WAIT_SLEEP_LONG)

        log.i(jindu + '  ' + name + '  ' + ' 完成')
        return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)
        # 归档_切换账簿(driver)
        log.exception('归档异常', r.status_code)
        科目表_切换账簿(driver)




def 归档_切换账簿(driver):
    try:
        site='浪潮'
        # 菜单手动
        retCode, companies, msg =  getMigCompany(site)
        if retCode != 0:
            log.e(msg)

            return
        unFind = 0
        for index in range(len(companies)):
            jindu = str(index) + '/' + str(len(companies))
            name = companies[index].companyName.strip()
            path = config.FILE_DOWNLOAD_COMPANY_LANGCHAOYUN + name + '\\'
            #
            # list = os.listdir(path)
            # for index in range(len(companies)):
            #     log.e(list[index])
            # if path.endswith('*\\'):
            #     path = path.replace('*\\', '\\')
            if not os.path.isdir(path):
                os.mkdir(path)
            if int(companies[index].startYear)>2020 :
                log.i(jindu + '  ' + name + ' 建账年 ' + str(companies[index].startYear) + ' 跳过')
                continue


            allFileExist = False
            for y in range(int(companies[index].startYear), int(companies[index].currentYear) + 1):
                if y > 2020:
                    log.i(jindu + '  ' + name + '  ' + str(y) + ' 跳过')
                    allFileExist = True
                    continue

                fileName = path + '归档管理' + str(y) + '.zip'
                if os.path.exists(fileName):
                    log.i(jindu + '  ' + name + '  ' + str(y) + ' 归档文件已存在')
                    allFileExist = True
                else:
                    allFileExist = False
                    break
            if allFileExist:
                continue

            # 设置 = wait.until(EC.presence_of_element_located((By.ID, 'moreBtn')))
            try:
                findTxt = driver.find_elements_by_class_name('el-input__inner')
                findTxt[0].click()
            except Exception as e:
                r = requests.get(driver.current_url, allow_redirects=False)
                # 归档_切换账簿(driver)
                log.exception('查询企业异常', r.status_code)
                # driver.refresh()
                # time.sleep(ACTION_WAIT_SLEEP_SHORT)

                if('https://vip.eyun' in driver.switch_to.active_element.text):
                    toPage(driver, "https://vip.eyun.cn/eyun3/html/#/")
                    toPage(driver, "https://vip.eyun.cn/eyun3/html/#/gdgl")
                else:
                    toPage(driver, "https://ykj.eyun.cn/eyun3/html/#/")
                    toPage(driver, "https://ykj.eyun.cn/eyun3/html/#/gdgl")
                findTxt[0] = driver.find_elements_by_class_name('el-input__inner')[0]
                findTxt[0].click()
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            findTxt[0].send_keys(name)
            # findTxt.send_keys("北京天泽汇丰建筑工程有限公司濮阳分公司")
            # time.sleep(ACTION_WAIT_SLEEP_SHORT)
            ret = driver.find_elements_by_class_name('el-select-dropdown__item')
            if len(ret) == 0:
                updateMigCompanyGdStatus(name, site,-2,jindu + '  ' + name + '  ' + ' 公司名模糊查询无结果')
                log.e(jindu + '  ' + name + '  ' + ' 公司名模糊查询无结果')
                continue
            match = False
            for i in range(len(ret)):
                # if ret[i].get_attribute("style") =='display: none;':
                #     continue
                if ret[i].text == name:
                    ret[i].click()
                    match = True
                    break

            if not match:
                unFind = unFind + 1
                updateMigCompanyGdStatus(name, site,-2,jindu + '  ' + name + '  ' + ' 公司名模糊查询无结果')
                log.e(jindu + '  ' + name + '  ' + ' 公司名模糊查询结果无匹配  ' + str(unFind))
                continue
            time.sleep(ACTION_WAIT_SLEEP_SHORT)
            if '/gdgl' not in driver.current_url :

                toPage(driver, driver.current_url+"gdgl")
            years = driver.find_elements_by_class_name("el-tree-node__label")

            for i in range(len(years)):

                if '月' in years[i].text:
                    continue
                if '2021年' in years[i].text:
                    log.i(jindu + '  ' + name + '  ' + years[i].text + ' 跳过--')
                    continue
                fileName = path + '归档管理' + years[i].text.replace('年','') + '.zip'
                if os.path.exists(fileName):
                    log.i(jindu + '  ' + name + '  ' + str(y) + ' 归档文件已存在')
                    continue
                years[i].click()
                归档按钮=driver.find_elements_by_class_name("el-button--primary")
                for j in range(len(归档按钮)):
                    if '归档' == 归档按钮[j].text:
                        归档按钮[j].click()
                        break
                log.i(jindu + '  ' + name + '  ' + years[i].text + '归档 ')
                maxTimes = int(DOWNLOAD_TIMEOUT / WHILE_WAIT_SLEEP_LONG)
                times = 0
                timeOut=False
                while (times < maxTimes):

                    文件=driver.find_elements_by_class_name("el-table__row")
                    if len(文件)==4 and driver.find_elements_by_class_name('el-button--default')[2].text=='EXCEL下载':
                        log.i(jindu + '  ' + name + '  ' + years[i].text + '归档完成')
                        break
                    times = times + 1
                    if times == maxTimes:
                        log.e(name + years[i].text + '归档等待 超时')
                        # updateMigCompanyGdStatus(name, site,-2,name + years[i].text + '归档等待 超时')
                        timeOut=True
                        break
                    else:
                        log.d(jindu + '  ' + name + '  ' + years[i].text + '归档等待  ' + str(times) + '/' + str(maxTimes))
                    time.sleep(WHILE_WAIT_SLEEP_LONG)
                    years[i].click()
                if timeOut:
                    break
                del_file(config.FILE_DOWNLOAD)
                time.sleep(ACTION_WAIT_SLEEP_SHORT)
                下载Excel = driver.find_elements_by_class_name('el-button--default')

                下载Excel[2].click()

                maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
                times = 0
                while (times < maxTimes):
                    list = os.listdir(config.FILE_DOWNLOAD)
                    if len(list) > 0 and list[0].endswith('.zip'):
                        log.i(jindu + '  ' + name + ' 下载Excel完成 复制')
                        os.rename(config.FILE_DOWNLOAD + "\\" + list[0],
                                  path + list[0])
                        log.i(jindu + '  ' + name + ' 复制完成')
                        break
                    times = times + 1
                    if times == maxTimes:
                        log.e(name + '文件下载等待 超时')
                        break
                    else:
                        log.d(jindu + '  ' + name + '文件下载等待  ' + str(times) + '/' + str(
                            maxTimes))
                    time.sleep(WHILE_WAIT_SLEEP_LONG)

            log.i(jindu + '  ' + name + '  ' + ' 完成')
        return 0
    except BaseException as e:
        r = requests.get(driver.current_url, allow_redirects=False)
        # 归档_切换账簿(driver)
        log.exception('归档异常', r.status_code)
        归档_切换账簿(driver)

if __name__ == "__main__":
    print('main')
    if not os.path.isdir(config.FILE_DOWNLOAD):
        os.mkdir(config.FILE_DOWNLOAD)
    if not os.path.isdir(config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG):
        os.mkdir(config.FILE_DOWNLOAD_COMPANY_YIDAIZHANG)
    # else:
    #     del_file(config.FILE_DOWNLOAD_COMPANY, True)
    #     os.mkdir(config.FILE_DOWNLOAD_COMPANY)
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    prefs = {
        'profile.default_content_settings.popups': 0,
        'download.default_directory': config.FILE_DOWNLOAD
    }

    option.add_experimental_option('prefs', prefs)
    log.i('不显示界面')
    # option.add_argument('--headless')
    # option.add_argument('--disable-gpu')
    # 指定驱动
    driver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(driver_path, options=option)
    # driver = webdriver.Chrome(options=option)
    driver.set_window_size(window_size_w, window_size_h)
    driver.implicitly_wait(5)
    # 合肥账号是13965692190，密码是568565
    # 明光公司的易代账主管账号18815502801密码lym123456
    # 合肥/池州 账号 13965692190 密码 568565

    ret = login(driver, '13213930109', '123abc')
    # ret = login(driver, 'maolianlian@56hui.com', '111111')
    loginName = '合肥池州'
    if (ret != 0):
        time.sleep(60)
        print(' 登陆失败')
    if (ret == 0):
        driver.refresh()
        time.sleep(ACTION_WAIT_SLEEP_LONG)

        ret = 归档_切换账簿(driver)
        if (ret != 0):
            log.e('遍历账簿失败', ret)
            time.sleep(60)
    # if (ret == 0):
    #     ret = getBalance(driver)
    #     if (ret != 0):
    #         log.e('反结账失败', ret)
    #         time.sleep(60)
    log.e('测试完成')
    time.sleep(5)
    driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
