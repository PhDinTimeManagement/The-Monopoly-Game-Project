from unittest import TestCase
from src.Model.Gameboard import *
from src.Model.Player import *

player1 = Player("Tommy")
player2 = Player("Chloe")

wan_chai = Property("Wan Chai", 3, 1000, 300, None, "Red")
go = Go(1500)
go_to_jail = GoToJail(12)
player_list = [player1, player2]
jail = Jail(3, [])
chance = Chance(10)
free_parking = FreeParking(9)

gameboard_testing = Gameboard()


class TestProperty(TestCase):

    def test_get_owner_obj(self):
        self.assertEqual(Property.get_owner_obj(player_list, player1.get_name()), player1)

    def test_can_buy(self):
        player1.set_current_money(1500)
        self.assertTrue(wan_chai.can_buy(player1))
        player1.set_current_money(500)
        self.assertFalse(wan_chai.can_buy(player1))

    def test_buy(self):
        player1.set_current_money(1500)
        result, message = wan_chai.buy(player1)
        self.assertTrue(result)
        result, message = wan_chai.buy(player1)
        self.assertFalse(result)

    def test_set_owner(self):
        wan_chai.set_owner(player1)
        self.assertEqual(player1, wan_chai.get_owner())

    def test_player_landed(self):
        wan_chai.set_owner(None)
        player1.set_current_money(1500)
        wan_chai.player_landed(player1, "buy", None)
        self.assertEqual(player1.get_current_money(), 500)
        wan_chai.set_owner(player1)
        player2.set_current_money(1500)
        wan_chai.player_landed(player2, "rent", player1)
        self.assertEqual(player2.get_current_money(), 1200)
        self.assertEqual(player1.get_current_money(), 800)
        self.assertEqual(wan_chai.player_landed(player1, None, player1), None)
        player1.set_current_money(1500)
        player2.set_current_money(1500)

    def test_pay_rent(self):
        starting_balance = player1.get_current_money()
        wan_chai.set_owner(player1)
        player2.set_current_money(300)
        money_left, message = wan_chai.pay_rent(player2, player1)
        self.assertGreaterEqual(money_left, 0)
        money_left, message = wan_chai.pay_rent(player2, player1)
        self.assertLess(money_left, 0)
        self.assertEqual(player1.get_current_money(), wan_chai.get_rent() + starting_balance)
        # print(f"{player1.get_name()} current balance is: {player1.get_current_money()} HKD")

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
        JailTile = gameboard_testing.get_jail_tile()
        player_list1 = [player1, player2]
        JailTile.set_jailed_players(player_list1)
        jailed_list = [player.get_name() for player in player_list1]

        self.assertListEqual(JailTile.get_jailed_players(), jailed_list)
        JailTile.free_player(player2)
        jailed_list.remove(player2.get_name())
        self.assertListEqual(JailTile.get_jailed_players(), jailed_list)
        JailTile.free_player(player1)
        jailed_list.remove(player1.get_name())
        self.assertListEqual(JailTile.get_jailed_players(), [])

    def test_player_landed(self):
        self.assertEqual(jail.player_landed(player1), None)


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
        JailTile = gameboard_testing.get_jail_tile()
        go_to_jail.player_landed(player1, JailTile)
        go_to_jail.player_landed(player2, JailTile)

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
        player3.set_current_money(1500)
        taxTile.set_income_tax(10)
        self.assertEqual(taxTile.calculate_tax(player3), 150)

    def test_player_landed(self):
        starting_balance = player1.get_current_money()
        tax_calculated = taxTile.calculate_tax(player1)
        taxTile.player_landed(player1)
        self.assertEqual(starting_balance - player1.get_current_money(), tax_calculated)

    def test_get_jail_tile(self):
        self.assertTrue(gameboard_testing.get_jail_tile().name, "Jail")


class TestTile(TestCase):
    def test_player_landed(self):
        self.assertEqual(Tile.player_landed(player1), None)


class TestChance(TestCase):
    def test_player_landed(self):
        player1.set_current_money(1500)
        random.seed(100)  # 0
        chance.player_landed(player1)
        self.assertEqual(player1.get_current_money(), 1360)
        random.seed(120)  # 1
        chance.player_landed(player1)
        self.assertEqual(player1.get_current_money(), 1390)
        player1.set_current_money(1500)


class TestFreeParking(TestCase):
    def test_player_landed(self):
        self.assertEqual(free_parking.player_landed(player1), None)


class TestGameboard(TestCase):
    gameboard_testing = Gameboard()
    def test_clear_owner(self):
        gameboard_testing.tiles[1].set_owner(player1)
        self.assertEqual(gameboard_testing.tiles[1].get_owner(), player1)
        gameboard_testing.clear_owner()
        self.assertEqual(gameboard_testing.tiles[1].get_owner(), None)

