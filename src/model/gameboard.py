class Tile:
    """Parent class for all tiles"""
    def __init__(self, name):
        self.name = name

    """Manages what happens to a player that lands on the tile"""
    def player_landed(self, player):
        pass


class Property(Tile):
    """
    Property has the following attributes
    All attributes have to be passed when initialized
    Except OWNER that will always start as None
    """
    def __init__(self, name, board_pos, price, rent):
        super().__init__(name)
        self.board_pos = board_pos
        self.price = price
        self.rent = rent
        self.owner = None

    def setSquare(self, atSquare):
        self.board_pos = atSquare

    def getSquare(self):
        return self.board_pos

    def setOwner(self, owner):
        self.owner = owner

    def getPropertyName(self):
        return self.name

    def getRent(self):
        return self.rent

    def getPrice(self):
        return self.price

    def getOwner(self):
        return self.owner

    def buy(self, player):
        pass


class Gameboard:
    def __init__(self):
        pass
