class Tile:
    """Parent class for all tiles"""
    def __init__(self, name):
        self.name = name

    """Manages what happens to a player that lands on the tile"""
    """
       By Kent: This should be a class method. I have modified it, since I want to use dynamic binding here
       to decrease the complexity of the game logic. Every class will have a player_landed
    """
    @classmethod
    def player_landed(cls,player):
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
        self.at_square = None

    def set_square(self, at_square):
        self.board_pos = at_square

    def get_square(self):
        return self.board_pos

    def set_owner(self, owner):
        self.owner = owner

    def get_property_name(self):
        return self.name

    def get_rent(self):
        return self.rent

    def get_price(self):
        return self.price

    def get_owner(self):
        return self.owner

    def buy(self, player):
        pass

class Go(Tile):
    super().__init__("Go")
    def player_landed(self,player):
        pass
    pass

class InJail(Tile):
    super().__init__("InJail")
    def player_landed(self,player):
        pass
    pass

class Chance(Tile):
    super().__init__("Chance")
    def player_landed(self,player):
        pass
    pass

class IncomeTax(Tile):
    super().__init__("IncomeTax")
    def player_landed(self,player):
        pass
    pass

class FreeParking(Tile):
    super().__init__("FreeParking")
    def player_landed(self,player):
        pass
    pass

class Gameboard:
    def __init__(self):
        tiles = []     #Stores different Tile Objects. Can be customized by the user
