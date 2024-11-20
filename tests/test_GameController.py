from unittest import TestCase

import _tkinter

from src.Controller.GameController import *
from src.Model.Player import *
from unittest.mock import Mock, patch
import tkinter as tk


#
# gui = GUI()

# TestGameController.gui.attributes('-alpha', 0)

class TestGameController(TestCase):
    is_delete = False

    @classmethod
    def setUpClass(cls):
        cls.is_delete = False
        cls.gui = GUI()
        cls.gui.attributes('-alpha', 0)

    def setUp(self):
        if TestGameController.is_delete:
            print("set_up")
            TestGameController.gui = GUI()
            TestGameController.gui.attributes('-alpha', 0)
            TestGameController.is_delete = False

    def test_set_player_list(self):
        test_controller1 = GameController(TestGameController.gui)
        Player1 = Player("Player 1")
        Player2 = Player("Player 2")
        player_list = [Player1, Player2]
        test_controller1.set_player_list([Player1, Player2])
        self.assertListEqual(test_controller1.get_player_list(), player_list)

    def test_save_game(self):
        test_controller = GameController(TestGameController.gui)

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
        test_controller.board.tiles[15].player_landed(Player3, jailTile)

        save_name = "SAVE_LOAD_TEST"
        test_controller.save_game(save_name)

    def test_load_game(self):
        # runs the save test first to generate the test file in case it's missing
        TestGameController.test_save_game(self)

        local_controller = GameController(TestGameController.gui)

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
        test_controller = GameController(TestGameController.gui)
        tile = test_controller.board.tiles
        tile[0].set_tile_name("Start")
        tile[0].set_pass_prize(3000)
        tile[3].set_income_tax(50)
        tile[1].set_color("red")

        save_name = "TEST_GAMEBOARD_SETUP_SAVE"
        test_controller.save_gameboard(save_name)

    # ---------- Test for Main Frame ----------#

    def test_load_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.load_button()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["load_game"].winfo_ismapped())

    # ---------- Test for Load Game Frame -----------#
    def test_select_load_game_slot(self):
        test_controller = GameController(TestGameController.gui)
        before = TestGameController.gui.load_game_frame.slot_item_ids
        ref = TestGameController.gui.load_game_canvas.itemcget(before[1], 'image')
        ref2 = TestGameController.gui.load_game_canvas.itemcget(before[2], 'image')
        test_controller.select_load_game_slot(1)
        self.assertEqual(
            TestGameController.gui.load_game_canvas.itemcget(TestGameController.gui.load_game_frame.slot_item_ids[2],
                                                             'image')
            , ref2)
        self.assertNotEqual(
            TestGameController.gui.load_game_canvas.itemcget(TestGameController.gui.load_game_frame.slot_item_ids[1],
                                                             'image')
            , ref)

    def test_load_and_start_game_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.load_and_start_game_button(1)
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["gameplay"].winfo_ismapped())

    def test_load_game_back_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.load_game_back_button()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["main_menu"].winfo_ismapped())

    # ---------- Test for Load Board Frame ----------#

    # ---------- Test for New Game Frame ----------#
    def test_new_game_load_board_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.new_game_load_board_button()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["load_board"].winfo_ismapped())

    # ---------- Test for Edit Board Frame ----------#
    def test_edit_back_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.edit_board_function()
        GameplayFrame.tile_info[1][1] = "Causeway Bay"
        GameplayFrame.tile_colors[1][0] = "pink"
        test_controller.edit_back_button()
        self.assertEqual(GameplayFrame.tile_info, test_controller.temp_tile_info)
        self.assertEqual(GameplayFrame.tile_colors, test_controller.temp_color_info)

    def test_apply_changes_button(self):
        test_controller = GameController(TestGameController.gui)
        GameplayFrame.tile_info.clear()
        GameplayFrame.tile_colors.clear()
        test_controller.edit_board_function()
        GameplayFrame.tile_info[1][1] = "Tai Po"
        test_controller.apply_changes_button()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["edit_board"].winfo_ismapped())
        GameplayFrame.tile_info[1][1] = "Causeway Bay"
        test_controller.apply_changes_button()
        self.assertEqual(GameplayFrame.tile_info[1][1], "Causeway Bay")

    def test_save_board_profile_button(self):
        test_controller = GameController(TestGameController.gui)
        GameplayFrame.tile_info.clear()
        GameplayFrame.tile_colors.clear()
        test_controller.edit_board_function()
        GameplayFrame.tile_info[2][1] = "Central"
        test_controller.save_board_profile_button()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["edit_board"].winfo_ismapped())
        GameplayFrame.tile_info[2][1] = "Lamma Island"
        test_controller.save_board_profile_button()
        self.assertEqual(GameplayFrame.tile_info[2][1], "Lamma Island")

    def test_reset_changes_button(self):
        test_controller = GameController(TestGameController.gui)
        GameplayFrame.tile_info.clear()
        GameplayFrame.tile_colors.clear()
        test_controller.edit_board_function()
        GameplayFrame.tile_info[19][1] = "Tai Po"
        GameplayFrame.tile_colors[2][0] = "blue"
        test_controller.reset_changes_button()
        self.assertEqual([row[0:2] for row in GameplayFrame.tile_info],
                         [row[0:2] for row in test_controller.temp_tile_info])
        self.assertEqual([row[0:1] for row in GameplayFrame.tile_colors],
                         [row[0:1] for row in test_controller.temp_color_info])

    # ---------- Test for Save Board Frame ----------#
    def test_select_saved_board_slot(self):
        test_controller = GameController(TestGameController.gui)
        before = TestGameController.gui.save_board_frame.slot_item_ids
        ref1 = TestGameController.gui.save_board_canvas.itemcget(before[1], 'image')
        ref2 = TestGameController.gui.save_board_canvas.itemcget(before[2], 'image')
        test_controller.select_saved_board_slot(TestGameController.gui.save_board_canvas, 1)
        self.assertEqual(
            TestGameController.gui.save_board_canvas.itemcget(TestGameController.gui.save_board_frame.slot_item_ids[2],
                                                              'image')
            , ref2)
        self.assertNotEqual(
            TestGameController.gui.save_board_canvas.itemcget(TestGameController.gui.save_board_frame.slot_item_ids[1],
                                                              'image')
            , ref1)

    def test_back_to_edit_board_frame(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.edit_board_function()
        test_controller.back_to_edit_board_frame()
        coords = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.delete_button_id)
        coords2 = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.save_button_id)
        self.assertEqual(coords, [-100, -100])
        self.assertEqual(coords2, [-100, -100])

    def test_home_in_edit_board(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.edit_board_function()
        test_controller.home_in_edit_board()
        coords = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.delete_button_id)
        coords2 = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.save_button_id)
        self.assertEqual(coords, [-100, -100])
        self.assertEqual(coords2, [-100, -100])
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["new_game"].winfo_ismapped())

    def test_open_board_enter_name_file_frame(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.open_board_enter_name_file_frame()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["enter_name"].winfo_ismapped())

    # ----------- Test for Save Game Frame ----------#
    def test_home_button(self):
        test_controller = GameController(TestGameController.gui)
        reference_board = Gameboard()
        test_controller.home_button()
        self.assertEqual([row.tile_type for row in test_controller.board.tiles],
                         [row.tile_type for row in reference_board.tiles])
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["main_menu"].winfo_ismapped())

    def test_back_to_game_play_frame(self):
        test_controller = GameController(TestGameController.gui)
        TestGameController.gui.input_handler.validate_and_store_name(1, "player1")
        self.assertTrue(TestGameController.gui.input_handler.validate_and_store_name(2, "player2"))
        self.assertFalse(
            TestGameController.gui.input_handler.validate_and_store_name(1, "This name is more than twenty characters"))
        self.assertTrue(TestGameController.gui.input_handler.generate_name())

        test_controller.button_play(False)
        test_controller.save_quit_button()
        test_controller.back_to_game_play_frame()
        coords = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.delete_button_id)
        coords2 = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.save_button_id)
        self.assertEqual(coords, [-100, -100])
        self.assertEqual(coords2, [-100, -100])

    # Test whether the saved game slot are selected and highlighted after the click
    def test_select_saved_game_slot(self):
        test_controller = GameController(TestGameController.gui)
        before = TestGameController.gui.save_game_frame.slot_item_ids
        ref = TestGameController.gui.save_game_canvas.itemcget(before[1], 'image')
        ref2 = TestGameController.gui.save_game_canvas.itemcget(before[2], 'image')
        test_controller.select_saved_game_slot(TestGameController.gui.save_game_canvas, 1)
        self.assertEqual(
            TestGameController.gui.save_game_canvas.itemcget(TestGameController.gui.save_game_frame.slot_item_ids[2],
                                                             'image')
            , ref2)
        self.assertNotEqual(
            TestGameController.gui.save_game_canvas.itemcget(TestGameController.gui.save_game_frame.slot_item_ids[1],
                                                             'image')
            , ref)

    def test_open_enter_name_file_frame(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.open_enter_name_file_frame()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["enter_name"].winfo_ismapped())

    # ---------- Test for Gameplay Frame ----------#

    # def test_determine_next_round(self):
    #     self.fail()
    #
    # def test_land_and_complete_round(self):
    #     self.fail()

    # Close the existing gui(root)
    @staticmethod
    def close_gui_window(message):
        print(message)
        TestGameController.gui.destroy()
        TestGameController.is_delete = True

    # Game set up (initialization) for testing
    @staticmethod
    def game_set_up(test_controller, seed):
        test_controller.game_logic = GameLogic()
        TestGameController.gui.input_handler = InputHandler()
        test_controller.input_handler = TestGameController.gui.input_handler
        TestGameController.gui.gameplay_frame.player_info.clear()
        TestGameController.gui.input_handler.validate_and_store_name(0, "player1")
        TestGameController.gui.input_handler.validate_and_store_name(1, "player2")
        test_controller.button_play(False)
        random.seed(seed)
        player_this_turn = test_controller.get_player_list()[test_controller.game_logic.get_player_turn()]
        return player_this_turn

    # Test the player is able to roll when they are not inside of jail
    @patch('tkinter.Tk.wait_variable')
    def test_roll_dice(self, mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 2)
        mock_wait_variable.side_effect = lambda var: var.set("buy")
        test_controller.roll_dice(player_this_turn)
        player_this_turn_1 = test_controller.get_player_list()[test_controller.game_logic.get_player_turn() + 1]
        test_controller.roll_dice(player_this_turn_1)
        message = "Temporary Close the App"
        TestGameController.gui.after(4000, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(test_controller.board.tiles[player_this_turn.get_current_position()].get_tile_type(),
                         "property")
        self.assertEqual(test_controller.board.tiles[player_this_turn_1.get_current_position()].get_tile_type(), "jail")

    @patch('tkinter.Tk.wait_variable')
    # Test on double, out of jail straight away
    def test_in_jail_roll_double(self,mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 2)  # On double
        GoToJail.arrest_player(player_this_turn, test_controller.board.get_jail_tile())
        self.assertEqual(test_controller.board.tiles[player_this_turn.get_current_position()].get_tile_type(),
                         "jail")
        mock_wait_variable.side_effect = lambda var: var.set("buy")
        test_controller.in_jail_roll(player_this_turn)
        message = "On double Jail Roll"
        TestGameController.gui.after(8000, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(test_controller.board.tiles[player_this_turn.get_current_position()].get_tile_type(),
                         "property")

    @patch('tkinter.Tk.wait_variable')
    # Test when the player have enough money to pay for the fine at the third round of jail
    def test_in_jail_pay_fine_not_broke(self, mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 4)
        GoToJail.arrest_player(player_this_turn, test_controller.board.get_jail_tile())
        player_this_turn.set_in_jail_turns(1)
        player_this_turn.set_current_money(200)
        mock_wait_variable.side_effect = lambda var: var.set("test_pay_fine")
        test_controller.in_jail_roll(player_this_turn)
        message = "Third Turn Pay Fine"
        TestGameController.gui.after(4500, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(player_this_turn.get_current_money(), 50)

    # Test when the player does not have enough money to pay the fine and get out of jail, and determine the winner
    @patch('tkinter.Tk.wait_variable')
    def test_player_in_jail_pay_fine_broke(self,mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 4)
        GoToJail.arrest_player(player_this_turn, test_controller.board.get_jail_tile())
        player_this_turn.set_in_jail_turns(1)
        player_this_turn.set_current_money(10)
        mock_wait_variable.side_effect = lambda var: var.set("test_pay_fine")
        test_controller.in_jail_roll(player_this_turn)
        message = "Third Turn Pay Fine and broke"
        TestGameController.gui.after(4500, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(player_this_turn.get_current_money(), -140)
        self.assertTrue(player_this_turn in test_controller.broke_list)
        self.assertEqual(test_controller.player_list[0].get_name(),"player2")


    def test_player_in_jail_not_moved (self):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 4)
        GoToJail.arrest_player(player_this_turn, test_controller.board.get_jail_tile())
        current_tile = player_this_turn.get_current_position()
        test_controller.in_jail_roll(player_this_turn)
        message = "Player in jail not moved"
        TestGameController.gui.after(4500, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(current_tile,player_this_turn.get_current_position())


    # ----------- Test for Edit File Name Frame ----------#

    # ----------- Enter Board Name Frame -----------#
    def test_show_saved_board_name(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.pass_tile_information_for_display()
        test_controller.pass_color_information_for_display()
        TestGameController.gui.selected_saved_game_slot = 1
        TestGameController.gui.show_frame("enter_name")
        TestGameController.gui.enter_file_name_frame.name_entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.enter_file_name_frame.name_entry.insert(0, "This is a word more than 20 characters")
        test_controller.show_saved_board_name()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["enter_name"].winfo_ismapped())
        TestGameController.gui.enter_file_name_frame.name_entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.enter_file_name_frame.name_entry.insert(0, "Valid Save Name")
        test_controller.show_saved_board_name()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["save_board"].winfo_ismapped())

    def test_enter_board_name_back_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.enter_board_name_back_button()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["save_board"].winfo_ismapped())

    # ----------- Load Board Frame Button ----------#

    def test_select_load_board_slot(self):
        test_controller = GameController(TestGameController.gui)
        before = TestGameController.gui.load_board_frame.slot_item_ids
        ref = TestGameController.gui.load_board_canvas.itemcget(before[1], 'image')
        ref2 = TestGameController.gui.load_board_canvas.itemcget(before[2], 'image')
        test_controller.select_load_board_slot(1)
        self.assertEqual(
            TestGameController.gui.load_board_canvas.itemcget(TestGameController.gui.load_board_frame.slot_item_ids[2],
                                                              'image')
            , ref2)
        self.assertNotEqual(
            TestGameController.gui.load_board_canvas.itemcget(TestGameController.gui.load_board_frame.slot_item_ids[1],
                                                              'image')
            , ref)

    def condition_for_load_board(self, board_name):
        if board_name is not None:
            TestGameController.gui.enter_file_name_frame.name_entry.insert(0, board_name)
            return True
        return False

    def test_load_board_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.load_board_button(5)
        reference_board = Gameboard()
        self.assertEqual([row.tile_type for row in test_controller.board.tiles],
                         [row.tile_type for row in reference_board.tiles])
        test_controller = GameController(TestGameController.gui)
        test_controller.load_board_button(1)
        board_info1 = test_controller.board
        self.condition_for_load_board(board_info1)
        test_controller.load_board_button(4)
        board_info = test_controller.board
        board_name = TestGameController.gui.load_board_frame.load_data(4)
        TestGameController.gui.enter_file_name_frame.name_entry = tk.Entry(TestGameController.gui)
        self.condition_for_load_board(board_name)
        TestGameController.gui.selected_saved_game_slot = 4
        TestGameController.gui.save_board_frame.delete_data(TestGameController.gui.save_board_canvas)
        test_controller.board = board_info
        test_controller.show_saved_board_name()
        TestGameController.gui.update()
        time.sleep(0.5)
        self.assertTrue(TestGameController.gui.frames["new_game"].winfo_ismapped())




