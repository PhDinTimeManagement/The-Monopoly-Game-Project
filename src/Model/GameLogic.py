import random

class GameLogic:

    """Get the number rolled from the two dices by a player"""
    @staticmethod
    def roll_dice():
        return random.randint(1,4),random.randint(1,4)

    """Check if the result of the two dice rolls are the same"""
    @staticmethod
    def same_double(dice_number1,dice_number2):
        return dice_number1 == dice_number2

    """The move logic, how a player moves on the board, and the tiles he/she lands or have been through"""
    @staticmethod
    def player_move(dice_number,player,gameboard):
        for i in range(0,dice_number):
            player.current_square += 1
            if player.current_square > 19:
                player.current_square = 0
            if gameboard.tiles[player.current_square-1].name == "Go" and i != dice_number-1:
                gameboard.tiles[player.current_square-1].player_landed(player) #Import Logic for 'Go'

        gameboard.tiles[player.current_square - 1].player_landed(player) #Run other logic when the player lands

    @staticmethod
    def pay_fine(player):
        pass

    @staticmethod
    def get_out_jail(player,dice_number1,dice_number2):
        pass


    @staticmethod
    def store_current_game(self):
        pass


