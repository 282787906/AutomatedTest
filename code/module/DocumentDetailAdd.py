class DocumentDetailAdd:
    company_name=str
    tax_id=str
    document_id=int
    summary = str
    account_code = str
    account_name = str
    account_feature_cd = str
    credit_amount = float
    debit_amount = float
    partner_code = str
    partner_name = str

    def __init__(self,company_name,tax_id,document_id, summary, account_code, account_name, account_feature_cd, credit_amount, debit_amount,
                 partner_code, partner_name):
        self.company_name = company_name
        self.tax_id = tax_id
        self.document_id = document_id
        self.summary = summary
        self.account_code = account_code
        self.account_name = account_name
        self.account_feature_cd = account_feature_cd
        self.credit_amount = credit_amount
        self.debit_amount = debit_amount
        self.partner_code = partner_code
        self.partner_name = partner_name

