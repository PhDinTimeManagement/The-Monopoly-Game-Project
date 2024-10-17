class Properties:
    def __init__(self,name,rent,price,owned):
        self.propertyName = name
        self.rent = rent
        self.price = price
        self.owned = False
        self.atSquare = None

    def setSquare(self,atSquare):
        self.atSquare = atSquare

    def getSquare(self):
        return self.atSquare

    def setOwned(self,owned):
        self.owned = owned

    def getPropertyName(self):
        return self.propertyName

    def getRent(self):
        return self.rent

    def getPrice(self):
        return self.price

    def getOwned(self):
        return self.owned