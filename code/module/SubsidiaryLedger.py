from tools import log


class SubsidiaryLedger:
    accountCode = str
    accountName = str
    date = str
    voucherNo = str
    summary = str
    debitAmount = float
    creditAmount = float
    direction = str
    qmYue = float

    def __init__(self, accountCode, accountName, date, voucherNo, summary, debitAmount, creditAmount, direction, qmYue):
        self.accountCode = accountCode
        self.accountName = accountName
        self.date = date
        self.voucherNo = voucherNo
        self.summary = summary
        self.debitAmount =round( debitAmount,2)
        self.creditAmount = round( creditAmount,2)
        self.direction = direction
        if len(str(qmYue))>10:
            qmYue2=round(qmYue, 2)
        self.qmYue =round( qmYue,2)
def dict2SubsidiaryLedger(d):


    sl= SubsidiaryLedger(d['accountCode'], d['accountName'], d['date'],d['voucherNo']
                    ,d['summary'],d['debitAmount'],d['creditAmount'],d['direction'],d['qmYue'])
    if sl.voucherNo==None:
        sl.voucherNo=''
    # if sl.summary==None:
    #     sl.summary=''
    return sl
