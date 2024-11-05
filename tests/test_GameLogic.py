from unittest import TestCase

from src.Model.GameLogic import *
from src.Model.Player import *
from src.Model.Gameboard import *

player1 = Player("Den")
player2 = Player("Ben")
player3 = Player("Ken")
player4 = Player("Wen")
player5 = Player("Ren")
player6 = Player("Jen")
player7 = Player("Sam")
player8 = Player("Yam")

gameboard = Gameboard()
gameboard.tiles[4] = Jail(4, [player1])
game_logic =GameLogic()
players_list = []
broke_list = []

class TestGameLogic(TestCase):
    def test_roll_dice(self):
        number1, number2 = GameLogic.roll_dice()
        self.assertLessEqual(number1, 4)
        self.assertLessEqual(number2, 4)

    def test_player_move(self):
        GameLogic.player_move(3, player3, gameboard)
        self.assertEqual(player3.get_current_money(), 1350)
        GameLogic.player_move(20, player4, gameboard)
        self.assertEqual(player4.get_current_money(), 3000)
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
        number3 = 9
        number4 = 9
        self.assertTrue(GameLogic.same_double(number3, number4))
        self.assertFalse(GameLogic.same_double(number1, number2))

    def test_out_jail_on_double(self):
        gameboard.get_jail_tile().set_jailed_players([player1, player2])
        GameLogic.out_jail_on_double(player1, 4, 4, gameboard)
        self.assertFalse(player1.get_jail_status())
        self.assertFalse(player1.get_fine_payed())
        self.assertListEqual(gameboard.get_jail_tile().get_jailed_players(), ["Ben"])

    def test_pay_fine(self):
        original = player1.get_current_money()
        GameLogic.pay_fine(game_logic,player1)
        self.assertTrue(player1.get_fine_payed())
        self.assertEqual(player1.get_current_money(), original -game_logic.get_fine())

    def test_player_broke(self):
        self.assertFalse(GameLogic.player_broke(player1))
        player1.set_current_money(-100)
        self.assertTrue(GameLogic.player_broke(player1))

    def test_player_out(self):
        players_list.clear()
        players_list.append(player1)
        GameLogic.player_out(game_logic,player1, players_list, broke_list)
        self.assertFalse(player1 in players_list)
        self.assertTrue(player1 in broke_list)

    def test_game_ends(self):
        players_list.clear()
        players_list.append(player1)
        self.assertTrue(GameLogic.game_ends(players_list, 1))
        players_list.remove(player1)
        self.assertTrue(GameLogic.game_ends(players_list, 100))

    def test_get_fine(self):
        game_logic.set_fine(100)
        self.assertEqual(game_logic.get_fine(), 100)

    def test_set_fine(self):
        game_logic.set_fine(200)
        self.assertEqual(game_logic.get_fine(), 200)

    def test_get_current_round(self):
        game_logic.set_current_round(100)
        self.assertEqual(game_logic.get_current_round(), 100)

    def test_set_current_round(self):
        game_logic.set_current_round(200)
        self.assertEqual(game_logic.get_current_round(), 200)

    def test_display_winner(self):
        players_list.clear()
        players_list.append(player1)
        player1.set_current_money(1000)
        self.assertEqual(GameLogic.display_winner(game_logic,players_list),
                         f"The winner is: Den, with {players_list[0].get_current_money()} money.")
        players_list.append(player2)
        player2.set_current_money(1000)
        game_logic.set_current_round(100)
        self.assertEqual(GameLogic.display_winner(game_logic,players_list),
                         f"The winner is: Den, Ben, with {players_list[0].get_current_money()} money.")

    def test_get_player_turn(self):
        players_list.clear()
        players_list.append(player6)
        players_list.append(player7)
        players_list.append(player8)
        for i in range(2):
            game_logic.set_player_turn(players_list)
        game_logic.player_out(game_logic,player7, players_list, broke_list)
        game_logic.set_player_turn(players_list)
        self.assertEqual(game_logic.get_player_turn(), 1)
        for i in range(2):
            game_logic.set_player_turn(players_list)
        self.assertEqual(game_logic.get_player_turn(), 1)

    def test_set_player_turn(self):
        players_list.append(player1)
        players_list.append(player2)
        game_logic.set_player_turn(players_list)
        self.assertEqual(game_logic.get_player_turn(), 1)

    def test_get_remove_last_round(self):
        self.fail()

    def test_set_removed_last_round(self):
        self.fail()
