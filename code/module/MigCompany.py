class MigCompany:

    taxNo = str
    companyName = str
    startYear = int
    currentYear = int
    site = str

    def __init__(self, taxNo, companyName,startYear,currentYear, site ):
        self.taxNo = taxNo
        self.companyName = companyName
        self.startYear = startYear
        self.currentYear = currentYear
        self.site = site