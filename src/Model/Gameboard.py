import random


class Tile:
    """Parent class for all tiles"""

    def __init__(self, name, board_pos):
        self.name = name
        self.board_pos = int(board_pos)
        self.tile_type = None

    def get_tile_position(self):
        return self.board_pos

    def get_tile_name(self):
        return self.name

    def set_tile_name(self, new_name):
        self.name = new_name

    def set_tile_pos(self, board_pos):
        self.board_pos = board_pos

    def set_tile_type(self, tile_type):
        self.tile_type = tile_type

    """Manages what happens to a player that lands on the tile"""
    # noinspection PyStatementEffect
    """
           By Kent: This should be a class method. I have modified it, since I want to use dynamic binding here
           to decrease the complexity of the game logic. Every class will have a player_landed
        """
    @classmethod
    def player_landed(cls, player):
        return None

    def update_name_pos_type(self, tile_name: str, board_pos: int, type: str) -> None:
        self.set_tile_name(tile_name)
        self.set_tile_pos(board_pos)
        self.set_tile_type(type)


class Property(Tile):
    """  Property has the following attributes
    All attributes have to be passed when initialized """

    def __init__(self, name, board_pos, price, rent, owner, color):
        super().__init__(name, board_pos)
        self.price = price
        self.rent = rent
        self.owner = owner
        self.color = color
        self.tile_type = "property"

    def get_property_name(self):
        return self.name

    def get_rent(self):
        return self.rent

    def set_rent(self, new_rent):
        self.rent = new_rent

    def get_price(self):
        return self.price

    def set_price(self, new_price):
        self.price = new_price

    def get_owner(self):
        return self.owner

    def set_owner(self, new_owner):
        self.owner = new_owner

    def get_color(self):
        return self.color

    def set_color(self, new_color):
        self.color = new_color

    def update_values(self, price: int, rent: int, owner: object, color: str) -> None:
        self.set_price(price)
        self.set_rent(rent)
        self.set_owner(owner)
        self.set_color(color)

    def buy(self, player):
        """ if property has no owner can be bought, then checks player balance
            if enough: removes money, adds property to player, sets property new owner
            returns 0 for not enough money, 1 for success """
        if player.get_current_money() >= self.price:
            player.remove_money(self.price)
            player.add_properties(self)
            self.set_owner(player)
            print(f"{player.get_name()} bought {self.name} for {self.get_price()} HKD")
            return True
        else:
            print(f"{player.get_name()}'s balance is not enough to buy {self.name}")
            return False

    def pay_rent(self, player):
        rent_amount = self.get_rent()   # gets rent value
        if player.get_current_money() < rent_amount:    # checks if player has enough money to pay
            rent_amount = player.get_current_money()  # if not gets all the player can give
        player.remove_money(self.get_rent())    # removes from the player total what is owed
        self.owner.add_money(rent_amount)  # all money available is added to the owner
        print(f"{player.get_name()} payed {rent_amount} HKD to {self.owner.get_name()}")
        return player.get_current_money()   # current player amount is returned (only for testing)

    def player_landed(self, player):
        """provides option to the player"""
        if self.owner is None:
            return True
            #message = f"{self.name} is available for purchase. Listed at {self.get_price()} HKD"
            """TODO GET INPUT FROM PLAYER if INPUT == BUY TILE: self.buy(player)"""
        else:
            #message = f"{self.name} is owned by {self.get_owner()}. {player.get_name()} owes {self.get_price()} HKD"
            self.pay_rent(player)
            return False
        #return message


class Jail(Tile):
    """Initialize the empty array of jailed players"""
    def __init__(self, board_pos, jailed_players):
        super().__init__("Jail", board_pos)
        self.jailed_players = jailed_players
        self.tile_type = "jail"

    def set_jailed_players(self, jailed_players):
        self.jailed_players = jailed_players.copy()

    def get_jailed_players(self):
        return self.jailed_players

    def update_values(self, jailed_players):
        self.set_jailed_players(jailed_players)

    def free_player(self, player):
        self.jailed_players.remove(player)
        print(f"{player.get_name()} is freed from Jail")


    def player_landed(self, player):
        return None


