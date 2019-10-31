import os

import xlrd
from datetime import date, datetime

from module.DocumentDetailAdd import DocumentDetailAdd
from module.DocumentDetailInput import DocumentDetailInput

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

        account_code = str(sheet1.cell_value(index, account_code_index))
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

        account_code = str(sheet1.cell_value(index, account_code_index))
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


if __name__ == "__main__":
    # read_excel()
    file = 'C:\\Users\\Liqg\\Desktop\\book1.xlsx'
    dir = os.path.dirname(__file__)
    parent_path = os.path.dirname(dir)
    case_dir = parent_path + '/testCases/csae_document.xlsx'  # 根据项目所在路径，找到用例所在的相对项目的路径
    ret, documents, msg = read_documentAdd( )

    log.d(documents)
