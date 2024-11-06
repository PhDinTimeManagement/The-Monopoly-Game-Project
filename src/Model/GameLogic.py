import random

from src.Controller.GameController import GameController
from src.Model.Player import *
#from tests.test_GameLogic import game_logic


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
            if player.get_square() > 19:
                player.set_square(0)
            # TODO i != dice_number always since range is not inclusive
            if gameboard.tiles[player.get_square()].name == "Go" and i != dice_number:
                gameboard.tiles[player.get_square()].player_landed(player, )  # Import Logic for 'Go'

        # returns the new_tile
        return gameboard.tiles[player.get_square()]

    """Three functions are for in jail"""
    # TODO what is this???

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
        # TODO problem here, wont move properly (NOW FIXED BUT CHECK)
        tile = GameLogic.player_move(dice_number1 + dice_number2, player, gameboard)
        GameController.land_and_complete_round(tile, player)
        gameboard.get_jail_tile().free_player(player)

    """Pay the fine of 150 in jail"""

    @staticmethod
    def pay_fine(game_logic,player):
        player.remove_money(game_logic.get_fine())
        player.set_fine_payed(True)

    """Check if player is broke, negative money"""

    @staticmethod
    def player_broke(player):
        return player.get_current_money() < 0

    @staticmethod
    def player_out(game_logic,player, player_list, broke_list):
        player_list.remove(player)
        broke_list.append(player)
        player.delete_all_properties()
        game_logic.set_removed_last_round(True)

    """Check if the game is finished"""

    @staticmethod
    def game_ends(player_list,game_round):
        return game_round == 100 or len(player_list)== 1

    @staticmethod
    def display_winner(game_logic,players_list):
        if game_logic.get_current_round() == 100:
            winner_list = []
            message = "The winner is: "
            value = -1
            for player in players_list:
                if player.get_current_money() >= value:
                    winner_list.append(player)
                    message += f"{player.get_name()}, "
                    value = player.get_current_money()
            message = f"{message}with {winner_list[0].get_current_money()} money."
            return message
        elif len(players_list) == 1:
            message = f"The winner is: {players_list[0].get_name()}, with {players_list[0].get_current_money()} money."
            return message

    @staticmethod
    def determine_next_round(game_logic,player_this_turn,player_list,broke_list):

        #After each round check whether if the player_this_turn is broke
        if GameLogic.player_broke(player_this_turn):
            #Remove the player is the player is broke from the players_list into the broke list
            GameLogic.player_out(game_logic, player_this_turn, player_list,broke_list)

        #Increment current round
        game_logic.set_current_round(game_logic.get_current_round() + 1)

        #After each round check if the round ends
        if GameLogic.game_ends(game_logic.get_current_round(),player_list):
            # display the message showing the winner, pass the message as a parameter to display
            message = GameLogic.display_winner(game_logic,player_list)
            action = ["game_ends",message]
            return action

        #Set the player's turn for next around (a variable from 0 to len(player_list) -1
        game_logic.set_player_turn(player_list)

        #Fetch the player out from the player_list
        player_next_turn = player_list[game_logic.get_player_turn()]

        #if the player is in jail
        if player_next_turn.get_jail_status():
            #the player has paid the fine in jail or is in the third round, only roll button is displayed, therefore return "jail_roll"
            if player_next_turn.get_fine_payed() or GameLogic.player_third_round(player_next_turn):
                action = ["jail_roll",player_next_turn]
            else:
                #in other cases, the player can either choose to pay fine or to roll the dice, therefore return "pay_fine_and_jail_roll"
                action = ["pay_fine_and_jail_roll",player_next_turn]
            return action

        #if the player is not in jail, not shows the roll button
        else:
            action = ["Roll",player_next_turn]

            return action
