class User:
    def __init__(self,username):
        self.username = username
        self.currentMoney = 1500
        self.jailStatus = False
        self.currentSquare = 1
        self.properties = {}

    def getname(self):
        return self.username

    def getCurrentMoney(self):
        return self.currentMoney

    def getJailStatus(self):
        return self.jailStatus

    def getSquare(self):
        return self.currentSquare

    def changeCurrentMoney(self,money):
        self.currentMoney += money

    def changeJailStatus(self,newStatus):
        self.jailStatus = newStatus

    def addProperties(self,newProperties):
        pass #define Properties Class First

    def deleteProperties(self,newProperties):
        pass

    def deleteAllProperties(self):
        pass