from unittest import TestCase
from src.Controller.GameController import *
from src.Model.Player import *

class TestGameController(TestCase):
    def test_load_game(self):
        local_controller = GameController()
        GameController.load_game(local_controller)
        assert local_controller.get_current_round() == 50
        assert local_controller.board.tiles[0].get_tile_name() == "Start"
        assert local_controller.board.tiles[0].get_pass_prize() == 3000
        assert local_controller.get_broke_player_list()[0].get_name() == "BROKE PLAYER"
        assert local_controller.get_broke_player_list()[0].get_current_money() == -1500
        assert local_controller.get_broke_player_list()[0].get_jail_status() == True
        assert local_controller.get_broke_player_list()[0].get_square() == 6
        assert local_controller.get_broke_player_list()[0].get_in_jail_turns() == 2

    def test_save_game(self):
        test_controller = GameController()
        Player1 = Player("Player 1")
        Player2 = Player("Player 2")
        Player3 = Player("Player 3")
        Player2.update_values("BROKE PLAYER", -1500, True, False, 6, 2, [])
        test_controller.set_player_list([Player1, Player3])
        test_controller.set_broke_player_list([Player2])
        test_controller.board.tiles[15].player_landed(Player3)
        test_controller.save_game()

    def test_set_player_list(self):
        test_controller1 = GameController()
        Player1 = Player("Player 1")
        Player2 = Player("Player 2")
        player_list = [Player1, Player2]
        test_controller1.set_player_list([Player1, Player2])
        self.assertListEqual(test_controller1.get_player_list(), player_list)

