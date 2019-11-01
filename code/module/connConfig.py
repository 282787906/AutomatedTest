class connConfig:
    dbName = str
    dbHost = str
    dbPort = int
    dbUser = str
    dbPasswd = str
    dbPlatform = str

    def __init__(self, dbName, dbHost, dbPort, dbUser, dbPasswd, dbPlatform):
        self.dbName = dbName
        self.dbHost = dbHost
        self.dbPort = dbPort
        self.dbUser = dbUser
        self.dbPasswd = dbPasswd
        self.dbPlatform = dbPlatform