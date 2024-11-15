# GameController.py

import json
import os.path
import time

from src.Model.Gameboard import *
from src.Model.Player import *
from src.Model.GameLogic import GameLogic
from datetime import datetime
from src.View.GUI import *
from tests.test_GameLogic import players_list, gameboard


class GameController:
    def __init__(self, the_gui):
        self.save_name = None
        self.board = Gameboard()
        self.game_logic = GameLogic()
        self.gui = the_gui
        self.player_list = []
        self.broke_list = []
        self.all_players = []
        self.input_handler = self.gui.input_handler
        self.click_var = tk.StringVar()
        self.new_name_frame = self.gui.new_game_frame

        #store the function related to all the buttons to an array for better initialization in button_play
        self.function_array = [self.roll_dice,self.buy_button,self.no_buy_button]

        #binding the buttons
        self.gui.new_game_canvas.tag_bind(self.gui.play_button_clickable_area, "<Button-1>", lambda e: self.button_play(False))

        # TODO same function is also called in play_button IS NECESSARY?
        self.pass_gameboard_info_to_view()
        self.gui.show_edit_board_frame()

        #bind the load game button here
        self.bind_load_game()

    #To clear all the data when loading ot starting a new game
    def clear_all_data(self):
        self.player_list.clear()
        self.broke_list.clear()
        self.all_players.clear()
        self.gui.gameplay_frame.player_info.clear()
        self.gui.gameplay_frame.tile_info.clear()
        self.click_var = tk.StringVar()
        self.gui.gameplay_frame.player_info.clear()
        self.board.clear_owner()
        self.input_handler.reset_players_names()

    def get_player_list(self):
        return self.player_list

    def set_player_list(self, player_list):
        self.player_list = player_list.copy()

    def get_broke_player_list(self):
        return self.broke_list

    def set_broke_player_list(self, broke_list):
        self.broke_list = broke_list.copy()

    def get_current_round(self):
        return self.game_logic.get_current_round()

    def get__turn(self):
        return self.game_logic.get_player_turn()

    def set__turn(self, turn):
        self.game_logic._player_turn = turn

    def set_current_round(self, new_round):
        self.game_logic.set_current_round(new_round)

    def set_save_name(self, save_name):
        self.save_name = save_name

    def set_remove_last_round(self, remove_last_round):
        self.game_logic.set_removed_last_round(remove_last_round)

    def pass_tile_information_for_display(self):
        for i in range(0, 20):
            # type, name, price, rent, owner,
            empty_9tuple = [None, None, None, None, None, None, None, None, None]
            # creates new empty row
            self.gui.gameplay_frame.tile_info.append(empty_9tuple)

            # for easier reading of code
            tile_info = self.gui.gameplay_frame.tile_info[i]
            board_tile = self.board.tiles[i]

            # updates fields with relevant information
            tile_info[0] = board_tile.get_tile_type()
            tile_info[1] = board_tile.get_tile_name()
            if tile_info[0] == "property":
                tile_info[2] = board_tile.get_price()
                tile_info[3] = board_tile.get_rent()
                tile_info[4] = board_tile.get_owner()
            elif tile_info[0] == "go":
                tile_info[2] = board_tile.get_pass_prize()
            elif tile_info[0] == "income_tax":
                tile_info[2] = board_tile.get_income_tax()

    def update_all_game_info(self):
        self.pass_updated_tile_ownership_info()
        self.pass_updated_players_info()
        self.gui.gameplay_frame.update_display_info(self.gui.game_canvas)

    # for each tile in the
    def pass_updated_tile_ownership_info(self):
        # checks only the property positions
        for i in [1, 2, 4, 6, 7, 9, 11, 13, 14, 16, 17, 19]:
            board_tile = self.board.tiles[i]
            tile_info = self.gui.gameplay_frame.tile_info[i]
            tile_info[4] = board_tile.get_owner()

    def pass_updated_players_info(self):
        for i in range(0, len(self.all_players)):
            self.gui.gameplay_frame.player_info[i][1] = self.all_players[i].get_current_money()
            curr_pos = self.all_players[i].get_current_position()
            self.gui.gameplay_frame.player_info[i][2] = self.board.tiles[curr_pos].get_tile_name()
            self.gui.gameplay_frame.player_info[i][3] = self.all_players[i].get_jail_status()
            self.gui.gameplay_frame.player_info[i][4] = self.all_players[i].get_in_jail_turns()
            self.gui.gameplay_frame.player_info[i][5] = len(self.all_players[i].get_properties_list())
            self.gui.gameplay_frame.player_info[i][6] = curr_pos

    def pass_player_information_to_view(self):
        self.gui.gameplay_frame.player_turn = self.game_logic.get_player_turn()
        for i in range(0, len(self.all_players)):
            # info passed: [name, balance, positionName, isJailed, inJailTurns, #propOwned, positionInt]
            player_tuple = [None, None, None, None, None, None, None]
            self.gui.gameplay_frame.player_info.append(player_tuple)    #adds new 6-tuple
            self.gui.gameplay_frame.player_info[i][0] = self.all_players[i].get_name()
        self.pass_updated_players_info()

    def pass_color_information_for_display(self):
        for i in range(0, 20):
            color_tuple = [None, None]
            self.gui.gameplay_frame.tile_colors.append(color_tuple)
            has_color = self.gui.gameplay_frame.get_color_coord(i)
            if has_color:
                color = self.board.tiles[i].get_color()
                self.gui.gameplay_frame.set_color(i, color)

    # passes necessary information to the gui and creates missing frames
    def pass_gameboard_info_to_view(self):
        self.pass_color_information_for_display()
        self.pass_tile_information_for_display()

    # ----------Hiding logic in controller----------#
    def hide_load_and_save_image(self):
        self.gui.load_game_frame.hide_load_image(self.gui.load_game_canvas)

    def hide_roll_image(self):
        self.gui.gameplay_frame.hide_roll_image(self.gui.game_canvas)

    def hide_yes_buy_image(self):
        self.gui.gameplay_frame.hide_yes_image(self.gui.game_canvas)
        # bind 'buy'

    def hide_no_buy_image(self):
        self.gui.gameplay_frame.hide_no_image(self.gui.game_canvas)

    def hide_pay_fine_image(self):
        self.gui.gameplay_frame.hide_pay_fine_image(self.gui.game_canvas)

    def hide_save_quit_image(self):
        self.gui.gameplay_frame.hide_save_quit_image(self.gui.game_canvas)

    def unbind_load_and_save_button(self):
        self.hide_load_and_save_image()
        self.gui.load_game_cvanvas.tag_unbind(self.gui.load_game_click_area[0],"<Button-1>") #position 0 is the click area of load_save button

    def unbind_roll_button(self):
        self.hide_roll_image()
        self.gui.game_canvas.tag_unbind(self.gui.game_frame_click_areas[0], "<Button-1>")

    def unbind_yes_buy_button(self):
        self.hide_yes_buy_image()
        self.gui.game_canvas.tag_unbind(self.gui.game_frame_click_areas[1], "<Button-1>")

    def unbind_no_buy_button(self):
        self.hide_no_buy_image()
        self.gui.game_canvas.tag_unbind(self.gui.game_frame_click_areas[2], "<Button-1>")

    def unbind_pay_fine_button(self, player_this_turn):
        self.hide_pay_fine_image()
        self.gui.game_canvas.tag_unbind(self.gui.game_frame_click_areas[3], "<Button-1>")

    def unbind_in_jail_roll_button(self, player_this_turn):
        self.hide_roll_image()
        self.gui.game_canvas.tag_unbind(self.gui.game_frame_click_areas[0], "<Button-1>")

    def unbind_save_quit_button(self):
        self.hide_save_quit_image()
        self.gui.game_canvas.tag_unbind(self.gui.game_frame_click_areas[4], "<Button-1>")

    def unbind_save_button(self):
        self.gui.save_game_canvas.tag_unbind(self.gui.save_delete_click_areas[0], "<Button-1>")

    def unbind_delete_button(self):
        self.gui.save_game_canvas.tag_unbind(self.gui.save_delete_click_areas[1], "<Button-1>")

    # ----------------------------------------------#

    # ----------Showing logic in controller---------#

    def show_load_and_save_image(self):
        self.gui.load_game_frame.show_load_image(self.gui.load_game_canvas)

    def show_roll_image(self):
        self.gui.gameplay_frame.show_roll_image(self.gui.game_canvas)

    def show_yes_buy_image(self):
        self.gui.gameplay_frame.show_yes_image(self.gui.game_canvas)  # show the buy(yes) image

    def show_no_buy_image(self):
        self.gui.gameplay_frame.show_no_image(self.gui.game_canvas)  # show the no_buy(no) image

    def show_pay_fine_image(self):
        self.gui.gameplay_frame.show_pay_fine_image(self.gui.game_canvas)

    def show_save_quit_image(self):
        self.gui.gameplay_frame.show_save_quit_image(self.gui.game_canvas)

    def bind_load_and_save_button(self, idx):
        self.show_load_and_save_image()
        self.gui.load_game_canvas.tag_bind(self.gui.load_game_click_areas[0], "<Button-1>",
                                 lambda e: self.load_and_start_game_button(idx) )

    def bind_load_game(self):
        self.gui.canvas.tag_bind(self.gui.load_game_click_area, "<Button-1>",
                                 lambda e: self.load_button() )

    def bind_roll_button(self, player_this_turn):
        self.show_roll_image()
        self.gui.game_canvas.tag_bind(self.gui.game_frame_click_areas[0], "<Button-1>",
                                      lambda e: self.roll_dice(player_this_turn))  # selection player next turn to roll the dice

    def bind_yes_buy_button(self):
        self.show_yes_buy_image()
        self.gui.game_canvas.tag_bind(self.gui.game_frame_click_areas[1], "<Button-1>",
                                      lambda e: self.buy_button())  # bind 'buy'

    def bind_no_buy_button(self):
        self.show_no_buy_image()
        self.gui.game_canvas.tag_bind(self.gui.game_frame_click_areas[2], "<Button-1>",
                                      lambda e: self.no_buy_button())  # bind 'not_buy'

    def bind_pay_fine_button(self, player_this_turn):
        self.show_pay_fine_image()
        self.gui.game_canvas.tag_bind(self.gui.game_frame_click_areas[3], "<Button-1>",
                                      lambda e: self.pay_fine(player_this_turn))  # bind 'not_buy'

    def bind_in_jail_roll_button(self, player_this_turn):
        self.show_roll_image()
        self.gui.game_canvas.tag_bind(self.gui.game_frame_click_areas[0], "<Button-1>",
                                      lambda e: self.in_jail_roll(player_this_turn))  # bind 'in_jail_roll'

    def bind_save_quit_button(self):
        self.show_save_quit_image()
        self.gui.game_canvas.tag_bind(self.gui.game_frame_click_areas[4], "<Button-1>",
                                          lambda e: self.save_quit_button())

    def bind_save_button(self):
        #self.gui.save_game_canvas.tag_bind(self.gui.save_delete_click_areas[0], "<Button-1>",
                                             #lambda e: self.show_save_game(save_game_name))
        self.show_save_quit_image()
        self.gui.save_game_canvas.tag_bind(self.gui.save_delete_click_areas[0], "<Button-1>",
                                           lambda e: self.open_enter_name_file_frame())

    def bind_enter_name_save_button(self):
        self.gui.enter_name_canvas.tag_bind(self.gui.enter_file_name_frame.color_save_button,"<Button-1>",
                                            lambda e: self.show_save_game())
    def bind_delete_button(self):
        self.gui.save_game_canvas.tag_bind(self.gui.save_delete_click_areas[1], "<Button-1>",
                                          lambda e: self.gui.save_game_frame.delete_data(self.gui.save_game_canvas))
    def bind_back_button(self):
        self.gui.save_game_canvas.tag_bind(self.gui.save_delete_click_areas[2], "<Button-1>",
                                           lambda e: self. back_to_game_play_frame())

    def bind_home_button(self):
        self.gui.save_game_canvas.tag_bind(self.gui.save_delete_click_areas[3], "<Button-1>",
                                           lambda e: self.home_button())

    # ---------------------------------------------------#

    #------------ Button func in Main Page --------------#
    def load_button(self):
        self.gui.load_game_frame.show_save_file(self.gui.load_game_canvas)
        self.gui.show_frame("load_game")
        #bind all the slots in the load page
        for i,slots in enumerate(self.gui.load_game_click_areas[1:]):
            self.gui.load_game_canvas.tag_bind(slots, "<Button-1>", lambda e, idx=i: self.select_slot(idx))

    # ---------------------------------------------------#

    #----------- Button func in Load Game Page ----------#
    def select_slot(self, idx):
        self.gui.load_game_frame.select_saved_slot(self.gui.load_game_canvas, idx)
        self.bind_load_and_save_button(idx)

    def load_and_start_game_button(self,idx):
        save_name = self.gui.load_game_frame.load_data(idx)
        self.clear_all_data()
        self.load_game(save_name)
        self.button_play(True)

    #----------------------------------------------------#

    #------------ Save Game Frame Button ----------------#

    def home_button(self):
        self.clear_all_data()
        """self.board = Gameboard()
        self.game_logic = GameLogic()
        self.pass_gameboard_info_to_view()"""
        self.gui.show_frame("main_menu")

    def back_to_game_play_frame(self):
        self.gui.save_game_frame.back_button(self.gui.save_game_canvas)
        self.unbind_delete_button()
        self.unbind_save_button()

    #bind a single the slots clicks with save and delete button
    def select_saved_game_slot(self,canvas,idx):
        self.gui.save_game_frame.select_saved_slot(canvas, idx)
        self.bind_delete_button()
        self.bind_save_button()

    #logic handling when the save_quit_button is clicked
    def save_quit_button(self):
        #bind all slots in the save_name frame
        for i,slots in enumerate(self.gui.save_delete_click_areas[4:]):
            self.gui.save_game_canvas.tag_bind(slots, "<Button-1>",
                            lambda e, idx=i: self.select_saved_game_slot(self.gui.save_game_canvas, idx))

        #bind the back button
        self.bind_back_button()

        self.gui.gameplay_frame.save_quit() #show the save game frame
        self.bind_home_button()

    #logic from binding and showing the buttons in enter name file
    def open_enter_name_file_frame(self):
        self.bind_enter_name_save_button()
        self.gui.show_frame("enter_name")

    """ This function is called after the 'Play' button is clicked in the game """

    def button_play(self, from_load):
        if self.new_name_frame.check_and_start_game(self.input_handler) or from_load:
            # if not from_load: #TODO bind the clear_all_data() to the home button in save game page later
            #     self.clear_all_data() #clear all the data
            print("In the Game!!!",len(self.input_handler.players_names))#TODO del this line later
            if not from_load:
                for player_name in self.input_handler.players_names:
                    if player_name is not None:
                        player = Player(player_name)
                        self.player_list.append(player)

            self.all_players = self.player_list.copy()  # maintains a record copy of all players obj to keep updating the view even after they are broke

            # passes all info to view to build the board
            self.pass_gameboard_info_to_view()
            self.pass_player_information_to_view()

            self.gui.show_game_play_frame()     # builds gameplay frame when it has all necessary information

            #The player's turn from load is already decide, but not if it was a new game
            if not from_load:
                self.game_logic.reset_player_turn() #reset the player's turn when a new game is starting
                self.game_logic.set_player_turn(self.get_player_list())

            player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]

            #display the current player who is rolling
            self.gui.gameplay_frame.highlight_current_player(self.gui.game_canvas, self.game_logic.get_player_turn())

            # Show the GameBoard frame
            self.gui.show_frame("gameplay")
            print(player_this_turn.get_name()," is now playing") #TODO del this line later
            # hide all the buttons apart from the roll button
            self.hide_yes_buy_image()
            self.hide_no_buy_image()
            self.hide_pay_fine_image()
            #bind the buttons
            self.bind_save_quit_button()

            #for 'from_load': if the player current player playing is in jail, then load the associated button
            if player_this_turn.get_jail_status():
                self.bind_in_jail_roll_button(player_this_turn)
                if not player_this_turn.get_fine_payed():
                    self.bind_pay_fine_button(player_this_turn)
            else:
                self.bind_roll_button(player_this_turn)
            # TODO <display highlight player_this_turn ONLY.>


    def determine_next_round(self, player_this_turn):
        """ Action is an array that stores the state of the Model after calling the 'determine_next_round' function """
        action, winners_list = GameLogic.determine_next_round(self.game_logic, player_this_turn, self.player_list,self.broke_list)

        if action[0] == "game_ends":
            print(action[1])
            self.update_all_game_info()
            self.gui.gameplay_frame.display_winners_on_canvas(self.gui.game_canvas, winners_list)
            # wait for click event
            return

        self.gui.gameplay_frame.highlight_current_player(self.gui.game_canvas, self.game_logic.get_player_turn())

        if action[0] == "jail_roll":
            self.bind_in_jail_roll_button(action[1])
            print("\nNext round, click roll\n")
            if action[2] == "fine_payed":
                print(action[1].get_name(), "is in Jail. Fine already paid. Can move out of Jail after roll") #TODO del
            elif action[2] == "player_third_turn":
                print(action[1].get_name(), "is in Jail, and in third turn. Roll first") #TODO del
            else:
                print(action[1].get_name(), "is in Jail, and have no money to pay fine") #TODO del
        elif action[0] == "pay_fine_and_jail_roll":
            # TODO <display jail_roll and pay fine>
            self.bind_in_jail_roll_button(action[1])
            self.bind_pay_fine_button(action[1])
            print("\nNext round, click roll\n")  # TODO del later
            print(action[1].get_name(), "Not yet paid and in Jail") #TODO del
        elif action[0] == "roll":
            self.bind_roll_button(action[1]) #selection player next turn to roll the dice
            print("Current Money: ",player_this_turn.get_current_money()) #TODO del later
            print("\nNext round,", action[1].get_name(),"'s turn. click roll\n") #TODO del later
        self.bind_save_quit_button()

    def land_and_complete_round(self, tile, player_this_turn):
        tile_type = tile.get_tile_type()
        action = None
        if tile_type == "property":
            if tile.get_owner() is None:
                can_buy = tile.can_buy(player_this_turn)
                print("buy(Yes) or not buy(No)")
                self.gui.after(1250, lambda: self.bind_no_buy_button()) #show and bind the no(buy) button
                if can_buy:
                    self.gui.after(1250, lambda: self.bind_yes_buy_button()) #show and bind the yes(buy) button
                else:
                    self.gui.after(1250, lambda: self.gui.gameplay_frame.show_not_enough_money(self.gui.game_canvas))
                self.gui.wait_variable(self.click_var)  # waits for the click_var to update before allowing execution
                if self.click_var.get() == "buy":
                    if can_buy:
                        action = "buy"
                        print(player_this_turn.get_name()," is now buying") #TODO del later
                    else:
                        print("Not enough money") #del
                        action = "not_buy"
                elif self.click_var.get() == "not_buy":
                    action = "not_buy"
                self.gui.gameplay_frame.delete_not_enough_money(self.gui.game_canvas)
            else:
                action = "rent"
            tile.player_landed(player_this_turn, action, Property.get_owner_obj(self.player_list, tile.get_owner()))
            self.unbind_yes_buy_button() #unbind and hide the yes_buy_button
            self.unbind_no_buy_button() #unbind and the hide the no_buy_button
        elif tile_type == "jail":
            # TODO update view just visiting
            pass
        elif tile_type == "go":
            # TODO update view
            pass
        elif tile_type == "go_to_jail":
            tile.player_landed(player_this_turn, self.board.get_jail_tile())
            # TODO jail animation
        elif tile_type == "income_tax":
            tile.player_landed(player_this_turn)
            # TODO tax animation
            pass
        elif tile_type == "free_parking":
            # TODO parking animation
            pass
        else:
            tile.player_landed(player_this_turn)
        self.update_all_game_info()

    """This function is called after pressing the 'Roll' button in the game window."""

    # def roll_dice(self,player_this_turn):
    #     self.unbind_roll_button() #unbind the roll button
    #     dice_roll1, dice_roll2 = GameLogic.roll_dice()
    #     tile = GameLogic.player_move(dice_roll1 + dice_roll2, player_this_turn, self.board)
    #     #player_this_turn = self.get_player_list()[self.game_logic.get_player_turn()]
    #     print("Money: ",player_this_turn.get_current_money())
    #     print("Square:",player_this_turn.get_current_position())
    #     print(tile.get_tile_name())
    #     self.update_all_game_info()
    #     self.land_and_complete_round(tile, player_this_turn)
    #     self.determine_next_round(player_this_turn)

    def roll_dice(self, player_this_turn):
        self.unbind_roll_button()  # Unbind the roll button
        self.unbind_save_quit_button()
        dice_roll1, dice_roll2 = GameLogic.roll_dice()
        dice_select_image_position1 = (2*dice_roll1-1) - random.randint(0,1) #for choosing image of dice1
        dice_select_image_position2 = (2*dice_roll2-1) - random.randint(0,1) #for choosing image of dice2
        print(player_this_turn.get_name(), "is Rolling, and rolled: ", dice_roll1 ,dice_roll2, dice_select_image_position1, dice_select_image_position2)

        # Save the dice results
        self.dice_results = []

        # Handle the result of each dice roll animation
        def on_dice_roll(dice_result):
            self.dice_results.append(dice_result)

            # Display each roll result
            roll_number = len(self.dice_results)

            if len(self.dice_results) < 2:
                #Wait for 1 second before starting the second roll
                self.gui.after(1000, lambda: self.gui.gameplay_frame.roll_dice_animation(
                            self.gui.game_canvas, self.gui.image_width * 2 / 7, self.gui.image_height * 2 / 5 + 120,
                                          roll_number + 1, on_dice_roll, dice_select_image_position2)
                            )

            else:
                # Both dice rolls are complete
                total_dice = sum(self.dice_results)
                # Pass total_dice to roll_dice_animation to display final result and hide dice
                self.gui.gameplay_frame.roll_dice_animation(
                    self.gui.game_canvas, self.gui.image_width * 2 / 7, self.gui.image_height * 2 / 5 + 120,
                    3, on_dice_roll,None, total_dice
                )

                startingPosition = player_this_turn.get_current_position()
                # Continue game logic with the total dice result after displaying it, updates position
                tile = GameLogic.player_move(total_dice, player_this_turn, self.board)
                # Shows player movement
                self.gui.gameplay_frame.player_movement(self.gui.game_canvas, self.player_list.index(player_this_turn),
                                                        startingPosition, tile.get_tile_position())
                self.update_all_game_info()

                #for smoother game experience, pause shorter when for the player who is buying property
                if tile.get_tile_type() == "property" and tile.get_owner() is None:
                    self.gui.after(750, lambda: self.for_delay_round(player_this_turn,tile))
                else:
                    #show the button for next round after 500 ms
                    self.gui.after(1500, lambda: self.for_delay_round(player_this_turn,tile))

        # Start the dice animation for the first roll
        self.gui.gameplay_frame.roll_dice_animation(
            self.gui.game_canvas, self.gui.image_width * 2 / 7, self.gui.image_height * 2 / 5 + 120, 1, on_dice_roll,
            dice_select_image_position1
        )

    def for_delay_round(self,player_this_turn,tile):
        self.land_and_complete_round(tile, player_this_turn)
        self.determine_next_round(player_this_turn)
        self.update_all_game_info()


    # Roll function for player in jail
    def in_jail_roll(self, player_this_turn):
        #unbind the in_jail_roll button and pay_fine button
        self.unbind_roll_button()
        self.unbind_pay_fine_button(player_this_turn)
        self.unbind_save_quit_button()

        print(player_this_turn.get_name(), "is Rolling IN JAIL.") # TODO del this line later
        print("Money: ", player_this_turn.get_current_money())  # TODO del this line later
        print("Square:", player_this_turn.get_current_position())  # TODO del this line later

        #x and y position for the dice image
        x_position = self.gui.image_width * 2 / 7
        y_position = self.gui.image_height * 2 / 5 + 120

        action = GameLogic.in_jail_roll(self.game_logic, player_this_turn, self.board)

        dice_select_image_position1 = (2 * action[2] - 1) - random.randint(0, 1)  # for choosing image of dice1
        dice_select_image_position2 = (2 * action[3] - 1) - random.randint(0, 1)  # for choosing image of dice2
        dice_results = [dice_select_image_position1, dice_select_image_position2]

        self.gui.gameplay_frame.jail_roll_animation(
            self.gui.game_canvas,x_position, y_position,dice_results,
            )

        self.gui.after(3250, lambda: self.update_all_game_info())

        self.gui.after(3250, lambda: on_jail_dice_roll())

        def on_jail_dice_roll():
            message = f"Out of Jail.\nPlayer move {action[2] + action[3]}"
            if action[0] == "show_pay_fine":
                self.bind_pay_fine_button(player_this_turn) #bind and show the pay_fine button
                self.gui.wait_variable(self.click_var)  # wait for pay fine button to be clicked
                #TODO display fine paid
                if action[1] is not None:
                    print("Fine paid. Move on")
                    self.gui.gameplay_frame.message_for_jail_roll(self.gui.game_canvas, message, y_position,
                                                                  sum(action[2:4]))
                    self.land_and_complete_round(action[1], player_this_turn)
                    # TODO <show moving animation>
                else:
                    message = None #player broke by paying fine
                    self.gui.gameplay_frame.message_for_jail_roll(self.gui.game_canvas, message, y_position,
                                                                  sum(action[2:4]))
            elif action[0] == "move":
                # TODO <show animation for player moving>
                print("Out of Jail, Move on")
                self.gui.gameplay_frame.player_movement(self.gui.game_canvas, self.player_list.index(player_this_turn), 5, action[1].get_tile_position())
                self.gui.gameplay_frame.message_for_jail_roll(self.gui.game_canvas, message, y_position,
                                                              sum(action[2:4]))
                self.land_and_complete_round(action[1], player_this_turn)
            elif action[0] == 'not_move':
                message = "Stay in Jail"
                self.gui.gameplay_frame.message_for_jail_roll(self.gui.game_canvas, message, y_position,
                                                              sum(action[2:4]))


            self.update_all_game_info()
            self.gui.after(50,lambda:self.determine_next_round(player_this_turn))


    def pay_fine(self, player_this_turn):
        # pay_fine_logic
        GameLogic.pay_fine(self.game_logic, player_this_turn)
        self.update_all_game_info()
        self.click_var.set("pay_fine")
        print("Paying fine")
        self.unbind_pay_fine_button(player_this_turn)
        # TODO <Show the money is deduced>

    def buy_button(self):
        self.click_var.set("buy")
        print("Buying")

    def no_buy_button(self):
        self.click_var.set("no_buy")
        print("Not Buying")
        # TODO <Show did not buy property>

    def end_game(self):
        # Need to modify the logic in GameLogic endgame
        pass

    def save_gameboard(self, save_name):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves/gameboard_setups"))
        message1 = ""

        # ensures directory existence or creates
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            message1 = "Save directory deleted or non existent --> Creating"

        gameboard_setup = SavedGameboard(save_name, self)
        gameboard_data = gameboard_setup.to_dictionary()
        file_path = os.path.join(save_directory, f'{save_name}.json')
        with open(file_path, 'w') as save_file:
            json.dump(gameboard_data, save_file, indent=4)
            message = "Game saved successfully.\n"
        return f"{message1}\n{message}"

    def show_save_game(self): #TODO del the initializer line later
        user_input = self.gui.enter_file_name_frame.name_entry.get().strip() #get the entry in the text box
        if self.input_handler.valid_current_game_name(user_input): #if the name is valid
            self.save_game(user_input) #save it to the folder
            self.gui.enter_file_name_frame.clear_all_info()
            self.gui.save_game_frame.save_data(self.gui.save_game_canvas) #go back to save game frame and show the name
        else:
            self.gui.enter_file_name_frame.wrong_save_name(self.gui.enter_name_canvas)

    # noinspection PyTypeChecker
    def save_game(self, save_name):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves/games"))
        message1 = ""

        # ensures directory existence or creates
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            message1 = "Save directory deleted or non existent --> Creating"

        save_instance = SavedGame(save_name, self)
        game_data = save_instance.to_dictionary()
        file_path = os.path.join(save_directory, f'{save_name}.json')
        with open(file_path, 'w') as save_file:
            json.dump(game_data, save_file, indent=4)
            message = "Game saved successfully.\n"
        return f"{message1}\n{message}"

    # loads gameboard_data into gameboard object, if data is passed, handles it, otherwise acts on the board_name and looks for it
    def load_gameboard(self, board_name = "", game_data_dict = None):
        if game_data_dict is None:
            # determines the filepath of the saved gameboard
            save_directory = os.path.dirname(os.path.abspath(__file__))
            save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves/gameboard_setups"))
            file_path = os.path.join(save_directory, f'{board_name}.json')

            # parse save file into a dictionary and handles exceptions
            try:
                with open(file_path, 'r') as game_data:
                    game_data_dict = json.load(game_data)
            except FileNotFoundError:
                print("Board layout does not exist.")
                return
            except json.JSONDecodeError:
                print("Error in reading save file.")
                return

        # gameboard_setup is a list of dictionaries, will cycle and update appropriately
        gameboard_info = game_data_dict["gameboard_setup"]
        for tile_info, i in zip(gameboard_info, range(20)):
            self.board.tiles[i].update_name_pos_type(tile_info["name"], tile_info["board_pos"], tile_info["tile_type"])
            tile_type = tile_info["tile_type"]
            if tile_type == "property":
                self.board.tiles[i].update_values(tile_info["price"], tile_info["rent"], tile_info["owner"], tile_info["color"])
            elif tile_type == "income_tax":
                self.board.tiles[i].update_values(tile_info["tax_percentage"])
            elif tile_type == "jail":
                self.board.tiles[i].update_values(tile_info["jailed_players"])
            elif tile_type == "go":
                self.board.tiles[i].update_values(tile_info["pass_prize"])

    def load_game(self, load_name):
        # gets current directory in which the program is running
        save_directory = os.path.dirname(os.path.abspath(__file__))

        # moves up and into the saves directory and normalizes the path
        save_directory = os.path.normpath(os.path.join(save_directory, "..", "..", "saves/games"))

        file_path = os.path.join(save_directory, f'{load_name}.json')

        # parse save file into a dictionary and handles exceptions
        try:
            with open(file_path, 'r') as game_data:
                game_data_dict = json.load(game_data)
        except FileNotFoundError:
            print("Game saved does not exist.")
            return
        except json.JSONDecodeError:
            print("Error in reading save file.")
            return

        # pulls information from the dictionary into respective variables
        self.set_save_name(game_data_dict["save_name"])
        self.set_current_round(game_data_dict["current_round"])
        self.set__turn(game_data_dict["_turn"])
        self.set_remove_last_round(game_data_dict["remove_last_round"])

        self.load_gameboard("", game_data_dict["gameboard_data"])

        # creates players objects and copies information from the dictionary
        players = game_data_dict["players_list"]
        for p_data in players:
            new_player = Player("")
            new_player.update_values(p_data["_username"], p_data["_current_money"], p_data["_jail_status"], p_data["_fine_payed"], p_data["_current_square"], p_data["_in_jail_turns"], p_data["_properties"])
            self.player_list.append(new_player)

        broke_players = game_data_dict["broke_list"]
        for p_data in broke_players:
            new_player = Player("")
            new_player.update_values(p_data["_username"], p_data["_current_money"], p_data["_jail_status"], p_data["_fine_payed"], p_data["_current_square"], p_data["_in_jail_turns"], p_data["_properties"])
            self.broke_list.append(new_player)

