class AccountSetInfo:
    companyName=str         #公司名
    taxidCode=str           #税号
    taxType=int             #增值税类型（ 0小规模 1 一般纳税人）
    startDateYear=int       #建账时间
    startDateMonth=int      #建账时间
    startDateDay=int        #建账时间
    accountSystem=str       #会计制度
    org=str                 #组
    zxCenter=str            #中心
    zcfzgs=str              #资产负债公式
    auditer=str             #财务主管/审核人 新接口auditerUid字段
    inputUser=str           #录入人
    def __init__(self,companyName,taxidCode,taxType,startDateYear,startDateMonth,startDateDay,accountSystem,org,zxCenter,zcfzgs):
        self.companyName=companyName
        self.taxidCode=taxidCode
        self.taxType=taxType
        self.startDateYear=startDateYear
        self.startDateMonth=startDateMonth
        self.startDateDay=startDateDay
        self.accountSystem=accountSystem
        self.org=org
        self.zxCenter=zxCenter
        self.zcfzgs=zcfzgs

