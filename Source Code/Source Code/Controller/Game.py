#The class represents the game state, where the game is running on the computer
class Game:
    def __int__(self):
        self.playerList = {} # a list to store all the current in game players. Stores Class User Objects


    def storePlayers(self,user,playerID): #'user' is of type Class user, 'playerID of type int
        self.playerList[user] = playerID  #ID must be unique
        return True