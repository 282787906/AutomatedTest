import os

import xlrd

from conf import config
from module.DocumentDetailAdd import DocumentDetailAdd
from module.DocumentDetailInput import DocumentDetailInput
from module.SubsidiaryLedger import SubsidiaryLedger
from module.Kemuyueb import Kemuyueb
from tools import log


def read_excel():
    file = 'C:\\Users\\Liqg\\Desktop\\csae_document.xlsx'
    wb = xlrd.open_workbook(filename=file)  # 打开文件
    print(wb.sheet_names())  # 获取所有表格名字

    sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格
    print(sheet1)
    print(sheet1.name, sheet1.nrows, sheet1.ncols)

    rows = sheet1.row_values(2)  # 获取行内容
    cols = sheet1.col_values(3)  # 获取列内容
    print(rows)
    print(cols)

    print(sheet1.cell(1, 0).value)  # 获取表格里的内容，三种方式
    print(sheet1.cell_value(1, 0))
    print(sheet1.row(1)[0].value)


def read_CompanyInfo():
    log.d('读取用例公司信息excel文件')
    dir = os.path.dirname(__file__)
    parent_path = os.path.dirname(dir)
    filename = parent_path + '/testCases/csae_document.xlsx'  # 根据项目所在路径，找到用例所在的相对项目的路径
    wb = xlrd.open_workbook(filename=filename)  # 打开文件
    company_name_index = int
    tax_id_index = int
    current_account_year_index = int
    current_account_month_index = int
    user_name_index = int
    user_pwd_index = int
    host_type_index = int

    sheet1 = wb.sheet_by_name('用例信息')  # 通过索引获取表格
    for index in range(sheet1.ncols):

        if ('company_name' == sheet1.cell_value(0, index)):
            company_name_index = index
        if ('tax_id' == sheet1.cell_value(0, index)):
            tax_id_index = index
        if ('current_account_year' == sheet1.cell_value(0, index)):
            current_account_year_index = index
        if ('current_account_month' == sheet1.cell_value(0, index)):
            current_account_month_index = index
        if ('user_name' == sheet1.cell_value(0, index)):
            user_name_index = index
        if ('user_pwd' == sheet1.cell_value(0, index)):
            user_pwd_index = index
        if ('host_type' == sheet1.cell_value(0, index)):
            host_type_index = index
    company_name = sheet1.cell_value(1, company_name_index)
    tax_id = sheet1.cell_value(1, tax_id_index)
    current_account_year = int(sheet1.cell_value(1, current_account_year_index))
    current_account_month = int(sheet1.cell_value(1, current_account_month_index))
    # user_name = sheet1.cell_value(1, user_name_index)
    ctype = sheet1.cell(1, user_name_index).ctype  # 表格的数据类型
    if ctype == 2 and sheet1.cell_value(1, user_name_index) % 1 == 0:  # 如果是整形
        user_name = int(sheet1.cell_value(1, user_name_index))
    else:
        user_name = sheet1.cell_value(1, user_name_index)

    ctype = sheet1.cell(1, user_pwd_index).ctype  # 表格的数据类型
    if ctype == 2 and sheet1.cell_value(1, user_pwd_index) % 1 == 0:  # 如果是整形
        user_pwd = int(sheet1.cell_value(1, user_pwd_index))
    else:
        user_pwd = sheet1.cell_value(1, user_pwd_index)

    host_type = sheet1.cell_value(1, host_type_index)

    config.set_caseCompanyName(company_name)
    config.set_caseTaxId(tax_id)
    config.set_caseCurrentAccountYear(current_account_year)
    config.set_caseCurrentAccountMonth(current_account_month)
    config.set_host(host_type)
    config.set_userName(user_name)
    config.set_userPwd(user_pwd)
    return 0


