import random

from src.Model.Player import *


class GameLogic:
    """a private variable stating the amount of fine needed to be paid for getting out of jail"""
    _fine = 150

    @staticmethod
    def get_fine():
        return GameLogic._fine

    @staticmethod
    def  set_fine(fine):
        GameLogic._fine = fine


    _current_round = 1

    @staticmethod
    def get_current_round():
        return GameLogic._current_round

    @staticmethod
    def set_current_round(new_round):
        GameLogic._current_round = new_round

    """Get the number rolled from the two dices by a player"""
    @staticmethod
    def roll_dice():
        return random.randint(1, 4), random.randint(1, 4)

    """The move logic, how a player moves on the board, and the tiles he/she lands or have been through"""

    @staticmethod
    def player_move(dice_number, player, gameboard):
        for i in range(0, dice_number):
            player.update_square(1)
            if player.get_square() > 19:
                player.current_square = 0
            if gameboard.tiles[player.get_square() - 1].name == "Go" and i != dice_number - 1:
                gameboard.tiles[player.get_square() - 1].player_landed(player)  # Import Logic for 'Go'

        gameboard.tiles[player.get_square() - 1].player_landed(player)  # Run other logic when the player lands

    """Three functions are for in jail"""

    @staticmethod
    def player_first_round(player):
        return player.get_in_jail_turns() == 3

    @staticmethod
    def player_second_round(player):
        return player.get_in_jail_turns() == 2

    """The player is forced to pay a fine if the player did not pay in the first and second round in jail. 
        This condition monitoring should happen in the controller, meaning the controller needs to check 
        the condition and apply the correct function"""

    @staticmethod
    def player_third_round(player):
        return player.get_in_jail_turns() == 1

    """Check if the result of the two dice rolls are the same"""

    @staticmethod
    def same_double(dice_number1, dice_number2):
        return dice_number1 == dice_number2

    """The player gets out of jail as soon as getting the same number on two dices"""

    @staticmethod
    def out_jail_on_double(player, dice_number1, dice_number2, gameboard):
        GameLogic.player_move(dice_number1 + dice_number2, player, gameboard)
        player.set_in_jail_turns(0)
        player.is_jailed(False)
        player.set_fine_payed(False)
        gameboard.get_jail_tile().free_player(player)

    """Pay the fine of 150 in jail"""

    @staticmethod
    def pay_fine(player):
        player.remove_money(GameLogic.get_fine())
        player.set_fine_payed(True)

    """Check if player is broke, negative money"""

    @staticmethod
    def player_broke(player):
        return player.get_current_money() < 0

    @staticmethod
    def player_out(player, player_list, broke_list):
        player_list.remove(player)
        broke_list.append(player)
        player.delete_all_properties()

    """Check if the game is finished"""

    @staticmethod
    def game_ends(player_list):
        return GameLogic.get_current_round() == 100 or len(player_list)== 1

    @staticmethod
    def display_winner(player_list):
        if GameLogic.get_current_round() == 100:
            winner_list = []
            message = "The winner is: "
            value = -1
            for player in player_list:
                if player.get_current_money() >= value:
                    winner_list.append(player)
                    message += f"{player.getname()}, "
                    value = player.get_current_money()
            message = f"{message}with {winner_list[0].get_current_money()} money."
            return message
        elif len(Player.players_list) == 1:
            message = f"The winner is: {Player.players_list[0].getname()}, with {Player.players_list[0].get_current_money()} money."
            return message


    @staticmethod
    def store_current_game(self):
        pass
