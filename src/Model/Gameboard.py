import random
import math

class Tile:
    """Parent class for all tiles"""
    def __init__(self, name, board_pos):
        self.name = name
        self.board_pos = board_pos

    def set_tile_position(self, new_position):
        self.board_pos = new_position

    def get_tile_position(self):
        return self.board_pos

    """Manages what happens to a player that lands on the tile"""
    # noinspection PyStatementEffect
    """
           By Kent: This should be a class method. I have modified it, since I want to use dynamic binding here
           to decrease the complexity of the game logic. Every class will have a player_landed
        """
    @classmethod
    def player_landed(cls, player):
        pass


class Property(Tile):
    """
    Property has the following attributes
    All attributes have to be passed when initialized
    """
    def __init__(self, name, board_pos, price, rent, owner, color):
        super().__init__(name, board_pos)
        self.price = price
        self.rent = rent
        self.owner = owner
        self.__color = color

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
        """ if property has no owner can be bought, then checks player balance
            if enough: removes money, adds property to player, sets property new owner
            returns 0 for not enough money, 1 for success """
        if (player.get_current_money() >= self.price):
            player.remove_money(self.price)
            player.add_properties(self.name)
            self.set_owner(player)
            print(f"{player.getname()} bought {self.name} for {self.get_price()} HKD")
            return 1
        else:
            print(f"{player.getname()} balance is not enough to buy {self.name}")
            return 0

    def pay_rent(self, player):
        """checks if the curr player has enough money,
            if NOT ENOUGH will add to the owner player all curr player can give.
            then removes balance from curr player, adds balance to tile owner """
        rent_amount = self.get_rent()
        if player.get_current_money() < rent_amount:
            rent_amount = player.get_current_money()
        player.remove_money(self.get_rent())
        self.owner.add_money(rent_amount)

    def player_landed(self, player):
        """provides option to the player"""
        if self.owner is None:
            print(f"{self.name} is available for purchase. Listed at {self.get_price()} HKD")
            """GET INPUT FROM PLAYER if INPUT == BUY TILE: self.buy(player)"""
        else:
            print(f"{self.name} is owned by {self.get_owner()}. {player.getname()} owes {self.get_price()} HKD")
            pay_rent(player)


class Jail(Tile):
    """Initialize the empty array of jailed players"""
    def __init__(self):
        super().__init__("Jail", 6)
        self.jailed_players = []

    def set_jailed_players(self, jailed_players):
        for i in range(0, 6):
            self.jailed_players.append(jailed_players[i])

    def free_player(self, player):
        self.jailed_players.remove(player)
        print(f"{player.name} is freed from Jail")

    def player_landed(self, player):
        pass


class Go(Tile):
    """Initialize the prize for passing amount"""
    def __init__(self):
        super().__init__("Go", 1)
        self.pass_prize = 1500

    def set_pass_prize(self, pass_prize):
        self.pass_prize = pass_prize

    def get_pass_prize(self):
        return self.pass_prize

    """When called adds pass_prize to the player balance"""
    def player_landed(self, player):
        player.add_money(self.get_pass_prize())


class GoToJail(Tile):
    super().__init__("Go To Jail", 16)

    """player status change, turns in jail added, moved to jail pos,
        added to jail player list, """
    def arrest_player(self, player):
        player.change_jail_status()
        player.set_in_jail_turns(3)
        player.current_square = Jail.get_board_pos()
        Jail.jailed_players.append(player)
        print(f"{player.name} has been locked up")

    def player_landed(self, player):
        self.arrest_player(player)


class Chance(Tile):
    def __init__(self, board_pos):
        super().__init__("Chance", board_pos)

    def player_landed(self, player):
        good_chance = """GENERATE TRUE OR FALSE"""
        if good_chance:
            amount = """GENERATE RANDOM BETWEEN 1 AND 20""" * 10
            player.add_money(amount)
        else:
            amount = """GENERATE RANDOM BETWEEN 1 AND 30""" * 10
            player.remove_money(amount)


class IncomeTax(Tile):
    def __init__(self):
        super().__init__("IncomeTax", 4)
        self.tax_pct = 10

    def set_new_tax_pct(self, new_tax_pct):
        self.tax_pct = new_tax_pct

    def player_landed(self, player):
        tax_amount = """10% ROUNDED DOWN TO NEAREST 10x"""
        player.remove_money(tax_amount)


class FreeParking(Tile):
    super().__init__("FreeParking", 11)

    def player_landed(self, player):
        pass


class Gameboard:
    def __init__(self):
        tiles = []     #Stores different Tile Objects. Can be customized by the user
