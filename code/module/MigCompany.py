class MigCompany:
    serNo = int
    taxNo = str
    companyName = str
    startYear = int
    currentYear = int
    site = str

    def __init__(self,serNo, taxNo, companyName,startYear,currentYear, site ):

        self.serNo = serNo
        self.taxNo = taxNo
        self.companyName = companyName
        self.startYear = startYear
        self.currentYear = currentYear
        self.site = site