def read_documentAdd():
    log.d('读取凭证excel文件')
    dir = os.path.dirname(__file__)
    parent_path = os.path.dirname(dir)
    filename = parent_path + '/testCases/csae_document.xlsx'  # 根据项目所在路径，找到用例所在的相对项目的路径
    wb = xlrd.open_workbook(filename=filename)  # 打开文件
    company_name_index = int
    tax_id_index = int
    document_id_index = int
    summary_index = int
    account_code_index = int
    account_name_index = int
    account_feature_cd_index = int
    credit_amount_index = int
    debit_amount_index = int
    partner_code_index = int
    partner_name_index = int

    sheet1 = wb.sheet_by_name('新增凭证用例')  # 通过索引获取表格
    for index in range(sheet1.ncols):

        if ('company_name' == sheet1.cell_value(0, index)):
            company_name_index = index
        if ('tax_id' == sheet1.cell_value(0, index)):
            tax_id_index = index
        if ('document_id' == sheet1.cell_value(0, index)):
            document_id_index = index
        if ('summary' == sheet1.cell_value(0, index)):
            summary_index = index

        if ('account_code' == sheet1.cell_value(0, index)):
            account_code_index = index
        if ('account_name' == sheet1.cell_value(0, index)):
            account_name_index = index
        if ('account_feature_cd' == sheet1.cell_value(0, index)):
            account_feature_cd_index = index
        if ('credit_amount' == sheet1.cell_value(0, index)):
            credit_amount_index = index
        if ('debit_amount' == sheet1.cell_value(0, index)):
            debit_amount_index = index
        if ('partner_code' == sheet1.cell_value(0, index)):
            partner_code_index = index
        if ('partner_name' == sheet1.cell_value(0, index)):
            partner_name_index = index

    documents = []
    lastDocument_id = ''
    documentDetails = []
    for index in range(sheet1.nrows):
        if (index == 0):
            continue
        # ctype = sheet1.cell(i, j).ctype  # 表格的数据类型
        # cell = sheet1.cell_value(i, j)
        # if ctype == 2 and cell % 1 == 0:  # 如果是整形
        #     cell = int(cell)
        # elif ctype == 3:
        #     # 转成datetime对象
        #     date = datetime(*xldate_as_tuple(cell, 0))
        #     cell = date.strftime('%Y/%d/%m %H:%M:%S')
        # elif ctype == 4:
        #     cell = True if cell == 1 else False
        company_name = sheet1.cell_value(index, company_name_index)
        tax_id = sheet1.cell_value(index, tax_id_index)
        document_id = sheet1.cell_value(index, document_id_index)
        summary = sheet1.cell_value(index, summary_index)

        # account_code = str(sheet1.cell_value(index, account_code_index))
        ctype = sheet1.cell(index, account_code_index).ctype  # 表格的数据类型
        if ctype == 2 and sheet1.cell_value(index, account_code_index) % 1 == 0:  # 如果是整形
            account_code = str(int(sheet1.cell_value(index, account_code_index)))
        else:
            account_code = sheet1.cell_value(index, account_code_index)

        account_name = ''
        ctype = sheet1.cell(index, account_feature_cd_index).ctype  # 表格的数据类型
        if ctype == 2 and sheet1.cell_value(index, account_feature_cd_index) % 1 == 0:  # 如果是整形
            account_feature_cd = int(sheet1.cell_value(index, account_feature_cd_index))
        else:
            account_feature_cd = ''
        credit_amount = sheet1.cell_value(index, credit_amount_index)
        debit_amount = sheet1.cell_value(index, debit_amount_index)
        # if credit_amount != '\\N':
        # print(credit_amount)

        # if debit_amount != '\\N':
        # print(debit_amount)
        partner_code = sheet1.cell_value(index, partner_code_index)
        partner_name = sheet1.cell_value(index, partner_name_index)
        if (lastDocument_id == ''):
            lastDocument_id = document_id
            # log.d('第一次' )
        if (lastDocument_id == document_id):

            documentDetails.append(
                DocumentDetailAdd(company_name, tax_id, document_id, summary, account_code, account_name,
                                  account_feature_cd, credit_amount, debit_amount,
                                  partner_code, partner_name))
            # log.d('添加明细1', 'lastDocument_id',lastDocument_id,'document_id',document_id,len(documentDetails))
        else:
            documents.append(documentDetails)

            # log.d('添加凭证1',   len(documents))
            documentDetails = []
            documentDetails.append(
                DocumentDetailAdd(company_name, tax_id, document_id, summary, account_code, account_name,
                                  account_feature_cd, credit_amount, debit_amount,
                                  partner_code, partner_name))

            # log.d('添加明细2', 'lastDocument_id',lastDocument_id,'document_id',document_id,len(documentDetails))
        if (index == sheet1.nrows - 1):
            documents.append(documentDetails)
            # log.d('添加凭证 最后一次', len(documents))
            documentDetails = []
        lastDocument_id = document_id

    log.d('读取凭证excel文件完成，凭证数量：', len(documents))
    return 0, documents, None


