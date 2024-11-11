from unittest import TestCase
from src.Controller.GameController import *
from src.Model.Player import *

gui = GUI()

class TestGameController(TestCase):
    def test_set_player_list(self):
        test_controller1 = GameController(gui)
        Player1 = Player("Player 1")
        Player2 = Player("Player 2")
        player_list = [Player1, Player2]
        test_controller1.set_player_list([Player1, Player2])
        self.assertListEqual(test_controller1.get_player_list(), player_list)

    def test_save_game(self):
        test_controller = GameController(gui)

        test_controller.set_current_round(50)

        test_controller.board.tiles[0].set_tile_name("Start")
        test_controller.board.tiles[0].set_pass_prize(3000)

        # setting up the save file information to be used in the LOAD_TEST
        Player1 = Player("Player 1")
        Player2 = Player("Player 2")
        Player3 = Player("Player 3")
        jailTile = test_controller.board.tiles[5]
        Player2.update_values("BROKE PLAYER", -1500, True, False, 6, 2, [])
        test_controller.set_player_list([Player1, Player3])
        test_controller.set_broke_player_list([Player2])
        test_controller.board.tiles[15].player_landed(Player3)

        save_name = "SAVE_LOAD_TEST"
        test_controller.save_game(save_name)

    def test_load_game(self):
        # runs the save test first to generate the test file in case it's missing
        TestGameController.test_save_game(self)

        local_controller = GameController(gui)

        load_name = "SAVE_LOAD_TEST"
        local_controller.load_game(load_name)

        assert local_controller.get_current_round() == 50
        assert local_controller.board.tiles[0].get_tile_name() == "Start"
        assert local_controller.board.tiles[0].get_pass_prize() == 3000
        assert local_controller.get_broke_player_list()[0].get_name() == "BROKE PLAYER"
        assert local_controller.get_broke_player_list()[0].get_current_money() == -1500
        assert local_controller.get_broke_player_list()[0].get_jail_status() == True
        assert local_controller.get_broke_player_list()[0].get_current_position() == 6
        assert local_controller.get_broke_player_list()[0].get_in_jail_turns() == 2
        self.assertEqual(len(local_controller.board.tiles[5].get_jailed_players()), 1)

    def test_save_gameboard(self):
        test_controller = GameController(gui)
        tile = test_controller.board.tiles
        tile[0].set_tile_name("Start")
        tile[0].set_pass_prize(3000)
        tile[3].set_income_tax(50)
        tile[1].set_color("red")

        save_name = "TEST_GAMEBOARD_SETUP_SAVE"
        test_controller.save_gameboard(save_name)

