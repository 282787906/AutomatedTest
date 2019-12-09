class SubsidiaryLedger:
    kmCode = str
    date = str
    voucherNo = str
    summary = str
    debitAmount = str
    creditAmount = str
    direction = str
    qmYue = str

    def __init__(self, kmCode, kmName, date, voucherNo, summary, debitAmount, creditAmount, direction, qmYue):
        self.kmCode = kmCode
        self.kmName = kmName
        self.date = date
        self.voucherNo = voucherNo
        self.summary = summary
        self.debitAmount = debitAmount
        self.creditAmount = creditAmount
        self.direction = direction
        self.qmYue = qmYue