def read_documentInput():
    log.d('读取凭证excel文件')
    dir = os.path.dirname(__file__)
    parent_path = os.path.dirname(dir)
    filename = parent_path + '/testCases/csae_document.xlsx'  # 根据项目所在路径，找到用例所在的相对项目的路径
    wb = xlrd.open_workbook(filename=filename)  # 打开文件
    tax_no_index = str
    document_id_index = int
    summary_index = int
    year_index = int
    month_index = int
    type_index = int
    TEMPLATE_ID_index = int
    TEMPLATED_NAME_index = int
    account_code_index = int
    account_name_index = int
    account_feature_cd_index = int
    credit_amount_index = int
    debit_amount_index = int
    partner_code_index = int
    partner_name_index = int

    sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格
    for index in range(sheet1.ncols):
        if ('tax_no' == sheet1.cell_value(0, index)):
            tax_no_index = index
        if ('year' == sheet1.cell_value(0, index)):
            year_index = index
        if ('month' == sheet1.cell_value(0, index)):
            month_index = index
        if ('type' == sheet1.cell_value(0, index)):
            type_index = index

        if ('document_id' == sheet1.cell_value(0, index)):
            document_id_index = index
        if ('summary' == sheet1.cell_value(0, index)):
            summary_index = index
        if ('TEMPLATE_ID' == sheet1.cell_value(0, index)):
            TEMPLATE_ID_index = index
        if ('TEMPLATED_NAME' == sheet1.cell_value(0, index)):
            TEMPLATED_NAME_index = index
        if ('account_code' == sheet1.cell_value(0, index)):
            account_code_index = index
        if ('account_name' == sheet1.cell_value(0, index)):
            account_name_index = index
        if ('account_feature_cd' == sheet1.cell_value(0, index)):
            account_feature_cd_index = index
        if ('credit_amount' == sheet1.cell_value(0, index)):
            credit_amount_index = index
        if ('debit_amount' == sheet1.cell_value(0, index)):
            debit_amount_index = index
        if ('partner_code' == sheet1.cell_value(0, index)):
            partner_code_index = index
        if ('partner_name' == sheet1.cell_value(0, index)):
            partner_name_index = index

    documents = []
    lastDocument_id = ''
    documentDetails = []
    for index in range(sheet1.nrows):
        if (index == 0):
            continue
        # ctype = sheet1.cell(i, j).ctype  # 表格的数据类型
        # cell = sheet1.cell_value(i, j)
        # if ctype == 2 and cell % 1 == 0:  # 如果是整形
        #     cell = int(cell)
        # elif ctype == 3:
        #     # 转成datetime对象
        #     date = datetime(*xldate_as_tuple(cell, 0))
        #     cell = date.strftime('%Y/%d/%m %H:%M:%S')
        # elif ctype == 4:
        #     cell = True if cell == 1 else False
        tax_no = sheet1.cell_value(index, tax_no_index)
        year = int(sheet1.cell_value(index, year_index))
        month = int(sheet1.cell_value(index, month_index))
        type = int(sheet1.cell_value(index, type_index))

        document_id = sheet1.cell_value(index, document_id_index)
        summary = sheet1.cell_value(index, summary_index)
        TEMPLATED_ID = int(sheet1.cell_value(index, TEMPLATE_ID_index))
        TEMPLATED_NAME = sheet1.cell_value(index, TEMPLATED_NAME_index)

        # account_code = str(sheet1.cell_value(index, account_code_index))

        ctype = sheet1.cell(index, account_code_index).ctype  # 表格的数据类型
        if ctype == 2 and sheet1.cell_value(index, account_code_index) % 1 == 0:  # 如果是整形
            account_code = str(int(sheet1.cell_value(index, account_code_index)))
        else:
            account_code = sheet1.cell_value(index, account_code_index)

        account_name = sheet1.cell_value(index, account_name_index)
        ctype = sheet1.cell(index, account_feature_cd_index).ctype  # 表格的数据类型
        if ctype == 2 and sheet1.cell_value(index, account_feature_cd_index) % 1 == 0:  # 如果是整形
            account_feature_cd = int(sheet1.cell_value(index, account_feature_cd_index))
        else:
            account_feature_cd = ''
        credit_amount = sheet1.cell_value(index, credit_amount_index)
        debit_amount = sheet1.cell_value(index, debit_amount_index)
        # if credit_amount != '\\N':
        # print(credit_amount)

        # if debit_amount != '\\N':
        # print(debit_amount)
        # partner_code = sheet1.cell_value(index, partner_code_index)
        ctype = sheet1.cell(index, partner_code_index).ctype  # 表格的数据类型
        if ctype == 2 and sheet1.cell_value(index, partner_code_index) % 1 == 0:  # 如果是整形
            partner_code = str(int(sheet1.cell_value(index, partner_code_index)))
        else:
            partner_code = sheet1.cell_value(index, partner_code_index)
        partner_name = sheet1.cell_value(index, partner_name_index)
        # if credit_amount != '\\N':
        # print(credit_amount)

        # if debit_amount != '\\N':
        # print(debit_amount)
        if (lastDocument_id == ''):
            lastDocument_id = document_id
            # log.d('第一次' )
        if (lastDocument_id == document_id):

            documentDetails.append(
                DocumentDetailInput(document_id, tax_no, year, month, type, TEMPLATED_ID, TEMPLATED_NAME, summary,
                                    account_code,
                                    account_name,
                                    account_feature_cd, credit_amount, debit_amount,
                                    partner_code, partner_name))
            # log.d('添加明细1', 'lastDocument_id',lastDocument_id,'document_id',document_id,len(documentDetails))
        else:
            documents.append(documentDetails)

            # log.d('添加凭证1',   len(documents))
            documentDetails = []
            documentDetails.append(
                DocumentDetailInput(document_id, tax_no, year, month, type, TEMPLATED_ID, TEMPLATED_NAME, summary,
                                    account_code,
                                    account_name,
                                    account_feature_cd, credit_amount, debit_amount,
                                    partner_code, partner_name))

            # log.d('添加明细2', 'lastDocument_id',lastDocument_id,'document_id',document_id,len(documentDetails))
        if (index == sheet1.nrows - 1):
            documents.append(documentDetails)
            # log.d('添加凭证 最后一次', len(documents))
            documentDetails = []
        lastDocument_id = document_id

    log.d('读取凭证excel文件完成，凭证数量：', len(documents))
    return 0, documents, None


