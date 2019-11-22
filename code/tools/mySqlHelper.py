import threading
import time
import traceback

import pymysql

from conf import config


# def getFileTemp():
#     try:
#         conn = pymysql.connect(host=config.dbHost,
#                                port=config.dbPort,
#                                user=config.dbUser,
#                                passwd=config.dbPasswd,
#                                db=config.dbPlatform,
#                                charset='utf8')
#     except:
#
#         log.exception('数据库连接异常')
#         return -1, None, '数据库连接异常 '
#
#     try:
#         # 使用 cursor() 方法创建一个游标对象 cursor
#         cursor = conn.cursor()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         # 使用 execute()  方法执行 SQL 查询
#         sql = 'SELECT *  FROM file_temp f WHERE id>3128641 AND (f.type=1 OR f.type=2)  ORDER BY id ASC LIMIT 1000'
#         sql = 'SELECT *  FROM file_temp f WHERE id>3130600 AND  f.type=2 and hh_flag=2  ORDER BY id ASC LIMIT 750'
#         # sql='SELECT *  FROM file_temp f WHERE id>3130600 AND  f.type=2 AND hh_flag=2 AND hh_ret LIKE \'%{"result":"1","name":"invoiceMethod","type":0}%\'  ORDER BY id ASC LIMIT 100'
#         cursor.execute(sql)
#
#         data = []
#         for row in cursor.fetchall():
#             path = row["name"]
#             hhFlag = row["hh_flag"]
#             uid = row["uid"]
#             type = row["type"]
#             fileId = row["file_id"]
#             config.domain
#             # print("hhFlag:", hhFlag, "    path:", config.domain + path)
#             model = fileTemp(uid, fileId, path, type, hhFlag)
#             data.append(model)
#         return 0, data, None
#     except:
#         log.exception('数据库查询异常')
#         return -2, None, '数据库查询异常'
#     finally:
#         # 关闭数据库连接
#         conn.close()
from module.Template import Template
from tools import log


def getTemplateSubjectById(id):
    try:
        conn = pymysql.connect(host=config.dbHost,
                               port=config.dbPort,
                               user=config.dbUser,
                               passwd=config.dbPasswd,
                               db=config.dbPlatform,
                               charset='utf8')
    except:

        log.exception('数据库连接异常')
        return -1, None, '数据库连接异常 '

    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 使用 execute()  方法执行 SQL 查询
        sql = 'SELECT t.`ID` tId,t.`NAME` tName,t.`SUBJECT_TYPE` subjectType, ts.`ID` tsId,ts.`NAME` tsName,ts.`SUBJECT_ID` kmCode,ts.`SUBJECT_NAME` kmName,ts.`TYPE` jdType  ' \
              'FROM `template` t,template_subject ts ' \
              'WHERE ts.`DELETE_FLAG`=1 AND t.`DELETE_FLAG`=1  AND ts.`TEMPLATE_ID`=t.`ID` AND t.`ID`='+str(id)

        cursor.execute(sql)

        data = []
        for row in cursor.fetchall():
            tId = row["tId"]
            tName = row["tName"]
            tsId = row["tsId"]
            subjectType = row["subjectType"]
            tsName = row["tsName"]
            kmCode = row["kmCode"]
            kmName = row["kmName"]
            jdType = row["jdType"]
            config.domain

            model = Template(tId, tName, subjectType,tsId, tsName, kmCode, kmName, jdType)
            data.append(model)
        return 0, data, None
    except:
        log.exception('数据库查询异常')
        return -2, None, '数据库查询异常'
    finally:
        # 关闭数据库连接
        conn.close()


