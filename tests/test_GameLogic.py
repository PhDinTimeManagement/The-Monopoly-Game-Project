from unittest import TestCase

from src.Model.GameLogic import *
from src.Model.Player import *
from src.Model.Gameboard import *

player1 = Player("Den")
player2 = Player("Ben")
player3 = Player("Ken")
player4 = Player("Wen")
player5 = Player("Ren")
gameboard = Gameboard()
gameboard.tiles[4] = Jail(4, [player1])


class TestGameLogic(TestCase):
    def test_roll_dice(self):
        number1, number2 = GameLogic.roll_dice()
        self.assertLessEqual(number1, 4)
        self.assertLessEqual(number2, 4)

    def test_player_move(self):
        GameLogic.player_move(3, player3, gameboard)
        self.assertEqual(player3.get_current_money(),1350)
        GameLogic.player_move(20,player4, gameboard)
        self.assertEqual(player4.get_current_money(),3000)
        GameLogic.player_move(23, player5, gameboard)
        self.assertEqual(player5.get_current_money(), 2700)

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
        number1 = 7
        number2 = 3
        number3 =9
        number4 =9
        self.assertTrue(GameLogic.same_double(number3, number4))
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
        self.assertTrue(player1 in Player.players_list)
        self.assertTrue(player1 in Player.broke_list)

    def test_game_ends(self):
        Player.players_list.append(player1)
        self.assertTrue(GameLogic.game_ends(Player.players_list,1))
        Player.players_list.remove(player1)
        self.assertTrue(GameLogic.game_ends(Player.players_list,100))

    def test_get_fine(self):
        GameLogic.set_fine(100)
        self.assertEqual(GameLogic.get_fine(), 100)

    def test_set_fine(self):
        GameLogic.set_fine(200)
        self.assertEqual(GameLogic.get_fine(), 200)

    def test_get_current_round(self):
        GameLogic.set_current_round(100)
        self.assertEqual(GameLogic.get_current_round(), 100)

    def test_set_current_round(self):
        GameLogic.set_current_round(200)
        self.assertEqual(GameLogic.get_current_round(), 200)

    def test_display_winner(self):
        Player.players_list.clear()
        Player.players_list.append(player1)
        player1.set_current_money(1000)
        self.assertEqual(GameLogic.display_winner(Player.players_list),
                         f"The winner is: Den, with {Player.players_list[0].get_current_money()} money.")
        Player.players_list.append(player2)
        player2.set_current_money(1000)
        GameLogic.set_current_round(100)
        self.assertEqual(GameLogic.display_winner(Player.players_list),
                         f"The winner is: Den, Ben, with {Player.players_list[0].get_current_money()} money.")

    def test_get_player_turn(self):
        Player.players_list.append(player1)
        Player.players_list.append(player2)
        GameLogic.set_current_round(98)
        GameLogic.set_player_turn()
        self.assertEqual(GameLogic.get_player_turn(),1)

    def test_set_player_turn(self):
        Player.players_list.append(player1)
        Player.players_list.append(player2)
        GameLogic.set_current_round(1)
        GameLogic.set_player_turn()
        self.assertEqual(GameLogic.get_player_turn(), 0)
