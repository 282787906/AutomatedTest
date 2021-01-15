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
HOST_SOURCE_ON_XI_AN= 'xiAn'
HOST_SOURCE_ON_YUN_NAN= 'yunNan'
HOST_SOURCE_ON_NAN_CHANG= 'nanChang'
HOST_SOURCE_ON_JIN_KAI_QU= 'jinKaiQu'
FILE_DOWNLOAD='d:\\seleniumTemp\\download'
FILE_DOWNLOAD_COMPANY='D:\\seleniumTemp\\归档_众网\\'


hostSource = None
def set_host(host):
    global domain
    global domain_cs_info
    global domain_api
    global dbHost
    global dbPort
    global dbUser
    global dbPasswd
    global dbPlatform
    global dbLog
    global hostSource
    hostSource = host
    if host==HOST_SOURCE_ON_LINE:

        log.i('设置环境参数-生产环境')
        domain = 'http://sstax.cn:1000/'

        domain_cs_info = 'http://sstax.cn:1000/'
        domain_api = 'http://sstax.cn:1000/'
        dbHost = '222.73.99.99'
        dbPort = 3030
        dbUser = 'csdb'
        dbPasswd = 'Pwd!2018@db'
        dbPlatform = 'cs_platform'
        dbLog = 'cs-log'
    elif host==HOST_SOURCE_PRE:


        log.i('设置环境参数-预发布环境')
        # domain = 'http://pre.sstax.cn:81/'
        # domain = 'http://61.153.190.93:18080'
        # domain_cs_info = 'http://61.153.190.93:18080'
        # domain_cs_info = 'pre.sstax.cn:81'
        domain = 'http://101.89.137.10:48080'
        domain_cs_info = 'http://101.89.137.10:48080'
        # domain_api = 'http://pre.sstax.cn:81'
        domain_api = 'http://sstax.cn:1000/'
        dbHost = '222.73.99.99'
        dbPort = 3031
        dbUser = 'precsdb'
        dbPasswd = 'Pwd2018db'
        dbPlatform = 'pre_cs_platform'

        dbLog = 'pre-cs-log'
    elif host == HOST_SOURCE_ON_XI_AN:


        log.i('设置环境参数-西安环境')
        domain = 'http://101.89.137.10:48080'
        domain_cs_info = 'http://101.89.137.10:48080'
        # domain_api = 'http://pre.sstax.cn:81'
        domain_api = 'http://sstax.cn:1000/'
        dbHost = '222.73.99.99'
        dbPort = 3031
        dbUser = 'precsdb'
        dbPasswd = 'Pwd2018db'
        dbPlatform = 'pre_cs_platform'

        dbLog = 'pre-cs-log'
    elif host == HOST_SOURCE_ON_YUN_NAN:

        log.i('设置环境参数-云南环境')
        domain = 'http://61.153.190.93:18080'
        domain_cs_info = 'http://61.153.190.93:18080'
        domain_api = 'http://61.153.190.93:18080/'
        dbHost = '222.73.99.99'
        dbPort = 3031
        dbUser = 'precsdb'
        dbPasswd = 'Pwd2018db'
        dbPlatform = 'pre_cs_platform'
        dbLog = 'pre-cs-log'
    elif host == HOST_SOURCE_ON_JIN_KAI_QU:

        log.i('设置环境参数-金开区环境')
        domain = 'http://101.91.230.16:28080'
        domain_cs_info = 'http://101.91.230.16:28080'
        domain_api = 'http://101.91.230.16:28080/'
        dbHost = '222.73.99.99'
        dbPort = 3031
        dbUser = 'precsdb'
        dbPasswd = 'Pwd2018db'
        dbPlatform = 'pre_cs_platform'
        dbLog = 'pre-cs-log'
    elif host == HOST_SOURCE_ON_NAN_CHANG:

        log.i('设置环境参数-南昌环境')
        domain = 'http://183.134.73.180:18080'
        domain_cs_info ='http://183.134.73.180:18080'
        domain_api = 'http://183.134.73.180:18080'
        dbHost = '222.73.99.99'
        dbPort = 3031
        dbUser = 'precsdb'
        dbPasswd = 'Pwd2018db'
        dbPlatform = 'pre_cs_platform'
        dbLog = 'pre-cs-log'
    else:
        log.w('未设置环境参数 ')

        hostSource = None
    dbHost = '222.73.99.99'
    dbPort = 3030
    dbUser = 'csdb'
    dbPasswd = 'Pwd!2018@db'
    dbPlatform = 'fs-admin'
    dbLog = 'cs-log'


WHILE_WAIT_SLEEP = 0.1
WHILE_WAIT_SLEEP_LONG= 1
ACTION_WAIT_SLEEP_SHORT = 0.3
ACTION_WAIT_SLEEP_LONG = 1
LOAD_PAGE_TIMEOUT = 10
DOWNLOAD_TIMEOUT = 90
FAIL_WAIT_SLEEP=20

window_size_w = 1400
window_size_h = 900

current_x = 0
current_y = 0
# excelTools.read_CompanyInfo()