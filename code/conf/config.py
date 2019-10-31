import os
import configparser

# 获取文件的当前路径（绝对路径）
from operator import eq

cur_path = os.path.dirname(os.path.realpath(__file__))

# 获取config.ini的路径
config_path = os.path.join(cur_path, 'conf.ini')

conf = configparser.ConfigParser()
conf.read(config_path)

global fileRoot
fileRoot = conf.get('local', 'fileRoot')

configRoot = conf.get('local', 'configRoot')
domain = conf.get('service', 'domain')
debug = eq(conf.get('local', 'debug'), '1')

dbHost = conf.get('db', 'host')
dbPort = int(conf.get('db', 'port'))
dbUser = conf.get('db', 'user')
dbPasswd = conf.get('db', 'passwd')
dbPlatform = conf.get('db', 'dbPlatform')


global rootdir
rootdir = fileRoot
global pathTemplateFail
pathTemplateFail = rootdir + '/templateFail/'
global pathOcrFail
pathOcrFail = rootdir + '/ocrFail/'
global pathOcrTaxSuccess
pathOcrTaxSuccess = rootdir + '/ocrTaxSuccess/'
global pathOcrImgCut
pathOcrImgCut = rootdir + '/ocrImgCut/'

global selectLimit
selectLimit = 20

global ocrQr
ocrQr = 1

global mapSub
mapSub = dict()

WHILE_WAIT_SLEEP = 0.2
ACTION_WAIT_SLEEP_SHORT = 0.2
ACTION_WAIT_SLEEP_LONG = 0.3
LOAD_PAGE_TIMEOUT = 10
FAIL_WAIT_SLEEP=20

window_size_w = 1400
window_size_h = 900

current_x = 0
current_y = 0

# offset_qr_top = - 220
# offset_qr_bottom = 0
# offset_qr_left = - 70
# offset_qr_right = + 185
#
# offset_taxCode_top = - 150
# offset_taxCode_bottom = - 100
# offset_taxCode_left = 185
# offset_taxCode_right = 535
#
# offset_taxNO_top = - 200
# offset_taxNO_bottom = - 60
# offset_taxNO_left = 1190
# offset_taxNO_right = 1630



offset_qr_top = - 110
offset_qr_bottom = 0
offset_qr_left = - 15
offset_qr_right = + 100

offset_taxCode_top = - 105
offset_taxCode_bottom = - 65
offset_taxCode_left = 125
offset_taxCode_right = 360

offset_taxNO_top = - 110
offset_taxNO_bottom = - 40
offset_taxNO_left = 810
offset_taxNO_right = 1090
