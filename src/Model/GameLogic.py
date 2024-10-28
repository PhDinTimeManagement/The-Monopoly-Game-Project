import random


class GameLogic:
    round = 1
    """Get the number rolled from the two dices by a player"""

    @staticmethod
    def roll_dice():
        return random.randint(1, 4), random.randint(1, 4)

    """The move logic, how a player moves on the board, and the tiles he/she lands or have been through"""

    @staticmethod
    def player_move(dice_number, player, gameboard):
        for i in range(0, dice_number):
            player.current_square += 1
            if player.current_square > 19:
                player.current_square = 0
            if gameboard.tiles[player.current_square - 1].name == "Go" and i != dice_number - 1:
                gameboard.tiles[player.current_square - 1].player_landed(player)  # Import Logic for 'Go'

        gameboard.tiles[player.current_square - 1].player_landed(player)  # Run other logic when the player lands

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
        player.get_residing_jail().free_jail(player)

    """Pay the fine of 150 in jail"""

    @staticmethod
    def pay_fine(player):
        player.remove_money(150)
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
        return round == 100 or player_list.len() == 1

    @staticmethod
    def store_current_game(self):
        pass
