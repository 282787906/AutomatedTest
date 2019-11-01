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

global runInPycharm
runInPycharm = 1
def set_runInPycharm( value):
    global runInPycharm
    runInPycharm = value

def get_runInPycharm():
    return runInPycharm


# domain = 'http://pre.sstax.cn:81/'
# dbHost = '222.73.99.99'
# dbPort = 3031
# dbUser = 'precsdb'
# dbPasswd = 'Pwd2018db'
# dbPlatform = 'pre_cs_platform'

domain = 'http://sstax.cn:1000/'
dbHost = '222.73.99.99'
dbPort = 3030
dbUser = 'csdb'
dbPasswd = 'Pwd!2018@db'
dbPlatform = 'cs_platform'


WHILE_WAIT_SLEEP = 0.2
ACTION_WAIT_SLEEP_SHORT = 0.2
ACTION_WAIT_SLEEP_LONG = 0.3
LOAD_PAGE_TIMEOUT = 10
FAIL_WAIT_SLEEP=20

window_size_w = 1400
window_size_h = 900

current_x = 0
current_y = 0