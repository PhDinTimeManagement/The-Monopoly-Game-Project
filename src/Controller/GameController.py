# GameController.py

import json
import os.path

from src.Model.Gameboard import *
from src.Model.Player import *
from src.Model.GameLogic import GameLogic
from src.Controller.InputHandler import InputHandler
from datetime import datetime

class GameController:
    def __init__(self):
        self.save_name = None
        self.board = Gameboard()
        self.game_logic = GameLogic()
        self.player_list = []
        self.broke_list = []
        self.input_handler = InputHandler()

    def get_player_list(self):
        return self.player_list

    def set_player_list(self, player_list):
        self.player_list = player_list.copy()

    def get_broke_player_list(self):
        return self.broke_list

    def set_broke_player_list(self, broke_list):
        self.broke_list = broke_list.copy()

    def get_current_round(self):
        return self.game_logic.get_current_round()

    def get__turn(self):
        return self.game_logic.get_player_turn()

    def set__turn(self, turn):
        self.game_logic._player_turn = turn

    def set_current_round(self, new_round):
        self.game_logic.set_current_round(new_round)

    def set_save_name(self, save_name):
        self.save_name = save_name

    def set_remove_last_round(self, remove_last_round):
        self.game_logic.set_removed_last_round(remove_last_round)

    # TODO By Kent: We need to program to detect the click events from the users. The click will call the functions for us. """
    def start_game(self):
        self.initialize_players()
        while not GameLogic.game_ends(self.game_logic,self.get_player_list()):
            #TODO self.play_round()
            self.game_logic.set_current_round(self.game_logic.get_current_round() + 1)

    """ This function is called after the 'Play' button is clicked in the game """
    def button_play(self):
        self.game_logic.set_player_turn(self.get_player_list())
        player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]
       #TODO <show the roll dice button and display player_this_turn ONLY>

    def determine_next_round(self,player_this_turn):
        """Action is an array that stores the state of the Model after calling the 'determine_next_round' function"""
        action = GameLogic.determine_next_round(self.game_logic,player_this_turn,self.get_player_list(),self.get_broke_player_list())

        if action[0] == "game_ends":
            print(action[1])
            #TODO <display the winner>
            #wait for click event
            return

        # TODO <Display the player for next round>
        if action[0] == "jail_roll":
            #TODO <display jail_roll only>
            #wait for click event
            return action
        elif action[0] == "pay_fine_and_jail_roll":
            # TODO <display jail_roll and pay fine>
            #wait for click event
            return action
        elif action[0] == "Roll":
            # TODO <display roll only>
            #wait for click
            return action

        # if GameLogic.player_broke(player_this_turn):
        #     GameLogic.player_out(self.game_logic, player_this_turn, self.get_player_list(), self.get_broke_player_list())
        #
        # self.game_logic.set_current_round(self.game_logic.get_current_round() + 1)  # Update the current round by +1
        # if GameLogic.game_ends(self.get_player_list(), self.game_logic.get_current_round()):  # When the game ends
        #     GameLogic.display_winner(self.game_logic, self.get_player_list())
        # else:
        #     self.game_logic.set_player_turn(self.get_player_list())
        #     player_next_turn = self.get_player_list()[self.game_logic.get_player_turn()]
        #     #TODO <Display the player for next round>
        #     if player_next_turn.get_jail_status():
        #         if player_next_turn.get_fine_payed():
        #             pass
        #             # TODO <Display the roll only, do not display the pay fine button>
        #         elif GameLogic.player_third_round(player_next_turn):
        #             #TODO <Display roll dice only>
        #             pass
        #         else:
        #             pass
        #             # TODO <Display the pay fine button as well as the roll button>
        #
        #         # waiting the click event
        #         pass
        #     else:
        #         # TODO <The button no need to change, display just Roll_dice>
        #         # waiting the click event
        #         pass

    @staticmethod
    def land_and_complete_round(tile, player_this_turn):
        tile_type = tile.get_tile_type()
        action = None

        if tile_type == "property":
            if tile.get_owner() is None:
                # TODO show button buy or not buy
                # gui.wait_variable(click_var)    # waits for the click_var to update before allowing execution
                pass
            else:
                # TODO update view for rent
                action = "rent"
            tile.player_landed(player_this_turn, action)
            return
        elif tile_type == "jail":
             # TODO update view just visiting
            pass
        elif tile_type == "go":
            # TODO update view
            pass
        elif tile_type == "go_to_jail":
            # TODO jail animation
            pass
        elif tile_type == "income_tax":
            # TODO tax animation
            pass
        elif tile_type == "free_parking":
            # TODO parking animation
            pass
        tile.player_landed(player_this_turn)

    """This function is called after pressing the 'Roll' button in the game window."""
    def roll_dice(self):
        player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]
        dice_roll1, dice_roll2 = GameLogic.roll_dice()
        tile = GameLogic.player_move(dice_roll1+dice_roll2,player_this_turn,self.board)
        #TODO<Call function to display the animation in the view>
        self.land_and_complete_round(tile, player_this_turn)
        self.determine_next_round(player_this_turn)

    # Roll function for player in jail
    def in_jail(self):
        player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]
        dice_roll1, dice_roll2 = GameLogic.roll_dice()
        if (not GameLogic.same_double(dice_roll1,dice_roll2)) and GameLogic.player_third_round(player_this_turn):
            # TODO<show the pay fine button only, after paying fine, the player is moved (Got to pay_fine function)
            pass
        else:
            flag = False
            if GameLogic.same_double(dice_roll1,dice_roll2):
                #TODO <on double, going out of jail>
                flag = True
            elif GameLogic.player_second_round(player_this_turn) and player_this_turn.get_fine_payed():
                #TODO <Out of jail>
                flag = True
            if flag:
                self.board.tiles[player_this_turn.get_current_square()].freeplayer(player_this_turn)
                information = GameLogic.player_move(dice_roll1 + dice_roll2, player_this_turn, self.board)
                # TODO<Call function to display the animation in the view>
                self.land_and_complete_round(information, player_this_turn)
            else:
                #TODO <Player is not moved>
                pass
            self.determine_next_round(player_this_turn)


    def pay_fine(self,dice_roll1,dice_roll2):
        #pay_fine_logic
        player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]
        GameLogic.pay_fine(self.game_logic,player_this_turn)
        if player_this_turn.player_third_round(player_this_turn):
            self.board.tiles[player_this_turn.get_current_square()].freeplayer(player_this_turn)
            information = GameLogic.player_move(dice_roll1 + dice_roll2, player_this_turn, self.board)
            # TODO<Call function to display the animation in the view>
            self.land_and_det_next_round(information, player_this_turn)
            self.determine_next_round(player_this_turn)
        #TODO <Show the money is deduced>

    def buy_button(self):
        player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]
        self.board.tiles[player_this_turn.get_current_square()].buy(player_this_turn)
        #TODO <show the property bought>
    
    def no_buy_button(self):
        #TODO <Show did not buy property>
        return
        
    """By Kent: we don't need loop here. Instead we get a list from the view after the player clicks 'play'"""
    def initialize_players(self):
        num_players = self.input_handler.get_name_or_players("Enter the number of players (2-6): ")
        for i in range(num_players):
            player_name = self.input_handler.get_name_or_players(f"Enter name for Player {i + 1}: ")
            new_player = Player(player_name)
            self.get_player_list().append(new_player)
        print("Players initialized successfully.\n")

    def end_game(self):
        # Need to modify the logic in GameLogic endgame
        pass

    # noinspection PyTypeChecker
    def save_game(self, save_name):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves"))
        message1 = ""

        # ensures directory existence or creates
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            message1 = "Save directory deleted or non existent --> Creating"

        save_instance = SavedGame(save_name, self)
        game_data = save_instance.to_dictionary()
        file_path = os.path.join(save_directory, f'{save_name}.json')
        with open(file_path, 'w') as save_file:
            json.dump(game_data, save_file, indent=4)
            message = "Game saved successfully.\n"
        return f"{message1}\n{message}"


    def load_game(self, load_name):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves"))

        file_path = os.path.join(save_directory, f'{load_name}.json')

        # parse save file into a dictionary and handles exceptions
        try:
            with open(file_path, 'r') as game_data:
                game_data_dict = json.load(game_data)
        except FileNotFoundError:
            print("Game saved does not exist.")
            return
        except json.JSONDecodeError:
            print("Error in reading save file.")
            return

        # pulls information from the dictionary into respective variables
        self.set_save_name(game_data_dict["save_name"])
        self.set_current_round(game_data_dict["current_round"])
        self.set__turn(game_data_dict["_turn"])
        self.set_remove_last_round(game_data_dict["remove_last_round"])

        # gameboard_setup is a list of dictionaries, will cycle and update appropriately
        gameboard_info = game_data_dict["gameboard_setup"]
        for tile_info, i in zip(gameboard_info, range(20)):
            self.board.tiles[i].update_name_pos_type(tile_info["name"], tile_info["board_pos"], tile_info["tile_type"])
            tile_type = tile_info["tile_type"]
            if tile_type == "property":
                self.board.tiles[i].update_values(tile_info["price"], tile_info["rent"], tile_info["owner"], tile_info["color"])
            elif tile_type == "income_tax":
                self.board.tiles[i].update_values(tile_info["tax_percentage"])
            elif tile_type == "jail":
                self.board.tiles[i].update_values(tile_info["jailed_players"])
            elif tile_type == "go":
                self.board.tiles[i].update_values(tile_info["pass_prize"])

        # creates players objects and copies information from the dictionary
        players = game_data_dict["players_list"]
        for p_data in players:
            new_player = Player("")
            new_player.update_values(p_data["_username"], p_data["_current_money"], p_data["_jail_status"], p_data["_fine_payed"], p_data["_current_square"], p_data["_in_jail_turns"], p_data["_properties"])
            self.player_list.append(new_player)

        broke_players = game_data_dict["broke_list"]
        for p_data in broke_players:
            new_player = Player("")
            new_player.update_values(p_data["_username"], p_data["_current_money"], p_data["_jail_status"], p_data["_fine_payed"], p_data["_current_square"], p_data["_in_jail_turns"], p_data["_properties"])
            self.broke_list.append(new_player)

# this class will copy the current game instance
class SavedGame:
    def __init__(self, save_name, game_controller):
        # Gets the name of the save and current round
        self.save_name = save_name
        self.save_time = datetime.now().strftime("%H:%M %d-%m-%Y")
        self._turn = game_controller.get__turn()
        self.remove_last_round = game_controller.game_logic.get_remove_last_round()
        self.current_round = game_controller.get_current_round()

        # Saves the setup of the gameboard as a list
        self.tiles = game_controller.board.tiles.copy()

        # Saves players information
        self.player_list = game_controller.get_player_list().copy()
        self.broke_list = game_controller.get_broke_player_list().copy()

    def to_dictionary(self):
        # unpacks list of objects to a list of dictionary entries
        gameboard_data = [tile.__dict__ for tile in self.tiles]
        player_data = [player.__dict__ for player in self.player_list]
        broke_player_data = [player.__dict__ for player in self.broke_list]

        return {
            "save_name": self.save_name,
            "save_time": self.save_time,
            "_turn": self._turn,
            "remove_last_round": self.remove_last_round,
            "current_round": self.current_round,
            "gameboard_setup": gameboard_data,
            "players_list": player_data,
            "broke_list": broke_player_data
        }

    def get_save_name(self):
        return self.save_name