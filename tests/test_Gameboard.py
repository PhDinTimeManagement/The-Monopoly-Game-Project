from unittest import TestCase
from src.Model.Gameboard import *
from src.Model.Player import *

player1 = Player("Tommy")
player2 = Player("Chloe")

wan_chai = Property("Wan Chai", 3, 1000, 300, None, "Red")
go = Go(1500)
go_to_jail = GoToJail(12)

gameboard = Gameboard()


class TestProperty(TestCase):
    def test_construction(self):
        assert Property("Wan Chai", 3, 1000, 100, None, "Red")
        assert GoToJail(10)
        assert Jail(4, [])
        assert Chance(15)
        assert Go(1500)
        assert IncomeTax(3, 10)
        assert FreeParking(14)

    def test_can_buy(self):
        self.assertEqual(wan_chai.can_buy(player1), True)
        self.assertEqual(wan_chai.can_buy(player1), False)

    def test_buy(self):
        self.assertEqual(wan_chai.buy(player1), True)
        self.assertEqual(wan_chai.buy(player1), False)

    def test_set_owner(self):
        wan_chai.set_owner(player1)
        self.assertEqual(player1, wan_chai.get_owner())

    def test_pay_rent(self):
        starting_balance = player1.get_current_money()
        self.assertGreaterEqual(wan_chai.pay_rent(player2), 0)
        self.assertGreaterEqual(wan_chai.pay_rent(player2), 0)
        self.assertGreaterEqual(wan_chai.pay_rent(player2), 0)
        self.assertGreaterEqual(wan_chai.pay_rent(player2), 0)
        self.assertGreaterEqual(wan_chai.pay_rent(player2), 0)
        self.assertLess(wan_chai.pay_rent(player2), 0)
        self.assertEqual(player1.get_current_money(), wan_chai.get_rent() * 5 + starting_balance)
        print(f"{player1.get_name()} current balance is: {player1.get_current_money()} HKD")

    def test_update_values(self):
        testUpdate = Property("Wan Chai", 3, 1000, 100, None, "Red")
        testUpdate.update_name_pos_type("NEW", 0)
        testUpdate.update_values(0, 0, player1, "Pink")
        assert testUpdate.get_property_name() == "NEW"
        assert testUpdate.get_tile_position() == 0
        assert testUpdate.get_price() == 0
        assert testUpdate.get_rent() == 0
        assert testUpdate.get_owner() == player1
        assert testUpdate.get_color() == "Pink"


class TestJail(TestCase):
    def test_set_jailed_players(self):
        self.assertEqual(JailTile.get_jailed_players(), [player1, player2])
        JailTile.free_player(player2)
        self.assertEqual(JailTile.get_jailed_players(), [player1])
        JailTile.free_player(player1)
        self.assertEqual(JailTile.get_jailed_players(), [])


class TestGo(TestCase):
    def test_set_pass_prize(self):
        go.set_pass_prize(2000)
        self.assertEqual(go.get_pass_prize(), 2000)

    def test_player_landed(self):
        starting_balance = player1.get_current_money()
        go.player_landed(player1)
        self.assertEqual(player1.get_current_money(), starting_balance + go.get_pass_prize())
        player1.set_current_money(starting_balance)


class TestGoToJail(TestCase):
    def test_player_landed(self):
        go_to_jail.player_landed(player1)
        go_to_jail.player_landed(player2)

    def test_update_values(self):
        testUpdate = GoToJail(10)
        testUpdate.update_name_pos_type("NEW", 13)
        assert testUpdate.get_tile_position() == 13
        assert testUpdate.get_tile_name() == "NEW"


taxTile = IncomeTax(3, 10)


class TestIncomeTax(TestCase):
    def test_set_income_tax(self):
        taxTile.set_income_tax(20)
        self.assertEqual(taxTile.tax_percentage, 20)
        taxTile.set_income_tax(10)

    def test_calculate_tax(self):
        player3 = Player("Max")
        taxTile.set_income_tax(10)
        self.assertEqual(taxTile.calculate_tax(player3), 150)

    def test_player_landed(self):
        starting_balance = player1.get_current_money()
        tax_calculated = taxTile.calculate_tax(player1)
        taxTile.player_landed(player1)
        self.assertEqual(starting_balance - player1.get_current_money(), tax_calculated)

    def test_get_jail_tile(self):
        self.assertTrue(gameboard.get_jail_tile().name, "Jail")



