import os
import configparser

# 获取文件的当前路径（绝对路径）
from operator import eq

# cur_path = os.path.dirname(os.path.realpath(__file__))
#
# # 获取config.ini的路径
# config_path = os.path.join(cur_path, 'conf.ini')
#
# conf = configparser.ConfigParser()
# conf.read(config_path)
#
# global fileRoot
# fileRoot = conf.get('local', 'fileRoot')
#
# configRoot = conf.get('local', 'configRoot')
# domain = conf.get('service', 'domain')
# debug = eq(conf.get('local', 'debug'), '1')
#
# dbHost = conf.get('db', 'host')
# dbPort = int(conf.get('db', 'port'))
# dbUser = conf.get('db', 'user')
# dbPasswd = conf.get('db', 'passwd')
# dbPlatform = conf.get('db', 'dbPlatform')
from tools import log, excelTools


# dateFormat = "%Y-%m-%d  %H:%M:%S"
dateFormat = "%H:%M:%S"



SHOW_UI_FALSE='0'
SHOW_UI_TRUE='1'

global showUI
showUI = SHOW_UI_TRUE
def set_showUI(value):
    global showUI
    showUI = value

RUN_WITH_UNKNOW='0'
RUN_WITH_PYCHARM='1'
RUN_WITH_CMD='2'


global userName
userName = str
def set_userName(value):
    global userName
    userName = value


global userPwd
userPwd = str

def set_userPwd(value):
    global userPwd
    userPwd = value

global caseCompanyName
caseCompanyName = str
def set_caseCompanyName(value):
    global caseCompanyName
    caseCompanyName = value

global caseTaxId
caseTaxId = str
def set_caseTaxId(value):
    global caseTaxId
    caseTaxId = value

global caseCurrentAccountMonth
caseCurrentAccountMonth = int
def set_caseCurrentAccountMonth(value):
    global caseCurrentAccountMonth
    caseCurrentAccountMonth = value

global caseCurrentAccountYear
caseCurrentAccountYear =int
def set_caseCurrentAccountYear(value):
    global caseCurrentAccountYear
    caseCurrentAccountYear = value


global runWith
runWith = RUN_WITH_PYCHARM
def set_runWith(value):
    global runWith
    runWith = value


    global dateFormat
    if runWith == RUN_WITH_CMD:
        dateFormat = "%Y-%m-%d  %H:%M:%S"



domain = str
domain_cs_info=str
dbHost = str
dbPort = int
dbUser = str
dbPasswd =str
dbPlatform =str
dbLog =str

HOST_SOURCE_PRE='pre'
HOST_SOURCE_ON_LINE= 'online'
FILE_DOWNLOAD='d:\\seleniumTemp\\download'
hostSource = None
def set_host(host):
    global domain
    global domain_cs_info
    global dbHost
    global dbPort
    global dbUser
    global dbPasswd
    global dbPlatform
    global dbLog
    global hostSource
    if host==HOST_SOURCE_ON_LINE:
        hostSource= 'online'
        log.i('设置环境参数-生产环境')
        domain = 'http://sstax.cn:1000/'
        dbHost = '222.73.99.99'
        dbPort = 3030
        dbUser = 'csdb'
        dbPasswd = 'Pwd!2018@db'
        dbPlatform = 'cs_platform'
        dbLog = 'cs-log'
    elif host==HOST_SOURCE_PRE:

        hostSource= 'pre'
        log.i('设置环境参数-预发布环境')
        # domain = 'http://pre.sstax.cn:81/'
        domain = 'http://learn.sstax.cn:81/'
        domain_cs_info = 'http://learn.sstax.cn:81/'
        dbHost = '222.73.99.99'
        dbPort = 3031
        dbUser = 'precsdb'
        dbPasswd = 'Pwd2018db'
        dbPlatform = 'pre_cs_platform'

        dbLog = 'pre-cs-log'
    else:
        log.w('未设置环境参数 ')

        hostSource = None



WHILE_WAIT_SLEEP = 0.1
ACTION_WAIT_SLEEP_SHORT = 0.3
ACTION_WAIT_SLEEP_LONG = 1
LOAD_PAGE_TIMEOUT = 10
FAIL_WAIT_SLEEP=20

window_size_w = 1400
window_size_h = 900

current_x = 0
current_y = 0
excelTools.read_CompanyInfo()