def read_balanceSheetList():
    log.d('资产负债表excel文件')
    filename = str
    dir_or_files = os.listdir(config.FILE_DOWNLOAD)
    if len(dir_or_files) == 0:
        log.d(config.FILE_DOWNLOAD, '文件夹为空')
        return 1, None
    for dir_file in dir_or_files:
        filename = config.FILE_DOWNLOAD + "\\" + dir_file
    # log.i(filename)
    wb = xlrd.open_workbook(filename=filename)  # 打开文件

    sheet1 = wb.sheet_by_name('资产负债表')  # 通过索引获取表格
    lists = dict()
    for index in range(sheet1.nrows):
        if (index < 3):
            continue

        if sheet1.cell_value(index, 1) != '' and sheet1.cell_value(index, 1) != '11':
            line = str(int(sheet1.cell_value(index, 1)))
            qm = sheet1.cell_value(index, 2)
            nc = sheet1.cell_value(index, 3)

            lists['r' + line + 'qm'] = qm if qm != '0' else '0.00'
            lists['r' + line + 'nc'] = nc if nc != '0' else '0.00'
        if sheet1.cell_value(index, 5) != '':
            line = str(int(sheet1.cell_value(index, 5)))
            qm = sheet1.cell_value(index, 6)
            nc = sheet1.cell_value(index, 7)

            lists['r' + line + 'qm'] = qm if qm != '0' else '0.00'
            lists['r' + line + 'nc'] = nc if nc != '0' else '0.00'

    return 0, lists