# def getInfoMapping():
#     try:
#         conn = pymysql.connect(host=config.dbHost,
#                                port=config.dbPort,
#                                user=config.dbUser,
#                                passwd=config.dbPasswd,
#                                db=config.dbPlatform,
#                                charset='utf8')
#     except:
#
#         log.exception('数据库连接异常:' )
#
#         return -1, None, '数据库连接异常 '
#
#     try:
#         # 使用 cursor() 方法创建一个游标对象 cursor
#         cursor = conn.cursor()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         # 使用 execute()  方法执行 SQL 查询
#         sql = 'SELECT * FROM `info_template_mapping` itm WHERE itm.`org_id`=6 OR itm.`org_id`=1 AND itm.`ID` >668 ORDER BY itm.`ID`'
#         cursor.execute(sql)
#
#         data = []
#         for row in cursor.fetchall():
#             id = row["id"]
#             template_id = row["template_id"]
#             mapping = row["mapping"]
#
#             model = infoTemplateMapping(id, template_id, mapping)
#             data.append(model)
#         return 0, data, None
#     except:
#         log.exception('数据库查询异常' )
#         return -2, None, '数据库查询异常'
#     finally:
#         # 关闭数据库连接
#         conn.close()


# def getSubjectByTemplateId(id):
#     try:
#         conn = pymysql.connect(host=config.dbHost,
#                                port=config.dbPort,
#                                user=config.dbUser,
#                                passwd=config.dbPasswd,
#                                db=config.dbPlatform,
#                                charset='utf8')
#     except:
#
#         print('数据库连接异常:', traceback._context_message)
#         traceback.print_exc()
#         return -1, None, '数据库连接异常 '
#
#     try:
#         # 使用 cursor() 方法创建一个游标对象 cursor
#         cursor = conn.cursor()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         # 使用 execute()  方法执行 SQL 查询
#         sql = 'SELECT * FROM `template_subject` ts WHERE ts.`DELETE_FLAG`=1 AND ts.`TEMPLATE_ID`=' + str(id)
#         cursor.execute(sql)
#
#         data = []
#         for row in cursor.fetchall():
#             id = row["ID"]
#             SUBJECT_CODE = row["SUBJECT_CODE"]
#
#             model = templateSubject(id, SUBJECT_CODE)
#             data.append(model)
#         return 0, data, None
#     except:
#         traceback.print_exc()
#
#         print('数据库查询异常:', traceback._context_message)
#         return -2, None, '数据库查询异常'
#     finally:
#         # 关闭数据库连接
#         conn.close()


# def updataNewTemplateMapping(id, mapping):
#     try:
#         conn = pymysql.connect(host=config.dbHost,
#                                port=config.dbPort,
#                                user=config.dbUser,
#                                passwd=config.dbPasswd,
#                                db=config.dbPlatform,
#                                charset='utf8')
#     except:
#
#         print('数据库连接异常:', traceback._context_message)
#         traceback.print_exc()
#         return -1, '数据库连接异常 '
#
#     try:
#         # 使用 cursor() 方法创建一个游标对象 cursor
#         cursor = conn.cursor()
#
#         # 使用 execute()  方法执行 SQL 查询
#         sql = "UPDATE `info_template_mapping` SET mapping='" + mapping + "' WHERE id=" + str(id)
#         cursor.execute(sql)
#         # 提交到数据库执行
#         conn.commit()
#
#         return 0, None
#     except:
#         conn.rollback()
#         traceback.print_exc()
#
#         print('数据库查询异常:', traceback._context_message)
#         return -2, '数据库查询异常'
#     finally:
#         # 关闭数据库连接
#         conn.close()


# # 发现文件被录入时更新临时表状态 主库
# #
# def updataFileTempWhenInputed(uid):
#     try:
#         conn = pymysql.connect(host=config.dbHost, port=config.dbPort, user=config.dbUser,
#                                passwd=config.dbPasswd, db=config.dbPlatform, charset='utf8')
#     except:
#         traceback.print_exc()
#         return -1
#
#     try:
#         # 使用 cursor() 方法创建一个游标对象 cursor
#         cursor = conn.cursor()
#         # 使用 execute()  方法执行 SQL 查询
#         sql = "UPDATE file_management f,file_temp t SET t.status=5 WHERE f.id=t.file_id AND t.uid=%s AND f.file_status=2"
#         cursor.execute(sql, uid)
#
#     except:
#         traceback.print_exc()
#         return -2
#     finally:
#         # 关闭数据库连接
#         conn.close()


