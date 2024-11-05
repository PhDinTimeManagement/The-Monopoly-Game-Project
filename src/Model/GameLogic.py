import random

from src.Model.Player import *


class GameLogic:
    """a private variable stating the amount of fine needed to be paid for getting out of jail"""
    def __init__ (self):
        self._fine = 150
        self._removed_last_round = False
        self._current_round = 1
        self._player_turn = -1


    def get_remove_last_round(self):
        return self._removed_last_round

    def set_removed_last_round(self,value):
        self._removed_last_round = value

    def get_fine(self):
        return self._fine

    def set_fine(self,fine):
        self._fine = fine

    def get_player_turn(self):
        return self._player_turn

    def set_player_turn(self,players_list):
        #If there is no player removed during last round
        if not self._removed_last_round:
            self._player_turn +=1
        self._removed_last_round = False
        self._player_turn = self._player_turn % len(players_list)

    def get_current_round(self):
        return self._current_round

    def set_current_round(self,new_round):
        self._current_round = new_round

    """Get the number rolled from the two dices by a player"""
    @staticmethod
    def roll_dice():
        return random.randint(1, 4), random.randint(1, 4)

    """The move logic, how a player moves on the board, and the tiles he/she lands or have been through"""

    @staticmethod
    def player_move(dice_number, player, gameboard):
        for i in range(0, dice_number):
            player.update_square(1)
            if player.get_square() > 20:
                player.set_square(1)
            if gameboard.tiles[player.get_square() - 1].name == "Go" and i != dice_number - 1:
                gameboard.tiles[player.get_square() - 1].player_landed(player)  # Import Logic for 'Go'

        information = gameboard.tiles[player.get_square() - 1].player_landed(player)  # Run other logic when the player lands
        return information

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


    def player_out(self,player, player_list, broke_list):
        player_list.remove(player)
        broke_list.append(player)
        player.delete_all_properties()
        self.set_removed_last_round(True)

    """Check if the game is finished"""

    @staticmethod
    def game_ends(player_list,game_round):
        return game_round == 100 or len(player_list)== 1

    @staticmethod
    def display_winner(player_list):
        if GameLogic.get_current_round() == 100:
            winner_list = []
            message = "The winner is: "
            value = -1
            for player in player_list:
                if player.get_current_money() >= value:
                    winner_list.append(player)
                    message += f"{player.get_name()}, "
                    value = player.get_current_money()
            message = f"{message}with {winner_list[0].get_current_money()} money."
            return message
        elif len(Player.players_list) == 1:
            message = f"The winner is: {Player.players_list[0].get_name()}, with {Player.players_list[0].get_current_money()} money."
            return message