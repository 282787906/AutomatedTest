import os
import sys
from datetime import datetime
import time

from conf import config
from module.connConfig import connConfig
from tools import log, mySqlHelper, mail


def checkConn(rate):
    dataConn = []

    dataConn.append(connConfig("主库", config.dbHost, config.dbPort, config.dbUser, config.dbPasswd, config.dbPlatform))
    dataConn.append(connConfig("分库1", config.dbHost, 3122, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库2", config.dbHost, 3123, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库3", config.dbHost, 3124, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库4", config.dbHost, 3125, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库5", config.dbHost, 3126, config.dbUser, "Pwd2018db", ""))
    dataConn.append(connConfig("分库6", config.dbHost, 30127, config.dbUser, "Pwd2018db", ""))
    warnMsg = ''
    retCode = 0;
    for conn in dataConn:
        code, max, count, msg = mySqlHelper.getConnStatus(conn)
        # print(msg)
        if code != 0:
            warnMsg = warnMsg + msg + '\n'
            retCode = 1
            break
        useRate = round(count / max * 100, 2)
        msg = conn.dbName + "\t最大连接数:" + str(max) + '\t当前连接数:' + str(count) + '\t使用率:' + str(useRate) + '%'
        if useRate > rate:
            retCode = 1
        warnMsg = warnMsg + msg + '\n'


    return retCode, warnMsg
def run():
    CONN_RATE_THRESHOLD = 50               # 数据库连接使用率（%）50
    CREATE_PZ_WAIT_COUNT_THRESHOLD = 20     # 自动创建凭证积压时间（分钟）20
    HE_HE_WAIT_TIME_THRESHOLD = 120          # 合合识别积压时间（分钟）120
    PDF_WAIT_THRESHOLD = 30                 # 凭证生成pdf等待数量（分钟）30
    SLEEP = 30                             # 执行周期（秒）300
    while True:
        mailMsg = ''
        hour = datetime.now().hour
        if hour > 6 and hour < 21:

            log.i('数据库状态监控')
            try:
                retCode, warnMsg = checkConn(CONN_RATE_THRESHOLD)
                if retCode != 0:
                    # log.w(warnMsg)
                    mailMsg = mailMsg + warnMsg + '\n'
                else:

                    log.d(warnMsg)
                retCode, minutes, msg = mySqlHelper.getUnCreateWaitTime()
                if retCode != 0:
                    mailMsg = mailMsg + '自动生成凭证等待查询出错 :' + msg + '\n'
                elif retCode == 0 and minutes > CREATE_PZ_WAIT_COUNT_THRESHOLD:

                    mailMsg = mailMsg + "自动生成凭证等待时间：" + str(minutes) + '分钟\n'
                else:
                    log.d("自动生成凭证等待时间：" + str(minutes) + '分钟')

                retCode, minutes, msg =mySqlHelper. getUnHeHeWaitTime()
                if retCode != 0:
                    mailMsg = mailMsg + '合合识别积压查询出错 :' + msg + '\n'
                elif retCode == 0 and minutes > HE_HE_WAIT_TIME_THRESHOLD:
                    mailMsg = mailMsg + "合合识别积压时间：" + str(minutes) + '分钟\n'
                else:
                    log.d("合合识别积压时间：" + str(minutes) + '分钟')

                retCode, count, msg = mySqlHelper.getUnPdfCount()
                if retCode != 0:
                    # log.w(warnMsg)
                    mailMsg = mailMsg + '凭证生成pdf积压查询出错 :' + msg + '\n'
                elif retCode == 0 and count > PDF_WAIT_THRESHOLD:
                    log.w('pdfCount:', count)
                    mailMsg = mailMsg + "凭证生成pdf积压" + str(count) + '\n'
                else:
                    log.d("凭证生成pdf积压" + str(count) )
                # retCode, msg = loadByHeaders('20171009-102958-845')
                # if retCode != 200:
                #     log.w('status_code:', retCode, 'msg:', msg)
                #     mailMsg = mailMsg + "third调用 code:" + str(retCode) + "  " + msg + '\n'
                if len(mailMsg) > 0:
                    # mail.send("财税警告", mailMsg)
                    log.e("财税警告", mailMsg)
                else:
                    log.i('状态正常\n')
            except BaseException  as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                log.e('状态监控异常', e.args)

        time.sleep(SLEEP)

if __name__ == "__main__":
    print('DbMonitor')
    run()