def getThirdLog(id):

    try:
        conn = pymysql.connect(host=config.dbHost,
                               port=config.dbPort,
                               user=config.dbUser,
                               passwd=config.dbPasswd,
                               db=config.dbLog,
                               charset='utf8')
    except:

        print('数据库连接异常:', traceback._context_message)
        traceback.print_exc()
        return -1, None, None,  '数据库连接异常 '

    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 使用 execute()  方法执行 SQL 查询
        sql = "SELECT * FROM  cs_third_log  l WHERE l.id="+str(id)
        cursor.execute(sql)
        for row in cursor.fetchall():

            # print('数据库查:',row["id"])
            # print('数据库查:',row["af"])
            # print('数据库查:',row["bf"])
            af=row["af"]
            bf=row["bf"]
            return 0, str(af, encoding = "utf8"),str(bf, encoding = "utf8"),None
    except:
        traceback.print_exc()

        print('数据库查询异常:', traceback._context_message)
        return -2, None,None,  '数据库查询异常'
    finally:
        # 关闭数据库连接
        conn.close()


def updateTest():
    try:

        conn = pymysql.connect(host="192.168.1.10",
                               port=3307,
                               user="root",
                               passwd="d0608",
                               db="csdb20170913153728181",
                               charset='utf8')
    except:
        traceback.print_exc()
        return

    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()
        # 使用 execute()  方法执行 SQL 查询

        sql = "UPDATE file_management set original_info ='567567567',status = 3 WHERE ID = 5"
        intRet = cursor.execute(sql)
        conn.commit()
        print("intRet", intRet)
    except:
        traceback.print_exc()
        return
    finally:
        # 关闭数据库连接
        conn.close()


# return returnCode
# max_connections
# processCount
# msg
def getConnStatus(connConfig):
    try:
        conn = pymysql.connect(host=connConfig.dbHost,
                               port=connConfig.dbPort,
                               user=connConfig.dbUser,
                               passwd=connConfig.dbPasswd,
                               db=connConfig.dbPlatform,
                               charset='utf8')
    except BaseException  as e:


        log.e('数据库连接异常:',e, traceback._context_message)
        traceback.print_exc()
        return -1, None, None, '数据库连接异常 '

    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 使用 execute()  方法执行 SQL 查询
        sql = "SHOW VARIABLES LIKE '%max_connections%'"
        cursor.execute(sql)
        for row in cursor.fetchall():
            if row["Variable_name"] == 'max_connections':
                max_connections = row["Value"]
                break
        sql = "SHOW PROCESSLIST"
        cursor.execute(sql)
        processCount = 0
        for row in cursor.fetchall():
            processCount = processCount + 1

        return 0, int(max_connections),processCount,None
    except:
        traceback.print_exc()

        log.e('数据库查询异常:', traceback._context_message)
        return -2, None, None, '数据库查询异常'
    finally:
        # 关闭数据库连接
        conn.close()

def getUnPdfCount():
    try:
        conn = pymysql.connect(host=config.dbHost,
                               port=config.dbPort,
                               user=config.dbUser,
                               passwd=config.dbPasswd,
                               db=config.dbPlatform,
                               charset='utf8')
    except:

        print('数据库连接异常:', traceback._context_message)
        traceback.print_exc()
        return -1, None,  '数据库连接异常 '

    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 使用 execute()  方法执行 SQL 查询
        sql = "SELECT COUNT(*) count FROM `monthly_temp`"
        cursor.execute(sql)
        for row in cursor.fetchall():
            count = row["count"]


        return 0, count,None
    except:
        traceback.print_exc()

        print('数据库查询异常:', traceback._context_message)
        return -2, None,  '数据库查询异常'
    finally:
        # 关闭数据库连接
        conn.close()


