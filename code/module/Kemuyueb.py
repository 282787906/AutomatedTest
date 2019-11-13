class Kemuyueb:
    accountCode = str
    accountName = str
    beginningBalanceDebit = str
    beginningBalanceCrebit = str
    currentAmountDebit = str
    currentAmountCrebit = str
    endingBalanceDebit = str
    endingBalanceCrebit = str

    def __init__(self, accountCode, accountName, beginningBalanceDebit, beginningBalanceCrebit, currentAmountDebit, currentAmountCrebit, endingBalanceDebit, endingBalanceCrebit):
        self.accountCode = accountCode
        self.accountName = accountName
        self.beginningBalanceDebit = beginningBalanceDebit
        self.beginningBalanceCrebit = beginningBalanceCrebit
        self.currentAmountDebit = currentAmountDebit
        self.currentAmountCrebit = currentAmountCrebit
        self.endingBalanceDebit = endingBalanceDebit
        self.endingBalanceCrebit = endingBalanceCrebit

def dict2Kemuyueb(d):
    return Kemuyueb(d['accountCode'], d['accountName'], d['beginningBalanceDebit'],d['beginningBalanceCrebit']
                    ,d['currentAmountDebit'],d['currentAmountCrebit'],d['endingBalanceDebit'],d['endingBalanceCrebit'])
