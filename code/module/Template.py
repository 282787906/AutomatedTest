class Template:
    tId = int
    tName = str
    tsId = int
    subjectType = int
    tsName = str
    kmCode = str
    kmName = str
    jdType = int

    def __init__(self, tId, tName,subjectType, tsId, tsName, kmCode, kmName, jdType):
        self.tId = tId
        self.tName = tName
        self.tsId = tsId
        self.subjectType = subjectType
        self.tsName = tsName
        self.kmCode = kmCode
        self.kmName = kmName
        self.jdType = jdType
