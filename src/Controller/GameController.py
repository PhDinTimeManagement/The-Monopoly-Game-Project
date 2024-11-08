# GameController.py

import json
import os.path

from src.Model.Gameboard import *
from src.Model.Player import *
from src.Model.GameLogic import GameLogic
from datetime import datetime
from src.View.GUI import *


class GameController:
    def __init__(self, the_gui):
        self.save_name = None
        self.board = Gameboard()
        self.game_logic = GameLogic()
        self.gui = the_gui
        self.player_list = []
        self.broke_list = []
        self.input_handler = InputHandler()
        self.click_var = tk.StringVar()

        # passes necessary information to the gui and creates missing frames
        self.pass_color_information_for_display()
        self.pass_tile_information_for_display()
        self.gui.show_game_play_frame()
        # self.gui.show_frame("gameplay")

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

    def pass_tile_information_for_display(self):
        for i in range(0, 20):
            empty_9tuple = [None, None, None, None, None, None, None, None, None]
            # creates new empty row
            self.gui.gameplay_frame.tile_info.append(empty_9tuple)

            # for easier reading of code
            tile_info = self.gui.gameplay_frame.tile_info[i]
            board_tile = self.board.tiles[i]

            # updates fields with relevant information
            tile_info[0] = board_tile.get_tile_type()
            tile_info[1] = board_tile.get_tile_name()
            if tile_info[0] == "property":
                tile_info[2] = board_tile.get_price()
                tile_info[3] = board_tile.get_rent()
                tile_info[4] = board_tile.get_owner()
            elif tile_info[0] == "go":
                tile_info[2] = board_tile.get_pass_prize()
            elif tile_info[0] == "income_tax":
                tile_info[2] = board_tile.get_income_tax()


    def pass_color_information_for_display(self):
        for i in range(0, 20):
            self.gui.gameplay_frame.tile_colors.append(None)
            has_color = self.gui.gameplay_frame.get_color_coord(i)
            if has_color:
                color = self.board.tiles[i].get_color()
                self.gui.gameplay_frame.set_color(i, color)

    # TODO By Kent: We need to program to detect the click events from the users. The click will call the functions for us. """
    def start_game(self):
        self.initialize_players()
        while not GameLogic.game_ends(self.game_logic, self.get_player_list()):
            # TODO self.play_round()
            self.game_logic.set_current_round(self.game_logic.get_current_round() + 1)

    """ This function is called after the 'Play' button is clicked in the game """

    def button_play(self):
        self.game_logic.set_player_turn(self.get_player_list())
        player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]

    # TODO <show the roll dice button and display player_this_turn ONLY. IMPORTANT: CONFIG ALL THE BUTTONS WITH ITS FUNCTIONS>

    def determine_next_round(self, player_this_turn):
        """ Action is an array that stores the state of the Model after calling the 'determine_next_round' function """
        action = GameLogic.determine_next_round(self.game_logic, player_this_turn, self.get_player_list(),
                                                self.get_broke_player_list())

        if action[0] == "game_ends":
            print(action[1])
            # TODO <display the winner>
            # wait for click event
            return

        # TODO <Display the player for next round>
        if action[0] == "jail_roll":
            # TODO <display jail_roll only>
            return action  # del
        elif action[0] == "pay_fine_and_jail_roll":
            # TODO <display jail_roll and pay fine>
            return action  # del
        elif action[0] == "Roll":
            # TODO <display roll only>
            return action  # del

    def land_and_complete_round(self, tile, player_this_turn):
        tile_type = tile.get_tile_type()
        action = None
        if tile_type == "property":
            if tile.get_owner() is None:
                if tile.can_buy(player_this_turn):
                    # TODO show button buy or not buy
                    pass  # del
                else:
                    # TODO show not buy only
                    pass  # del
                self.gui.wait_variable(self.click_var)  # waits for the click_var to update before allowing execution
                if self.click_var == "buy":
                    action = "buy"
                elif self.click_var == "not_buy":
                    action = "not_buy"
                pass
            else:
                # TODO update view for rent
                action = "rent"
            tile.player_landed(player_this_turn, action)
            if self.click_var == "buy":
                # TODO display property
                pass  # del
            else:
                # TODO display property not bought
                pass  # del
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
        tile.player_landed(tile, player_this_turn, action)

    """This function is called after pressing the 'Roll' button in the game window."""

    def roll_dice(self):
        player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]
        dice_roll1, dice_roll2 = GameLogic.roll_dice()
        tile = GameLogic.player_move(dice_roll1 + dice_roll2, player_this_turn, self.board)
        # TODO<Call function to display the animation in the view>
        self.land_and_complete_round(tile, player_this_turn)
        self.determine_next_round(player_this_turn)

    # Roll function for player in jail
    def in_jail_roll(self, player_this_turn):
        action = GameLogic.in_jail_roll(self.game_logic, player_this_turn, self.board)
        if action[0] == "show_pay_fine":
            # TODO <show the pay fine button>
            # wait for pay fine button to be clicked
            if action[1] is not None:
                self.land_and_complete_round(action[1], player_this_turn)
                # TODO <show moving animation>
        elif action[0] == "move":
            # TODO <show animation for player moving>
            self.land_and_complete_round(action[1], player_this_turn)
        elif action[0] == 'not_move':
            # TODO <display the normal roll button>
            pass  # del
        self.determine_next_round(player_this_turn)

    def pay_fine(self, player_this_turn):
        # pay_fine_logic
        GameLogic.pay_fine(self.game_logic, player_this_turn)
        # TODO <Show the money is deduced>

    def buy_button(self, name_of_action):
        self.click_var.set(name_of_action)

    def no_buy_button(self, name_of_action):
        self.click_var.set(name_of_action)
        # TODO <Show did not buy property>

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

    def save_gameboard(self, save_name):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves/gameboard_setups"))
        message1 = ""

        # ensures directory existence or creates
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            message1 = "Save directory deleted or non existent --> Creating"

        gameboard_setup = SavedGameboard(save_name, self)
        gameboard_data = gameboard_setup.to_dictionary()
        file_path = os.path.join(save_directory, f'{save_name}.json')
        with open(file_path, 'w') as save_file:
            json.dump(gameboard_data, save_file, indent=4)
            message = "Game saved successfully.\n"
        return f"{message1}\n{message}"

    # noinspection PyTypeChecker
    def save_game(self, save_name):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves/games"))
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

    # loads gameboard_data into gameboard object, if data is passed, handles it, otherwise acts on the board_name and looks for it
    def load_gameboard(self, board_name = "", game_data_dict = None):
        if game_data_dict is None:
            # determines the filepath of the saved gameboard
            save_directory = os.path.dirname(os.path.abspath(__file__))
            save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves/gameboard_setups"))
            file_path = os.path.join(save_directory, f'{board_name}.json')

            # parse save file into a dictionary and handles exceptions
            try:
                with open(file_path, 'r') as game_data:
                    game_data_dict = json.load(game_data)
            except FileNotFoundError:
                print("Board layout does not exist.")
                return
            except json.JSONDecodeError:
                print("Error in reading save file.")
                return

        # gameboard_setup is a list of dictionaries, will cycle and update appropriately
        gameboard_info = game_data_dict["gameboard_data"]["gameboard_setup"]
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

    def load_game(self, load_name):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves/games"))

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

        self.load_gameboard("", game_data_dict)

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

class SavedGameboard:
    def __init__(self, save_name, game_controller):
        self.board_name = save_name
        self.tiles = game_controller.board.tiles.copy()

    def to_dictionary(self):
        gameboard_data = [tile.__dict__ for tile in self.tiles]
        return {
            "board_name": self.board_name,
            "gameboard_setup": gameboard_data
        }

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
        self.gameboard = SavedGameboard("", game_controller)

        # Saves players information
        self.player_list = game_controller.get_player_list().copy()
        self.broke_list = game_controller.get_broke_player_list().copy()

    def to_dictionary(self):
        # unpacks list of objects to a list of dictionary entries
        gameboard_data = self.gameboard.to_dictionary()
        player_data = [player.__dict__ for player in self.player_list]
        broke_player_data = [player.__dict__ for player in self.broke_list]

        return {
            "save_name": self.save_name,
            "save_time": self.save_time,
            "_turn": self._turn,
            "remove_last_round": self.remove_last_round,
            "current_round": self.current_round,
            "gameboard_data": gameboard_data,
            "players_list": player_data,
            "broke_list": broke_player_data
        }

    def get_save_name(self):
        return self.save_name