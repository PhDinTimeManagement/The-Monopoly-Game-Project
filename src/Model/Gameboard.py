class Tile:
    """Parent class for all tiles"""
    def __init__(self, name, board_pos):
        self.name = name
        self.board_pos = board_pos

    def get_tile_position(self):
        return self.board_pos

    def set_tile_name(self, new_name):
        self.name = new_name

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

    def set_owner(self, owner):
        self.owner = owner

    def buy(self, player):
        """ if property has no owner can be bought, then checks player balance
            if enough: removes money, adds property to player, sets property new owner
            returns 0 for not enough money, 1 for success """
        if player.get_current_money() >= self.price:
            player.remove_money(self.price)
            player.add_properties(self)
            self.set_owner(player)
            message = f"{player.getname()} bought {self.name} for {self.get_price()} HKD"
            return 1,message
        else:
            message = f"{player.getname()} balance is not enough to buy {self.name}"
            return 0,message

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
            message = f"{self.name} is available for purchase. Listed at {self.get_price()} HKD"
            """TODO GET INPUT FROM PLAYER if INPUT == BUY TILE: self.buy(player)"""
        else:
            message = f"{self.name} is owned by {self.get_owner()}. {player.getname()} owes {self.get_price()} HKD"
            self.pay_rent(player)
        return message


class Jail(Tile):
    """Initialize the empty array of jailed players"""
    def __init__(self, board_pos, jailed_players):
        super().__init__("Jail", board_pos)
        self.jailed_players = jailed_players

    def set_jailed_players(self, jailed_players):
        self.jailed_players = jailed_players.copy()

    def free_player(self, player):
        self.jailed_players.remove(player)
        message = f"{player.name} is freed from Jail"
        return message

    def player_landed(self, player):
        pass

#initialized here in order to be hardcoded into go to jail tile
JailTile = Jail(5, [])

class Go(Tile):
    """Initialize the prize for passing amount"""
    def __init__(self, prize):
        super().__init__("Go", 0)
        self.pass_prize = prize

    def get_pass_prize(self):
        return self.pass_prize

    def set_pass_prize(self, new_prize):
        self.pass_prize = new_prize

    """When called adds pass_prize to the player balance"""
    def player_landed(self, player):
        player.add_money(self.get_pass_prize())


#Global Array containing list of all jail objects
list_of_jails = []


class GoToJail(Tile):
    def __init__(self, board_pos):
        super().__init__("Go To Jail", board_pos)

    def arrest_player(self, player):
        player.is_jailed(True)
        player.set_in_jail_turns(3)     #sets max turns to spend in jail
        player.set_current_square(JailTile.get_tile_position())     #the player position is updated to the jail position which cannot be changed
        JailTile.jailed_players.append(player)      #puts the player name in the jail list of detainees

        message = f"{player.name} has been locked up"
        return message

    def player_landed(self, player):
        return self.arrest_player(player)


class Chance(Tile):
    def __init__(self, board_pos):
        super().__init__("Chance", board_pos)

    def player_landed(self, player):
        good_chance = int(random.random() * 2)
        if good_chance:
            amount = int(random.random() * 21) * 10
            player.add_money(amount)
        else:
            amount = int(random.random() * 31) * 10
            player.remove_money(amount)


class IncomeTax(Tile):
    def __init__(self, board_pos, new_tax_percentage):
        super().__init__("IncomeTax", board_pos)
        self.tax_percentage = new_tax_percentage

    def set_income_tax(self, new_tax):
        self.tax_percentage = new_tax

    def player_landed(self, player):
        tax_amount = int(player.get_current_money() / 100) * 10 #10% ROUNDED DOWN TO NEAREST 10x
        player.remove_money(tax_amount)


class FreeParking(Tile):
    def __init__(self, board_pos):
        super().__init__("Free Parking", board_pos)

    def player_landed(self, player):
        pass


class Gameboard:
    def __init__(self):
        tiles = [   Go(1500),
                    Property("Central", 1, 800, 90, None, "Blue"),
                    Property("Wan Chai", 2, 700, 65, None, "Blue"),
                    IncomeTax(3, 10),
                    Property("Stanley", 4, 600, 60, None, "Blue"),
                    JailTile, #inizialized globally after Jail class in order to be hardcoded into goToJail tile behaviour
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
                ]     #Stores different Tile Objects. Can be customized by the user
