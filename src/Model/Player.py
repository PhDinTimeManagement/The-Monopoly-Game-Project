


class Player:
    """Lists that store the existing players and the player who is broke"""
    players_list = []
    broke_list = []

    def __init__(self, username):
        self._username = username
        self._current_money = 1500
        self._jail_status = False
        self._fine_payed = False
        self._current_square = 1
        self._in_jail_turns = 0
        self._properties = {}

    def getname(self):
        return self._username

    def get_current_money(self):
        return self._current_money

    def set_current_money(self, new_balance):
        self._current_money = new_balance

    def get_jail_status(self):
        return self._jail_status

    def get_fine_payed(self):
        return self._fine_payed

    def set_fine_payed(self, fine_payed):
        self._fine_payed = fine_payed

    def get_square(self):
        return self._current_square

    def update_square(self,value):
        self._current_square += value

    def get_in_jail_turns(self):
        return self._in_jail_turns

    def set_in_jail_turns(self, value):
        if value >=0 and value <= 3:
            self._in_jail_turns = value

    def add_money(self, money):
        self._current_money += money

    def remove_money(self, money):
        self._current_money -= money

    def is_jailed(self, state):
        self._jail_status = state

    def set_in_jail_turns(self, new_turns):
        self._in_jail_turns = new_turns

    def set_current_square(self, position):
        self._current_square = position

    def add_properties(self, properties):
        self._properties[properties] = properties.get_rent()

    def delete_properties(self, new_properties):
        pass

    """Delete all properties when the player is broke"""

    def delete_all_properties(self):
        for key in self._properties:
            key.set_owner(None)
        self._properties.clear()