# initialized here in order to be hardcoded into go to jail tile
JailTile = Jail(5, [])


class Go(Tile):
    """Initialize the prize for passing amount"""
    def __init__(self, prize):
        super().__init__("Go", 0)
        self.pass_prize = prize
        self.tile_type = "go"

    def get_pass_prize(self):
        return self.pass_prize

    def set_pass_prize(self, new_prize):
        self.pass_prize = new_prize

    def update_values(self, pass_prize):
        self.set_pass_prize(pass_prize)

    """When called adds pass_prize to the player balance"""
    def player_landed(self, player):
        player.add_money(self.get_pass_prize())
        return None

class GoToJail(Tile):
    def __init__(self, board_pos):
        super().__init__("Go To Jail", board_pos)
        self.tile_type = "go_to_jail"

    @staticmethod
    def arrest_player(player):
        player.is_jailed(True)
        player.set_in_jail_turns(3)     # sets max turns to spend in jail
        player.set_current_square(JailTile.get_tile_position())    # the player position is updated to the jail position
        JailTile.jailed_players.append(player)      # puts the player name in the jail list of detainees
        print(f"{player.get_name()} has been locked up")

    def player_landed(self, player):
        return self.arrest_player(player)


class Chance(Tile):
    def __init__(self, board_pos):
        super().__init__("Chance", board_pos)
        self.tile_type = "chance"

    def player_landed(self, player):
        good_chance = int(random.random() * 2)
        if good_chance:
            amount = int(random.random() * 21) * 10
            player.add_money(amount)
        else:
            amount = int(random.random() * 31) * 10
            player.remove_money(amount)
        return None


class IncomeTax(Tile):
    def __init__(self, board_pos, new_tax):
        super().__init__("IncomeTax", board_pos)
        self.tax_percentage = new_tax
        self.tile_type = "income_tax"

    def set_income_tax(self, new_tax):
        self.tax_percentage = new_tax

    def update_values(self, income_tax):
        self.set_income_tax(income_tax)

    def calculate_tax(self, player):
        return int(player.get_current_money() / 100) * self.tax_percentage  # tax_percentage ROUNDED DOWN TO NEAREST 10x

    def player_landed(self, player):
        tax_amount = self.calculate_tax(player)
        player.remove_money(tax_amount)
        return None


class FreeParking(Tile):
    def __init__(self, board_pos):
        super().__init__("Free Parking", board_pos)
        self.tile_type = "free_parking"

    def player_landed(self, player):
        return None


class Gameboard:
    def __init__(self):
        self.tiles = [Go(1500),
                      Property("Central", 1, 800, 90, None, "Blue"),
                      Property("Wan Chai", 2, 700, 65, None, "Blue"),
                      IncomeTax(3, 10),
                      Property("Stanley", 4, 600, 60, None, "Blue"),
                      JailTile,     # initialized globally after Jail to be used in goToJail
                      Property("Shek-O", 6, 400, 10, None, "Red"),
                      Property("Mong Kok", 7, 500, 40, None, "Red"),
                      Chance(8),
                      Property("Tsing Yi", 9, 400, 15, None, "Red"),
                      FreeParking(10),
                      Property("Shatin", 11, 700, 75, None, "Green"),
                      Chance(12),
                      Property("Tuen Mun", 13, 400, 20, None, "Green"),
                      Property("Tai Po", 14, 500, 25, None, "Green"),
                      GoToJail(15),
                      Property("Sai Kung", 16, 400, 10, None, "Yellow"),
                      Property("Yuen Long", 17, 400, 25, None, "Yellow"),
                      Chance(18),
                      Property("Tai O", 19, 600, 25, None, "Yellow")
                      ]     # Stores different Tile Objects. Can be customized by the user

    def get_jail_tile(self):
        for i in range (0,len(self.tiles)):
            if self.tiles[i].name == "Jail":
                return self.tiles[i]