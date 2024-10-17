class Player:
    def __init__(self,username):
        self.username = username
        self.currentMoney = 1500
        self.jail_status = False
        self.current_square = 1
        self.in_jail_turns = 0
        self.properties = {}

    def getname(self):
        return self.username

    def get_current_money(self):
        return self.currentMoney

    def get_jail_status(self):
        return self.jail_status

    def get_square(self):
        return self.current_square

    def get_in_jail_turns(self):
        return self.in_jail_turns

    def change_current_money(self,money):
        self.currentMoney += money

    def change_jail_status(self,new_status):
        self.jail_status = new_status

    def set_in_jail_turns(self,new_turns):
        self.in_jail_turns = new_turns

    def add_properties(self,new_properties):
        pass #define Properties Class First

    def delete_properties(self,new_properties):
        pass

    """Delete all properties when the player is broke"""
    def delete_all_properties(self):
        for key in self.properties:
            key.set_owner(None)
        self.properties.clear()