def read_balanceList():
    log.d('余额表excel文件')
    filename = str
    dir_or_files = os.listdir(config.FILE_DOWNLOAD)
    if len(dir_or_files) == 0:
        log.d(config.FILE_DOWNLOAD, '文件夹为空')
        return 1, None
    for dir_file in dir_or_files:
        filename = config.FILE_DOWNLOAD + "\\" + dir_file
    log.i(filename)
    wb = xlrd.open_workbook(filename=filename)  # 打开文件

    sheet1 = wb.sheet_by_name('余额表')  # 通过索引获取表格
    lists = dict()
    for index in range(sheet1.nrows):
        if (index < 5):
            continue
        accountCode = sheet1.cell_value(index, 0)
        accountName = sheet1.cell_value(index, 1)
        beginningBalanceDebit = round(sheet1.cell_value(index, 2))
        beginningBalanceCrebit = round(sheet1.cell_value(index, 3))
        currentAmountDebit = round(sheet1.cell_value(index, 4))
        currentAmountCrebit = round(sheet1.cell_value(index, 5))
        endingBalanceDebit = round(sheet1.cell_value(index, 6))
        endingBalanceCrebit = round(sheet1.cell_value(index, 7))
        if index == sheet1.nrows - 1:
            lists['sum'] = Kemuyueb('sum', accountName, beginningBalanceDebit, beginningBalanceCrebit,
                                    currentAmountDebit, currentAmountCrebit, endingBalanceDebit, endingBalanceCrebit)
        else:
            lists[accountCode] = Kemuyueb(accountCode, accountName, beginningBalanceDebit, beginningBalanceCrebit,
                                          currentAmountDebit, currentAmountCrebit, endingBalanceDebit,
                                          endingBalanceCrebit)
    return 0, lists


def read_subsidiaryLedgerList():
    log.d('明细账excel文件')
    filename = str
    dir_or_files = os.listdir(config.FILE_DOWNLOAD)
    if len(dir_or_files) == 0:
        log.d(config.FILE_DOWNLOAD, '文件夹为空')
        return 1
    for dir_file in dir_or_files:
        filename = config.FILE_DOWNLOAD + "\\" + dir_file
    log.i(filename)
    wb = xlrd.open_workbook(filename=filename)  # 打开文件

    sheet1 = wb.sheet_by_name('明细账')  # 通过索引获取表格
    lastKmCode = ''
    lists = dict()
    subsidiaryLedgers = []
    for index in range(sheet1.nrows):
        if (index < 3):
            continue
        kmCode = sheet1.cell_value(index, 0).split('_')[0]
        kmName = sheet1.cell_value(index, 0).split('_')[1]
        date = sheet1.cell_value(index, 1)
        voucherNo = sheet1.cell_value(index, 2)
        summary = sheet1.cell_value(index, 3)
        debitAmount = sheet1.cell_value(index, 4)
        creditAmount = sheet1.cell_value(index, 5)
        direction = sheet1.cell_value(index, 6)
        qmYue = sheet1.cell_value(index, 7)

        sl = SubsidiaryLedger(kmCode, kmName, date, voucherNo, summary, debitAmount, creditAmount, direction, qmYue)
        # subsidiaryLedgers.append(sl)
        # log.d(kmCode,kmName,date, voucherNo, summary, debitAmount,creditAmount,direction,qmYue)
        # log.d(kmCode,kmName,date, voucherNo, summary, sl.debitAmount,sl.creditAmount,direction,sl.qmYue)
        if (lastKmCode == ''):
            lastKmCode = kmCode
            # log.d('第一次' )
        if (lastKmCode == kmCode):
            subsidiaryLedgers.append(sl)
        else:
            lists[lastKmCode] = subsidiaryLedgers
            subsidiaryLedgers = []
            subsidiaryLedgers.append(sl)
        if (index == sheet1.nrows - 1):
            lists[kmCode] = subsidiaryLedgers
            # log.d('最后一次', len(lists))
            subsidiaryLedgers = []
        lastKmCode = kmCode
    return 0, lists


