# GameController.py

from src.Model.Gameboard import *
from src.Model.Player import Player
from src.Model.GameLogic import GameLogic
from src.Controller.InputHandler import InputHandler

class GameController:
    def __init__(self):
        self.board = Gameboard()
        self.players = []
        self.broke_players = []
        self.input_handler = InputHandler()
        self.current_turn = 0
        self.game_round = 1

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
        # Need to odify the logic in GameLogic endgame
        pass