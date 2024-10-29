from unittest import TestCase

from src.Model.GameLogic import *
from src.Model.Player import *
from src.Model.Gameboard import *

player1 = Player("Den")
player2 = Player("Ben")
gameboard = Gameboard()
gameboard.tiles[4] = Jail(4,player2)


class TestGameLogic(TestCase):
    def test_roll_dice(self):
        number1, number2 = GameLogic.roll_dice()
        self.assertLessEqual(number1, 4)
        self.assertLessEqual(number2,4)

    def test_player_move(self):
        self.fail()

    def test_player_first_round(self):
        player1.set_in_jail_turns(3)
        self.assertTrue(GameLogic.player_first_round(player1))

    def test_player_second_round(self):
        player1.set_in_jail_turns(2)
        self.assertTrue(GameLogic.player_second_round(player1))

    def test_player_third_round(self):
        player1.set_in_jail_turns(1)
        self.assertTrue(GameLogic.player_third_round(player1))

    def test_same_double(self):
        number1, number2 = GameLogic.roll_dice()
        if number1 == number2:
            self.assertTrue(GameLogic.same_double(number1, number2))
        else:
            self.assertFalse(GameLogic.same_double(number1, number2))

    def test_out_jail_on_double(self):

        GameLogic.out_jail_on_double(player1, 4, 4, gameboard)
        self.assertFalse(player1.get_jail_status())
        self.assertFalse(player1.get_fine_payed())

    def test_pay_fine(self):
        original = player1.get_current_money()
        GameLogic.pay_fine(player1)
        self.assertTrue(player1.get_fine_payed())
        self.assertEqual(player1.get_current_money(), original - GameLogic._fine)

    def test_player_broke(self):
        self.assertFalse(GameLogic.player_broke(player1))
        player1.set_current_money(-100)
        self.assertTrue(GameLogic.player_broke(player1))

    def test_player_out(self):
        Player.players_list.append(player1)
        GameLogic.player_out(player1, Player.players_list, Player.broke_list)
        self.assertFalse(player1 in Player.players_list)
        self.assertTrue(player1 in Player.broke_list)

    def test_game_ends(self):
        Player.players_list.append(player1)
        self.assertTrue(GameLogic.game_ends(Player.players_list))
        Player.players_list.remove(player1)
        GameLogic.set_current_round(100)
        self.assertTrue(GameLogic.game_ends(Player.players_list))

    def test_get_fine(self):
        GameLogic.set_fine(100)
        self.assertEqual(GameLogic.get_fine(),100)

    def test_set_fine(self):
        GameLogic.set_fine(200)
        self.assertEqual(GameLogic.get_fine(),200)

    def test_get_current_round(self):
        GameLogic.set_current_round(100)
        self.assertEqual(GameLogic.get_current_round(), 100)

    def test_set_current_round(self):
        GameLogic.set_current_round(200)
        self.assertEqual(GameLogic.get_current_round(), 200)

    def test_store_current_game(self):
        self.fail()