class SavedGameboard:
    def __init__(self, save_name, game_controller):
        self.board_name = save_name
        self.tiles = game_controller.board.tiles.copy()

    def to_dictionary(self):
        gameboard_data = [tile.__dict__ for tile in self.tiles]
        return {
            "board_name": self.board_name,
            "gameboard_setup": gameboard_data
        }

# this class will copy the current game instance
class SavedGame:
    def __init__(self, save_name, game_controller):
        # Gets the name of the save and current round
        self.save_name = save_name
        self.save_time = datetime.now().strftime("%H:%M %d-%m-%Y")
        self._turn = game_controller.get__turn()
        self.remove_last_round = game_controller.game_logic.get_remove_last_round()
        self.current_round = game_controller.get_current_round()

        # Saves the setup of the gameboard as a list
        self.gameboard = SavedGameboard("", game_controller)

        # Saves players information
        self.player_list = game_controller.get_player_list().copy()
        self.broke_list = game_controller.get_broke_player_list().copy()

    def to_dictionary(self):
        # unpacks list of objects to a list of dictionary entries
        gameboard_data = self.gameboard.to_dictionary()
        player_data = [player.__dict__ for player in self.player_list]
        broke_player_data = [player.__dict__ for player in self.broke_list]

        return {
            "save_name": self.save_name,
            "save_time": self.save_time,
            "_turn": self._turn,
            "remove_last_round": self.remove_last_round,
            "current_round": self.current_round,
            "gameboard_data": gameboard_data,
            "players_list": player_data,
            "broke_list": broke_player_data
        }

    def get_save_name(self):
        return self.save_name