def read_Balance(path):
    log.d('读取用例公司信息excel文件')
    dir = os.path.dirname(__file__)
    parent_path = os.path.dirname(dir)
    # filename = parent_path + '/testCases/湖北达喜供应链管理有限公司_余额表_202004-202004.xls'  # 根据项目所在路径，找到用例所在的相对项目的路径
    wb = xlrd.open_workbook(filename=path)  # 打开文件
    bm_index = 0
    mc_index = 1
    qcD_index = 2
    qcC_index = 3
    bqD_index = 4
    bqC_index = 5
    qmD_index = 6
    qmC_index = 7
    lists = dict()
    sheet1 = wb.sheet_by_name('余额表')  # 通过索引获取表格
    for index in range(sheet1.nrows):
        if index < 5:
            continue

        bm = sheet1.cell_value(index, bm_index)
        mc = sheet1.cell_value(index, mc_index)
        qcD = sheet1.cell_value(index, qcD_index)
        qcC = sheet1.cell_value(index, qcC_index)
        bqD = sheet1.cell_value(index, bqD_index)
        bqC = sheet1.cell_value(index, bqC_index)
        qmD = sheet1.cell_value(index, qmD_index)
        qmC = sheet1.cell_value(index, qmC_index)
        if index == sheet1.nrows - 1:
            lists['sum'] = Kemuyueb('sum',   mc, qcD, qcC, bqD, bqC, qmD, qmC)
        else:
            if bm =='':
                continue
            lists[bm] = Kemuyueb(bm, mc, qcD, qcC, bqD, bqC, qmD, qmC)
        # log.i(bm, mc, qcD, qcC, bqD, bqC, qmD, qmC)
    return 0 ,lists

def read_BalanceBaseCode(path):
    log.d('读取用例公司信息excel文件')
    dir = os.path.dirname(__file__)
    # parent_path = os.path.dirname(dir)
    # filename = parent_path + '/testCases/湖北达喜供应链管理有限公司_余额表_202004-202004.xls'  # 根据项目所在路径，找到用例所在的相对项目的路径
    wb = xlrd.open_workbook(filename=path)  # 打开文件
    bm_index = 0
    mc_index = 1

    lists = dict()
    sheet1 = wb.sheet_by_name('科目表')  # 通过索引获取表格
    for index in range(sheet1.nrows):
        if index < 5:
            continue

        bm = sheet1.cell_value(index, bm_index)
        mc = sheet1.cell_value(index, mc_index)

        if bm =='':
            continue
        lists[bm] = Kemuyueb(bm, mc, 0, 0, 0, 0, 0, 0)

    return 0 ,lists


if __name__ == "__main__":
    # read_excel()
    # file = 'C:\\Users\\Liqg\\Desktop\\book1.xlsx'
    # dir = os.path.dirname(__file__)
    # parent_path = os.path.dirname(dir)
    # case_dir = parent_path + '/testCases/csae_document.xlsx'  # 根据项目所在路径，找到用例所在的相对项目的路径
    # ret, documents, msg = read_documentInput( )
    # read_CompanyInfo()
    # log.i(config.caseCompanyName)
    # log.d(documents)
    # read_balanceList()
    read_Balance(None)
