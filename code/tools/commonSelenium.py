

import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from conf import config
from conf.config import LOAD_PAGE_TIMEOUT, WHILE_WAIT_SLEEP, ACTION_WAIT_SLEEP_SHORT
from tools import log


def printLocation(element):
    log.d('location',element.location,'size', element.size)

def toPage(driver, url):
    """
    :param driver: aaa
    :param url:ddd
    :return: 0 跳转成功
    """

    if (driver.current_url == url):
        return 0
    driver.get(url)
    times = 0
    maxTimes = int(LOAD_PAGE_TIMEOUT / WHILE_WAIT_SLEEP)
    while (times < maxTimes):
        if (driver.current_url == url):
            return 0
        times = times + 1

        log.d('页面加载等待', maxTimes, times)
        time.sleep(WHILE_WAIT_SLEEP)
    log.e('页面加载超时', url)
    return 1

def mouseLeftClick(_driver, x, y):
    global current_x
    offset_x = x - current_x
    current_x = x;
    global current_y
    offset_y = y - current_y
    current_y = y

    # log.d('鼠标左键点击', x, y, offset_x, offset_y)
    ActionChains(_driver).move_by_offset(offset_x, offset_y).click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标 多次使用时偏移累加


def mouseLeftDoubleClick(_driver, x, y):
    current_x=config.current_x
    offset_x = x - current_x
    config.current_x = x;
    current_y=config.current_y
    offset_y = y - current_y
    config.current_y = y

    # log.d('鼠标左键双击', x, y, offset_x, offset_y)
    ActionChains(_driver).move_by_offset(offset_x,
                                         offset_y).double_click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标 多次使用时偏移累加


def mouseLocationReset(_driver):
    global current_x
    offset_x = 0 - current_x
    current_x = 0;
    global current_y
    offset_y = 0 - current_y
    current_y = 0

    log.d('mouseLocationReset', offset_x, offset_y)
    ActionChains(_driver).move_by_offset(current_x, current_y).perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标


def mouseRightClick(_driver, x, y):
    global current_x
    offset_x = x - current_x
    current_x = x;
    global current_y
    offset_y = y - current_y
    current_y = y

    log.d('鼠标右键点击', x, y, offset_x, offset_y)
    ActionChains(_driver).move_by_offset(current_x, current_y).context_click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标


def clearElement(element):
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.DELETE)

