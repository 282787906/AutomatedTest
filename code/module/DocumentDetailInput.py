class DocumentDetailInput:

    document_id=int
    tax_no = str
    year = int
    month = int
    type = int
    TEMPLATED_ID = int
    TEMPLATED_NAME = str
    summary = str
    account_code = str
    account_name = str
    account_feature_cd = str
    credit_amount = float
    debit_amount = float
    partner_code = str
    partner_name = str


    def __init__(self, document_id,tax_no, year, month, type, TEMPLATED_ID,TEMPLATED_NAME, summary, account_code, account_name, account_feature_cd,
                 credit_amount, debit_amount,
                 partner_code, partner_name):
        self.document_id = document_id
        self.tax_no = tax_no
        self.year = year
        self.month = month
        self.type = type
        self.TEMPLATED_ID = TEMPLATED_ID
        self.TEMPLATED_NAME = TEMPLATED_NAME
        self.summary = summary
        self.account_code = account_code
        self.account_name = account_name
        self.account_feature_cd = account_feature_cd
        self.credit_amount = credit_amount
        self.debit_amount = debit_amount
        self.partner_code = partner_code
        self.partner_name = partner_name