def getUnHeHeCount():
    try:
        conn = pymysql.connect(host=config.dbHost,
                               port=config.dbPort,
                               user=config.dbUser,
                               passwd=config.dbPasswd,
                               db=config.dbPlatform,
                               charset='utf8')
    except:

        print('数据库连接异常:', traceback._context_message)
        traceback.print_exc()
        return -1, None,  '数据库连接异常 '

    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 使用 execute()  方法执行 SQL 查询
        sql = "SELECT COUNT(*) count FROM `file_temp` f WHERE (f.type=1 OR f.type=2  ) AND f.`hh_flag`=1"
        cursor.execute(sql)
        count = 0
        for row in cursor.fetchall():
            count = row["count"]


        return 0, count,None
    except:
        traceback.print_exc()

        print('数据库查询异常:', traceback._context_message)
        return -2, None,  '数据库查询异常'
    finally:
        # 关闭数据库连接
        conn.close()


def getUnHeHeWaitTime():
    try:
        conn = pymysql.connect(host=config.dbHost,
                               port=config.dbPort,
                               user=config.dbUser,
                               passwd=config.dbPasswd,
                               db=config.dbPlatform,
                               charset='utf8')
    except:

        print('数据库连接异常:', traceback._context_message)
        traceback.print_exc()
        return -1, None,  '数据库连接异常 '

    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 使用 execute()  方法执行 SQL 查询
        sql = "SELECT   TIMESTAMPDIFF(MINUTE, f.`time`,NOW()) dt, f.* FROM `file_temp` f WHERE (f.type = 1 OR f.type = 2 ) AND f.`hh_flag` = 1 ORDER BY id LIMIT 1"
        cursor.execute(sql)
        minutes=0
        for row in cursor.fetchall():
            minutes = row["dt"]


        return 0, minutes,None
    except:
        traceback.print_exc()

        print('数据库查询异常:', traceback._context_message)
        return -2, None,  '数据库查询异常'
    finally:
        # 关闭数据库连接
        conn.close()

# 生成凭证等待
def getUnCreateWaitTime():
    try:
        conn = pymysql.connect(host=config.dbHost,
                               port=config.dbPort,
                               user=config.dbUser,
                               passwd=config.dbPasswd,
                               db=config.dbPlatform,
                               charset='utf8')
    except:

        print('数据库连接异常:', traceback._context_message)
        traceback.print_exc()
        return -1, None,  '数据库连接异常 '

    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 使用 execute()  方法执行 SQL 查询
        sql = "SELECT   TIMESTAMPDIFF(MINUTE, f.`time`,NOW()) dt, f.* FROM `file_temp` f " \
              "WHERE (f.type = 1 OR f.type = 2) AND f.`hh_flag` = 2 AND f.`auto_flg` IS NULL AND " \
              "f.`uid` IN  (SELECT uid FROM `fun_ext` k WHERE k. TYPE=1 AND k.`fun`=3) ORDER BY id LIMIT 1 ;"
        cursor.execute(sql)
        minutes=0
        for row in cursor.fetchall():
            minutes = row["dt"]


        return 0, minutes,None
    except:
        traceback.print_exc()

        print('数据库查询异常:', traceback._context_message)
        return -2, None,  '数据库查询异常'
    finally:
        # 关闭数据库连接
        conn.close()
if __name__ == "__main__":
    # index = 0
    # map = getSubMap()
    # getFileTemp(map)

    # # 字典遍历
    # for key in map.keys():
    #     print(key, ":", map[key])

    # 连接测试
    # index = 0
    # timer = threading.Timer(1, connTestSub)
    # timer.start()
    getConnStatus()
