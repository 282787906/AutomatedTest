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
from tools import log


RUN_WITH_UNKNOW=0
RUN_WITH_PYCHARM=1
RUN_WITH_CMD=2

global runWith
runWith = 1
def set_runWith(value):
    global runWith
    runWith = value


domain = str
dbHost = str
dbPort = int
dbUser = str
dbPasswd =str
dbPlatform =str
hostSource = None
def set_Host(host):
    global domain
    global dbHost
    global dbPort
    global dbUser
    global dbPasswd
    global dbPlatform
    global hostSource
    if host=='online':
        hostSource= 'online'
        log.i('设置环境参数-生产环境')
        domain = 'http://sstax.cn:1000/'
        dbHost = '222.73.99.99'
        dbPort = 3030
        dbUser = 'csdb'
        dbPasswd = 'Pwd!2018@db'
        dbPlatform = 'cs_platform'
    elif host=='pre':

        hostSource= 'pre'
        log.i('设置环境参数-预发布环境')
        domain = 'http://pre.sstax.cn:81/'
        dbHost = '222.73.99.99'
        dbPort = 3031
        dbUser = 'precsdb'
        dbPasswd = 'Pwd2018db'
        dbPlatform = 'pre_cs_platform'
    else:
        log.w('未设置环境参数 ')

        hostSource = None


# domain = 'http://sstax.cn:1000/'
# dbHost = '222.73.99.99'
# dbPort = 3030
# dbUser = 'csdb'
# dbPasswd = 'Pwd!2018@db'
# dbPlatform = 'cs_platform'


WHILE_WAIT_SLEEP = 0.2
ACTION_WAIT_SLEEP_SHORT = 0.2
ACTION_WAIT_SLEEP_LONG = 0.3
LOAD_PAGE_TIMEOUT = 10
FAIL_WAIT_SLEEP=20

window_size_w = 1400
window_size_h = 900

current_x = 0
current_y = 0