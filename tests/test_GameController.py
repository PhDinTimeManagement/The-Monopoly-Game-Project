from unittest import TestCase
from src.Controller.GameController import *
from src.Model.Gameboard import *

class TestGameController(TestCase):
    def test_save_game(self):
        GameController.save_game()

    def test_load_game(self):
        localController = GameController()
        GameController.load_game(localController)
        assert localController.get_game_round() == 50
        assert localController.board.tiles[0].get_tile_name() == "Start"
        assert localController.board.tiles[0].get_pass_prize() == 3000
        assert localController.broke_players[0].get_name() == "Player 3"
        assert localController.broke_players[0].get_current_money() == 15000
        assert localController.broke_players[0].get_jail_status() == True
        assert localController.broke_players[0].get_square() == 6
        assert localController.broke_players[0].get_in_jail_turns() == 2
