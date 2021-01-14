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
        if beginningBalanceDebit=='':
            self.beginningBalanceDebit = 0
        else:
            self.beginningBalanceDebit = beginningBalanceDebit

        if beginningBalanceCrebit == '':
            self.beginningBalanceCrebit = 0
        else:
            self.beginningBalanceCrebit = beginningBalanceCrebit

        if currentAmountDebit == '':
            self.currentAmountDebit = 0
        else:
            self.currentAmountDebit = currentAmountDebit

        if currentAmountCrebit == '':
            self.currentAmountCrebit = 0
        else:
            self.currentAmountCrebit = currentAmountCrebit
        if endingBalanceDebit == '':
            self.endingBalanceDebit = 0
        else:
            self.endingBalanceDebit = endingBalanceDebit
        if endingBalanceCrebit == '':
            self.endingBalanceCrebit = 0
        else:
            self.endingBalanceCrebit = endingBalanceCrebit

def dict2Kemuyueb(d):
    return Kemuyueb(d['accountCode'], d['accountName'], d['beginningBalanceDebit'],d['beginningBalanceCrebit']
                    ,d['currentAmountDebit'],d['currentAmountCrebit'],d['endingBalanceDebit'],d['endingBalanceCrebit'])
