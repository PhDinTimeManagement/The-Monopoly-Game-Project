# GameController.py

import json
import os.path

from src.Model.Gameboard import *
from src.Model.Player import Player
from src.Model.GameLogic import GameLogic
from src.Model.InputHandler import InputHandler
from tests.test_Gameboard import gameboard
from datetime import datetime

class GameController:
    def __init__(self):
        self.save_name = None
        self.board = Gameboard()
        self.players = [Player("Player 1"), Player("Player 2")]
        self.broke_players = []
        self.input_handler = InputHandler()
        self.current_turn = 0
        self.game_round = 10

    def get_player_list(self):
        return self.players

    def get_broke_player_list(self):
        return self.broke_players

    def get_game_round(self):
        return self.game_round

    def set_game_round(self, new_round):
        self.game_round = new_round

    def set_save_name(self, save_name):
        self.save_name = save_name

    def start_game(self):
        self.initialize_players()
        while not GameLogic.game_ends(self.players):
            self.play_round()
            GameLogic.set_current_round(self.game_round + 1)

    def initialize_players(self):
        num_players = self.input_handler.get_name_or_players("Enter the number of players (2-6): ")
        for i in range(num_players):
            player_name = self.input_handler.get_name_or_players(f"Enter name for Player {i + 1}: ")
            new_player = Player(player_name)
            self.players.append(new_player)
        print("Players initialized successfully.\n")

    def end_game(self):
        # Need to modify the logic in GameLogic endgame
        pass

    @staticmethod
    def save_game():
        save_name = input("Enter the name of the saved game: ")

        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves"))

        # ensures directory existence or creates
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            print("Save directory deleted or non existent --> Creating")

        game_data = SavedGame(save_name).to_dictionary()
        file_path = os.path.join(save_directory, f'{save_name}.json')
        with open(file_path, 'w') as save_file:
            json.dump(game_data, save_file, indent=4)
            print("Game saved successfully.\n")

    def load_game(self):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves"))

        save_name = input("Enter the name of the save you want to load: ")
        file_path = os.path.join(save_directory, f'{save_name}.json')

        # parse save file into a dictionary and handles exceptions
        try:
            with open(file_path, 'r') as game_data:
                game_data_dict = json.load(game_data)
        except FileNotFoundError:
            print("Game saved does not exist.")
        except json.JSONDecodeError:
            print("Error in reading save file.")

        # pulls information from the dictionary into respective variables
        self.set_save_name(game_data_dict["save_name"])
        controller.set_game_round(game_data_dict["current_round"])

        # gameboard_setup is a list of dictionaries, will cycle and update appropriately
        gameboard_info = game_data_dict["gameboard_setup"]
        for tile_info, i in gameboard_info, range(0, 20):
            self.board.tiles[i].update_name_pos(tile_info["name"], tile_info["board_pos"], tile_info["tile_type"])
            if tile_info.tile_type == "property":
                self.board.tiles[i].update_values(tile_info["price"], tile_info["rent"], tile_info["owner"], tile_info["color"])
            elif tile_info.tile_type == "income_tax":
                self.board.tiles[i].update_value(tile_info["tax_percentage"])
            elif tile_info.tile_type == "jail":
                self.board.tiles[i].update_value(tile_info["jail_players"])
            elif tile_info.tile_type == "go":
                self.board.tiles[i].update_value(tile_info["pass_prize"])

        # copies player list from save file as the format is compatible
        self.players = game_data_dict["players_list"].copy()
        self.broke_players = game_data_dict["broke_list"].copy()


""" INITIALIZING CONTROLLER TO BE USED IN SAVED GAME, contains game information needed"""
controller = GameController()

# this class will copy the current game instance
class SavedGame:
    def __init__(self, save_name):
        # Gets the name of the save and current round
        self.save_name = save_name
        self.save_time = datetime.now().strftime("%H:%M %d-%m-%Y")
        self.current_round = controller.get_game_round()

        # Saves the setup of the gameboard as a list
        self.tiles = gameboard.tiles.copy()

        # Saves players information
        self.players_list = controller.get_player_list().copy()
        self.broke_list = controller.get_broke_player_list().copy()

    def to_dictionary(self):
        # unpacks list of objects to a list of dictionary entries
        gameboard_data = [tile.__dict__ for tile in self.tiles]
        player_data = [player.__dict__ for player in self.players_list]
        broke_player_data = [player.__dict__ for player in self.broke_list]

        return {
            "save_name": self.save_name,
            "save_time": self.save_time,
            "current_round": self.current_round,
            "gameboard_setup": gameboard_data,
            "players_list": player_data,
            "broke_list": broke_player_data
        }

    def get_save_name(self):
        return self.save_name