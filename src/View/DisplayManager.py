import tkinter as tk
import os
import time
from random import choice
from typing import final

from tests.test_GameLogic import players_list

# Base path for assets
assets_base_path = os.path.join(os.path.dirname(__file__), "../../assets")

class DisplayManager:
    def __init__(self, gui):
        self.gui = gui  # Reference to the main GUI instance
        self.error_labels = [None] * 6  # Hold error messages for player names
        self.player_entries = []  # Hold player name entry widgets
        self.player_box_images_refs = []  # Hold player box image references
        self.player_text_refs = [None] * 6  # Store references to the text displayed in each player box
        self.clicked_boxes = [False] * 6  # Add a flag list to track clicked boxes

        self.active_widgets = []  # Store references to active widgets
        self.hidden_widgets = {}  # Dictionary to store widgets and their positions for hiding/showing

        self.back_arrow_image = tk.PhotoImage(file=os.path.join(assets_base_path, "info_frame/back_arrow.png"))

    def clear_widgets_create_canvas_set_background(self, frame, background):
        # Clear any existing widgets in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Create the canvas and set the background image
        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.gui.image_height, width=self.gui.image_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=background)
        return canvas

    @staticmethod
    def calc_button_dim(button_image):
        return button_image.width(), button_image.height()


# noinspection DuplicatedCode
class GameplayFrame(DisplayManager):

    # Gameboard tiles 9-tuple will get loaded in by the Controller
    #  [type, name, price, rent, owner, nameObj, priceObj, rentObj, ownerObj]
    tile_info = []

    def __init__(self, gui):
        super().__init__(gui)

        # New Gameplay frame images
        self.new_gameplay_frame_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "gameplay_frame/gameplay_frame_background.png"))
        self.roll_dice_image = tk.PhotoImage(file = os.path.join(assets_base_path, "gameplay_frame/roll_dice.png"))
        self.save_quit_image = tk.PhotoImage(file = os.path.join(assets_base_path, "gameplay_frame/save_quit.png"))
        self.pay_fine_image = tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/pay_fine.png"))
        self.yes_image = tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/yes.png"))
        self.no_image = tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/no.png"))
        self.player_info_ID = []

        # Dice animation frames
        self.dice_animation_frames = [
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/animation/dice_animation_frame_1.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/animation/dice_animation_frame_2.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/animation/dice_animation_frame_3.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/animation/dice_animation_frame_4.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/animation/dice_animation_frame_5.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/animation/dice_animation_frame_6.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/animation/dice_animation_frame_7.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/animation/dice_animation_frame_8.png"))
        ]

        # Dice result images
        self.dice_result_images = [
            (tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/results/dice_side_view_result_1.png")), 1),
            (tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/results/dice_top_down_result_1.png")), 1),
            (tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/results/dice_side_view_result_2.png")), 2),
            (tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/results/dice_top_down_result_2.png")), 2),
            (tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/results/dice_side_view_result_3.png")), 3),
            (tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/results/dice_top_down_result_3.png")), 3),
            (tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/results/dice_side_view_result_4.png")), 4),
            (tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/dice/results/dice_top_down_result_4.png")), 4)
        ]

        # Gameboard tiles colors empty list, will get loaded in by the Controller
        self.tile_colors = []

        # Tile color coordinates from anchor (reference point) "NW" corner
        self.__tile_color_coord = [
            None,
            [565, 818],
            [430, 818],
            None,
            [160, 818],
            None,   # jail
            [118, 683],
            [118, 548],
            None,
            [118, 278],
            None, # free parking
            [565, 236],
            None,
            [430, 236],
            [160, 236],
            None, # go to jail
            [700, 278],
            [700, 413],
            None,
            [700, 683]
        ]

        # Tile info coordinates, 6-tuple
        self.__tile_info_coord = [
            [None, None, 770, 860, None, None, None, None], # go
            [635, 880, 635, 905, 635, 930, 635, 840], # prop1
            [500, 880, 500, 905, 500, 930, 500, 840], # prop2
            [365, 870, 365, 930, None, None, None, None],   # income tax
            [230, 880, 230, 905, 230, 930, 230, 840], # prop3
            [None, None, None, None, None, None, None, None], # jail
            [100, 752, 75, 752, 50, 752, 142, 752], # prop4
            [100, 617, 75, 617, 50, 617, 142, 617], # prop5
            [95, 510, None, None, None, None, None, None], # chance
            [100, 347, 75, 347, 50, 347, 142, 347], # prop6
            [95 , 210, None, None, None, None, None, None], # free parking
            [230, 165, 230, 190, 230, 215, 230, 258],  # prop7
            [365, 240, 365, 190, None, None, None, None],  # chance
            [500, 165, 500, 190, 500, 215, 500, 258],  # prop8
            [635, 165, 635, 190, 635, 215, 635, 258],  # prop9
            [None, None, None, None, None, None, None, None],  # go to jail
            [765, 347, 790, 347, 815, 347, 722, 347],  # prop10
            [765, 482, 790, 482, 815, 482, 722, 482],  # prop11
            [770, 645, None, None, None, None, None, None],  # chance
            [765, 752, 790, 752, 815, 752, 722, 752]  # prop12
        ]

        # players information
        self.player_info = []
        self.totalMovement = 135
        self.no_money_ID = None
        self.player_image_ID = []
        self.player_image = [
            tk.PhotoImage(file= os.path.join(assets_base_path, "gameplay_frame/player1.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/player2.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/player3.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/player4.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/player5.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "gameplay_frame/player6.png"))
            ]
        self.placeholder_coords = [
            [730, 865],
            [810, 915],
            [810, 865],
            [730, 915],
            [770, 865],
            [770, 915]
        ]

        # Buttons Coordinates
        self.half_screen_y = self.gui.image_height / 2
        self.roll_dice_x_pos = self.gui.image_width * 2 / 7
        self.roll_dice_y_pos = self.gui.image_height * 2 / 5 - 50
        self.save_quit_x_pos = self.gui.image_width * 11 / 14
        self.save_quit_y_pos = self.gui.image_height * 9 / 10
        self.pay_fine_x_pos = self.gui.image_width * 2 / 7
        self.pay_fine_y_pos = self.gui.image_height * 5 / 10 - 45
        self.yes_x_pos = self.gui.image_width * 5 / 14
        self.yes_y_pos = self.gui.image_height * 4 / 5 - 20
        self.no_x_pos = self.gui.image_width * 3 / 14
        self.no_y_pos = self.gui.image_height * 4 / 5 - 20

        # Player INFO Coordinates
        self.starting_y_pos = 200
        self.bottom_y_border = 860
        self.right_x_border = 950
        self.left_x_border = 1430
        self.player_positional_increment = 0
        self.global_increment = 0
        self.player_turn = 0
        self.player_highlighter_ID = []

# ------------------------------------# Game Play Frame #------------------------------------#
    @staticmethod
    def set_appropriate_text_dimension(name, price, rent, owner):
        name_size = 16
        price_size = 16
        rent_size = 16
        owner_size = 16

        if len(name) > 12:
            name_size -= 4
        elif len(name) > 10:
            name_size -= 2

        if len(price) > 12:
            price_size -= 4
        elif len(price) > 10:
            price_size -= 2

        if len(rent) > 12:
            rent_size -= 4
        elif len(rent) > 10:
            rent_size -= 2

        if owner:
            if len(owner) > 11:
                owner_size -= 4
            elif len(owner) >= 9:
                owner_size -= 2

        return name_size, price_size, rent_size, owner_size

    @staticmethod
    def rotate_text(i):
        text_rotate = 0
        # text rotation information
        if 5 < i < 10:  # left board side
            text_rotate = 270.0
        elif 15 < i < 20:  # right board side
            text_rotate = 90.0
        return text_rotate

    def set_color(self, pos, color):
        self.tile_colors[pos][0] = color

    def get_color_coord(self, pos):
        return self.__tile_color_coord[pos]

    def roll_dice_animation(self, canvas, roll_dice_x_pos, roll_dice_y_pos, dice_counter, callback, total_dice=None):
        # Show each frame of the dice animation
        def show_frame(frame_index):
            if frame_index < len(self.dice_animation_frames):
                canvas.delete("dice_animation")
                canvas.create_image(
                    roll_dice_x_pos, roll_dice_y_pos,
                    image=self.dice_animation_frames[frame_index],
                    anchor="center", tags="dice_animation"
                )
                self.gui.after(50, show_frame, frame_index + 1)  # Show next frame after 50 ms
            else:
                if dice_counter <= 2:
                    # After the animation, display a random dice result
                    result_image, dice_result = choice(self.dice_result_images)
                    canvas.delete("dice_animation")
                    canvas.create_image(
                        roll_dice_x_pos, roll_dice_y_pos,
                        image=result_image, anchor="center", tags="dice_animation"
                    )

                    # Display the dice result on the canvas as text
                    x_offset = - 135 if dice_counter == 1 else 135
                    canvas.create_text(
                        0.28440 * self.gui.image_width + x_offset, 0.65274 * self.gui.image_height,
                        text=f"Dice {dice_counter} Result: {dice_result}",
                        font=("Comic Sans MS", 22, "bold"),
                        fill="#000000",
                        tags=f"dice_result_text_{dice_counter}"
                    )

                    # Pass the dice result to the callback function
                    callback(dice_result)
                else:
                    # After a 0.5s delay, display again
                    self.gui.after(500,
                                   lambda: clear_dice_display(canvas, roll_dice_x_pos, roll_dice_y_pos, total_dice))

        def clear_dice_display(canvas, roll_dice_x_pos, roll_dice_y_pos, total_dice):
            # Hide the dice image and individual roll texts
            canvas.delete("dice_animation", "dice_result_text_1", "dice_result_text_2")

            # Display the total dice result on the canvas
            canvas.create_text(
                0.28458 * self.gui.image_width, roll_dice_y_pos + 30,
                text=f"Total Dice is {total_dice}, Move {total_dice} forward.",
                font=("Comic Sans MS", 22, "bold"),
                fill="#000000",
                tags="total_dice_result_text",
            )

        # Clear any previous result text before starting a new roll
        if dice_counter == 1:
            canvas.delete("total_dice_result_text")

        # Start the animation with the first frame
        show_frame(0)

    #for testing
    def save_quit(self):
        self.gui.show_frame("save_game")

    def create_button(self, canvas, x_pos, y_pos, button_image):
        button_width, button_height = self.calc_button_dim(button_image)
        image_id = canvas.create_image(x_pos, y_pos, anchor="center", image=button_image)
        button_click_area = canvas.create_rectangle(
            (x_pos - button_width // 2), (y_pos - button_height // 2),
            (x_pos + button_width // 2), (y_pos + button_height // 2),
            outline="", fill=""
        )
        return button_click_area, canvas, image_id

    def show_pay_fine_button(self, canvas):
        pay_fine_click_area, canvas, pay_fine_image_id = self.create_button(canvas, self.pay_fine_x_pos, self.pay_fine_y_pos, self.pay_fine_image)
        return pay_fine_click_area, canvas, pay_fine_image_id

    def show_yes_button(self, canvas):
        yes_click_area, canvas, yes_button_image_id = self.create_button(canvas, self.yes_x_pos, self.yes_y_pos, self.yes_image)
        return yes_click_area,canvas,yes_button_image_id

    def show_no_button(self, canvas):
        no_click_area, canvas, no_button_image_id = self.create_button(canvas, self.no_x_pos, self.no_y_pos, self.no_image)
        # TODO BIND FUNCTION canvas.tag_bind(no_click_area, "<Button-1>", lambda e: )
        return no_click_area,canvas, no_button_image_id

    def destroy_old_info(self, canvas):
        # destroys old GameplayFrame.tile_info widgets
        for i in [1, 2, 4, 6, 7, 9, 11, 13, 14, 16, 17, 19]:
            for j in range(5, 9):
                canvas.delete(GameplayFrame.tile_info[i][j])

        # destroys player_info widgets
        for i in range(0, len(self.player_info_ID)):
            canvas.delete(self.player_info_ID[i])

    def update_display_info(self, canvas):
        self.destroy_old_info(canvas)
        self.display_player_info(canvas)
        self.display_tile_info(canvas)

    def create_player_highlighter(self, canvas):
        y_pos = self.starting_y_pos
        for i in range(0, len(self.player_info)):
            image_id = canvas.create_image(self.right_x_border - 40, y_pos, anchor="center",
                                            image=self.player_image[i])
            y_pos += self.player_positional_increment
            self.player_highlighter_ID.append(image_id)
        return canvas

    def display_appropriate_player_highlighter_on_initialization(self, canvas):
        if self.player_turn == -1:
            self.player_turn += 1
        for i in range(0, len(self.player_info)):
            if i != self.player_turn:   # if it's the player's current turn then it doesn't move
                canvas.move(self.player_highlighter_ID[i], 1000, 0) # moves out of screen
        return canvas

    def hide_all_player_highlighter(self, canvas):
        for i in range(0, len(self.player_info)):
            coords = canvas.coords(self.player_highlighter_ID[i])
            if coords[0] == (self.right_x_border - 40):
                canvas.move(self.player_highlighter_ID[i], 1000, 0)
        return canvas

    # hides previous player and moves into view the current one
    def highlight_current_player(self, canvas, curr_player_idx):
        canvas = self.hide_all_player_highlighter(canvas)
        canvas.move(self.player_highlighter_ID[curr_player_idx], -1000, 0)

    def display_winners_on_canvas(self, canvas, winners_list):
        winner_message = winners_list[0]
        list_size = len(winners_list)
        if list_size > 1:
            for i in range(1, list_size):
                winner_message = f"{winner_message}\n{winners_list[i]}"
        winner_message = f"{winner_message}\n WON THE GAME"
        canvas.create_text(self.roll_dice_x_pos, self.half_screen_y + 50 , anchor="center", text=winner_message,
                           font= ("Comic Sans MS", 20, "bold"), fill="#000000", justify="center")

    def show_not_enough_money(self, canvas):
        self.no_money_ID = canvas.create_text(self.yes_x_pos, self.yes_y_pos, anchor="center", text="NOT ENOUGH\nMONEY",
                           font= ("Comic Sans MS", 20, "bold"), fill="#000000", justify="center")

    def delete_not_enough_money(self, canvas):
        canvas.delete(self.no_money_ID)

    def create_player_placeholders(self, canvas):
        for i in range(0, len(self.player_info)):
            placeholder_id = canvas.create_image(self.placeholder_coords[i][0], self.placeholder_coords[i][1], image= self.player_image[i])
            self.player_image_ID.append(placeholder_id)
        return canvas

    # moves the player horizontally, returns new position
    def player_move_horizontal(self, canvas, placeholder_id, direction):
        if direction == "left":
            canvas.move(placeholder_id, -self.totalMovement, 0)
        else:
            canvas.move(placeholder_id, self.totalMovement, 0)
        return canvas.coords(placeholder_id)

    # moves the player vertically, returns new position
    def player_move_vertical(self, canvas, placeholder_id, direction):
        if direction == "up":
            canvas.move(placeholder_id, 0, -self.totalMovement)
        else:
            canvas.move(placeholder_id, 0, self.totalMovement)

    # noinspection PyUnusedLocal
    def player_movement(self, canvas, player, starting_pos, final_pos):
        placeholder_id = self.player_image_ID[player]
        if final_pos < starting_pos:
            final_pos += 20
        curr_pos = starting_pos
        while curr_pos < final_pos:
            if 0 <= curr_pos < 5:
                self.player_move_horizontal(canvas, placeholder_id, "left")
            elif 5 <= curr_pos < 10:
                self.player_move_vertical(canvas, placeholder_id, "up")
            elif 10 <= curr_pos < 15:
                self.player_move_horizontal(canvas, placeholder_id, "right")
            elif 15 <= curr_pos < 19:
                self.player_move_vertical(canvas, placeholder_id, "down")
            else:
                index = self.player_image_ID.index(placeholder_id)
                canvas.coords(placeholder_id, self.placeholder_coords[index][0], self.placeholder_coords[index][1])
                curr_pos = 0
                final_pos -= 19
            curr_pos += 1

        if final_pos == 15: #go to jail tile, moves player to jail
            canvas.move(placeholder_id, -675, 675)
        #placeholder_id.lift()

    def display_player_info(self, canvas):
        starting_pos = self.starting_y_pos
        total_players = len(self.player_info)
        increment = (self.bottom_y_border - starting_pos) / total_players
        self.player_positional_increment = increment
        self.global_increment = increment
        name_size = 22
        info_size = 20
        for i in range(0, total_players):
            player_name = self.player_info[i][0]
            player_balance = self.player_info[i][1]
            player_balance_text = f"Balance: {player_balance} HKD"
            player_position = self.player_info[i][2]
            player_position_text = f" is in {player_position}"
            player_jail_status = self.player_info[i][3]
            player_jail_turns = self.player_info[i][4]
            player_total_properties = f"Properties: {self.player_info[i][5]}"

            # filters appropriate message based on balance and jail status
            if player_balance >= 0:
                if player_position == "Jail":
                    if not player_jail_status:
                        player_position_text = f"{player_position_text}, just visiting"
                    else:
                        player_position_text = f"{player_position_text}, {player_jail_turns} remaining"
            else:
                player_position_text = "HAS LOST"

            name_id = canvas.create_text(self.right_x_border, starting_pos, text= player_name, anchor="w",
                                         font=("Comic Sans MS", name_size, "bold"), fill="#000000")

            # calculates dimensions of name box
            name_box = canvas.bbox(name_id)
            name_width = name_box[2] - name_box[0] + 5

            pos_id = canvas.create_text(self.right_x_border + name_width, starting_pos, text= player_position_text, anchor="w",
                                        font=("Comic Sans MS", info_size), fill="#000000")
            balance_id = canvas.create_text(self.right_x_border, starting_pos + 40, text= player_balance_text, anchor="w",
                                            font=("Comic Sans MS", info_size), fill="#000000")
            tot_prop_id = canvas.create_text(self.left_x_border, starting_pos + 40, text= player_total_properties, anchor="e",
                                             font=("Comic Sans MS", info_size), fill="#000000")
            starting_pos += increment
            self.player_info_ID.append(name_id)
            self.player_info_ID.append(pos_id)
            self.player_info_ID.append(balance_id)
            self.player_info_ID.append(tot_prop_id)

    #----------Handles hiding the button IMAGE in the canvas----------#
    def hide_yes_image(self,canvas):
        canvas.coords(self.yes_image_id,-100,-100)

    def hide_no_image(self,canvas):
        canvas.coords(self.no_image_id,-100,-100)

    def hide_roll_image(self,canvas):
        canvas.coords(self.roll_dice_image_id,-100,-100)

    def hide_pay_fine_image(self,canvas):
        canvas.coords(self.pay_fine_image_id,-100,-100)

    def hide_save_quit_image(self,canvas):
        canvas.coords(self.save_quit_image_id,-100,-100)

    #------------------------------------------------------------------#


    #----------Handles showing the button image in the canvas----------#
    def show_yes_image(self,canvas):
        canvas.coords(self.yes_image_id,self.yes_x_pos, self.yes_y_pos)

    def show_no_image(self,canvas):
        canvas.coords(self.no_image_id,self.no_x_pos, self.no_y_pos)

    def show_roll_image(self,canvas):
        canvas.coords(self.roll_dice_image_id, self.roll_dice_x_pos, self.roll_dice_y_pos)

    def show_pay_fine_image(self,canvas):
        canvas.coords(self.pay_fine_image_id, self.pay_fine_x_pos, self.pay_fine_y_pos)

    def show_save_quit_image(self,canvas):
        canvas.coords(self.save_quit_image_id,self.save_quit_x_pos, self.save_quit_y_pos)

    # ------------------------------------------------------------------#

    # from the gameboard information loads the appropriate colors in the game frame
    def load_tile_colors(self):
        for i in range(0,20):
            color = self.tile_colors[i][0]
            if color:
                self.modify_tile_color(color, i)

    # gets the information from the lists above and display all the tiles colors
    def display_tile_colors(self, canvas):
        self.load_tile_colors()
        for i in range(0, 20):
            color_coord = self.__tile_color_coord[i]
            if color_coord: # if None (meaning at that position there is a tile that has no color) doesn't execute
                x_pos = color_coord[0]
                y_pos = color_coord[1]
                tile_color = self.tile_colors[i][1]
                canvas.create_image(x_pos, y_pos, anchor="nw", image=tile_color)

    # from the info in the gameboard, displays it on the gameboard
    def display_tile_info(self, canvas):
        for i in range(0, 20):
            # gets all information necessary to display
            tile_type = GameplayFrame.tile_info[i][0]
            tile_name = GameplayFrame.tile_info[i][1]
            tile_price = str(GameplayFrame.tile_info[i][2])
            tile_rent = f"{GameplayFrame.tile_info[i][3]} HDK"
            tile_owner = GameplayFrame.tile_info[i][4]
            name_x_pos = self.__tile_info_coord[i][0]
            name_y_pos = self.__tile_info_coord[i][1]
            price_x_pos = self.__tile_info_coord[i][2]
            price_y_pos = self.__tile_info_coord[i][3]
            rent_x_pos = self.__tile_info_coord[i][4]
            rent_y_pos = self.__tile_info_coord[i][5]
            owner_x_pos = self.__tile_info_coord[i][6]
            owner_y_pos = self.__tile_info_coord[i][7]

            # calculates text sizes
            text_name_size, text_price_size, text_rent_size, text_owner_size = self.set_appropriate_text_dimension(
                tile_name, tile_rent, tile_price, tile_owner)

            # calculates text rotation
            text_rotate = self.rotate_text(i)

            # displays text based on tile type
            if tile_type == "property":
                GameplayFrame.tile_info[i][5] = canvas.create_text(name_x_pos, name_y_pos, text=tile_name,
                                                          font=("Comic Sans MS", text_name_size, "bold"),
                                                          fill="#000000", angle=text_rotate)
                tile_price = f"{tile_price} HKD"
                GameplayFrame.tile_info[i][6] = canvas.create_text(price_x_pos, price_y_pos, text=tile_price,
                                                          font=("Comic Sans MS", text_price_size), fill="#000000",
                                                          angle=text_rotate)
                GameplayFrame.tile_info[i][7] = canvas.create_text(rent_x_pos, rent_y_pos, text=tile_rent,
                                                          font=("Comic Sans MS", text_rent_size), fill="#000000",
                                                          angle=text_rotate)
                GameplayFrame.tile_info[i][8] = canvas.create_text(owner_x_pos, owner_y_pos, text=tile_owner,
                                                          font=("Comic Sans MS", text_owner_size), fill="#000000",
                                                          angle=text_rotate)

            elif tile_type == "go":
                tile_price = f"Collect\n{tile_price} HKD"
                GameplayFrame.tile_info[i][6] = canvas.create_text(price_x_pos, price_y_pos, text=tile_price,
                                                          font=("Comic Sans MS", 18, "bold"), fill="#000000",
                                                          justify="center")

            elif tile_type == "free_parking":
                tile_name = tile_name.replace(" ", "\n")
                GameplayFrame.tile_info[i][6] = canvas.create_text(name_x_pos, name_y_pos, text=tile_name,
                                                          font=("Comic Sans MS", 20, "bold"), fill="#000000",
                                                          justify="center")

            elif tile_type == "chance":
                GameplayFrame.tile_info[i][6] = canvas.create_text(name_x_pos, name_y_pos, text=tile_name,
                                                          font=("Comic Sans MS", 20, "bold"), fill="#000000")

            elif tile_type == "income_tax":
                tile_name = tile_name.replace(" ", "\n")
                GameplayFrame.tile_info[i][6] = canvas.create_text(name_x_pos, name_y_pos, text=tile_name,
                                                          font=("Comic Sans MS", 20, "bold"), fill="#000000",
                                                          justify="center")
                tile_price = f"{tile_price} %"
                GameplayFrame.tile_info[i][7] = canvas.create_text(price_x_pos, price_y_pos, text=tile_price,
                                                          font=("Comic Sans MS", 16), fill="#000000")

    # called to set up the entire gameplay_frame
    def setup_new_gameplay_frame(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.new_gameplay_frame_background)

        # TILE COLORS
        self.display_tile_colors(canvas)

        # TILE INFORMATION
        self.display_tile_info(canvas)

        # PLAYER INFORMATION
        self.display_player_info(canvas)

        # PLAYER HIGHLIGHTER
        canvas = self.create_player_highlighter(canvas)
        canvas = self.display_appropriate_player_highlighter_on_initialization(canvas)

        # PLAYER POSITION ON BOARD and MOVES TO CORRECT TILE IN CASE OF LOADING GAME
        canvas = self.create_player_placeholders(canvas)
        player_index = 0
        for player in self.player_info:
            self.player_movement(canvas, player_index, 0, player[6]) #player[6] players_info position information
            player_index += 1

        # ROLL DICE BUTTON
        roll_dice_click_area, canvas, self.roll_dice_image_id = self.create_button(canvas, self.roll_dice_x_pos, self.roll_dice_y_pos, self.roll_dice_image)
        #canvas.tag_bind(roll_dice_click_area, "<Button-1>", lambda e: self.roll_dice())

        # SAVE QUIT BUTTON
        save_quit_click_area, canvas, self.save_quit_image_id = self.create_button(canvas, self.save_quit_x_pos, self.save_quit_y_pos, self.save_quit_image)
        #canvas.tag_bind(save_quit_click_area, "<Button-1>", lambda e:self.save_quit())


        # OTHER BUTTONS JUST FOR TESTING POS WONT BE SHOWN ALL THE TIME
        pay_fine_click_area,canvas, self.pay_fine_image_id = self.show_pay_fine_button(canvas)

        #return the id so that image can be hidden and shown
        yes_click_area,canvas, self.yes_image_id = self.show_yes_button(canvas)
        no_click_area, canvas, self.no_image_id = self.show_no_button(canvas)

        click_area = [roll_dice_click_area, yes_click_area, no_click_area, pay_fine_click_area, save_quit_click_area] #TODO place other click area for other buttons
        return canvas, click_area

    #------------------------#
    # EDITING MODE FUNCTIONS #
    #------------------------#

    # modifies the color of the tile in the board editor
    def modify_tile_color(self, color, tile_position):
        # gets the right color path based on the tile position (vertical or horizontal)
        if 0 < tile_position < 5 or 10 < tile_position < 15: #tile is horizontal
            color_path = f"gameplay_frame/{color}_h.png"
        else:
            color_path = f"gameplay_frame/{color}_v.png"

        #gets the appropriate image path
        image_color_path = os.path.join(assets_base_path, color_path)

        #modifies the list at the appropriate position with the new tile color reference
        self.tile_colors[tile_position][1] = tk.PhotoImage(file=image_color_path)


class NewGameFrame(DisplayManager):
    def __init__(self, gui):
        super().__init__(gui)

        # New game frame images
        self.new_game_frame_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "new_game_frame/new_game_frame_background.png"))
        self.player_box_images = [
            tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/player1_box.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/player2_box.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/player3_box.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/player4_box.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/player5_box.png")),
            tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/player6_box.png"))
        ]
        self.player_insert_demo_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "new_game_frame/player_insert_demo.png"))
        self.edit_board_button_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "new_game_frame/edit_board_button.png"))
        self.start_game_image = tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/play_button.png"))
        self.random_name_button_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "new_game_frame/random_name_dice_button.png"))
        self.exit_new_game_hint_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "new_game_frame/exit_new_game_hint.png"))
        self.yes_button_image = tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/yes_button.png"))
        self.no_button_image = tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/no_button.png"))
        self.trash_button_image = tk.PhotoImage(file=os.path.join(assets_base_path, "new_game_frame/trash_button.png"))

    # ------------------------------------# New Game Frame #------------------------------------#

    def setup_new_game_page(self, frame, input_handler):
        # Clear previously active widgets (including dice buttons)
        self.clear_active_widgets()

        # Create canvas and set background image
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.new_game_frame_background)

        # Display the back button to return to the main menu
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)
        canvas.tag_bind(back_button, "<Button-1>", lambda e: self.confirm_exit_new_game(canvas))

        # Store references to player input entries and images
        self.player_entries = [None] * 6  # To hold the entry widgets
        self.player_box_images_refs = []  # To hold image references for updating

        # Display six player insert boxes on the left side
        x_position = 300  # X position for the player boxes
        y_position = 260  # Starting Y position for player boxes

        for i, player_box_image in enumerate(self.player_box_images):
            # Display each player box image
            player_box = canvas.create_image(x_position, y_position, anchor="nw", image=player_box_image)
            self.player_box_images_refs.append(player_box)

            # Dice button for random name generation
            dice_button = tk.Button(
                canvas, image=self.random_name_button_image, bd=0, highlightthickness=0,
                highlightbackground="#FBF8F5", bg="#FBF8F5", activebackground="#FBF8F5",
                command=lambda idx=i: self.generate_random_name(canvas, idx)
            )
            dice_button.place(x=x_position - 100, y=y_position + 9)
            self.active_widgets.append(dice_button)  # Track dice button for removal

            # Trash button for clearing names
            trash_button = tk.Button(
                canvas, image=self.trash_button_image, bd=0, highlightthickness=0,
                highlightbackground="#FBF8F5", bg="#FBF8F5", activebackground="#FBF8F5",
                command=lambda idx=i: self.delete_name(canvas, idx)
            )
            trash_button.place(x=x_position - 55, y=y_position + 9)
            self.active_widgets.append(trash_button)  # Track trash button for removal

            # Set up clickable area for player box
            clickable_area = canvas.create_rectangle(
                x_position, y_position, x_position + 1.2 * player_box_image.width(),
                                        y_position + 1.2 * player_box_image.height(),
                outline="", fill=""
            )
            canvas.tag_bind(clickable_area, "<Button-1>",
                            lambda e, idx=i, x=x_position, y=y_position: self.show_insert_entry(canvas, idx, x, y))

            y_position += 100  # Adjust y-position for the next player box

        # Display Edit Board and Play buttons on the right side
        edit_board_button = canvas.create_image(self.gui.image_width - 450, 430, image=self.edit_board_button_image)
        play_button = canvas.create_image(self.gui.image_width - 450, 650, image=self.start_game_image)

        # Create clickable rectangles for Edit Board and Play buttons
        edit_board_clickable_area = canvas.create_rectangle(
            self.gui.image_width - 450 - (self.edit_board_button_image.width() * 0.6),
            430 - (self.edit_board_button_image.height() * 0.6),
            self.gui.image_width - 450 + (self.edit_board_button_image.width() * 0.6),
            430 + (self.edit_board_button_image.height() * 0.6),
            outline="", fill=""
        )
        play_button_clickable_area = canvas.create_rectangle(
            self.gui.image_width - 450 - (self.start_game_image.width() * 0.6),
            650 - (self.start_game_image.height() * 0.6),
            self.gui.image_width - 450 + (self.start_game_image.width() * 0.6),
            650 + (self.start_game_image.height() * 0.6),
            outline="", fill=""
        )

        # Bind actions for Edit Board and Play clickable areas
        canvas.tag_bind(edit_board_clickable_area, "<Button-1>",
                        lambda e: self.gui.show_frame("edit_board"))  # Placeholder action

        return canvas, play_button_clickable_area

    def clear_active_widgets(self):
        for widget in self.active_widgets:
            widget.place_forget()
        self.active_widgets.clear()  # Reset active widgets list

    def delete_name(self, canvas, idx):
        # Clear the player's name from the entry
        self.gui.input_handler.players_names[idx] = None

        # Reset the box appearance to its original state
        canvas.itemconfig(self.player_box_images_refs[idx], image=self.player_box_images[idx])
        if self.player_text_refs[idx]:  # If there was a previous name shown, remove it
            canvas.delete(self.player_text_refs[idx])
            self.player_text_refs[idx] = None
        if self.player_entries[idx]:  # If an entry widget is open, destroy it
            self.player_entries[idx].destroy()
            self.player_entries[idx] = None
        self.clicked_boxes[idx] = False  # Reset the clicked state

    def generate_random_name(self, canvas, idx):
        # Ensure that all previous player names (up to idx-1) have been entered
        if any(not self.gui.input_handler.players_names[i] for i in range(idx)):
            self.show_msg(canvas, idx, "* All previous player names must be entered first.", is_error=True)
            return

        # Generate a random name
        player_name = self.gui.input_handler.generate_name()

        # Check if the name can be stored according to validation rules
        if self.gui.input_handler.validate_and_store_name(idx, player_name):
            # Save the generated name immediately
            self.gui.input_handler.players_names[idx] = player_name

            # Always show the generated name in the player box
            self.show_insert_entry(canvas, idx, name=player_name)

            # Show a hint message to prompt the user to press Enter if they want to save manually
            self.show_msg(canvas, idx, "* You can modify the name and press <Return> to save.", is_error=False)
        else:
            # Show error if the name is invalid or duplicate
            self.show_msg(canvas, idx, "* Generated name is invalid or duplicate.", is_error=True)

    def show_insert_entry(self, canvas, idx, x_position=None, y_position=None, name=None):
        if name:
            # If a generated name is provided, show and save it immediately
            player_name = name
            self.gui.input_handler.players_names[idx] = player_name

            # Remove any existing entry widget to update the display with the new name
            if self.player_entries[idx]:
                self.player_entries[idx].destroy()
                self.player_entries[idx] = None  # Clear the reference

            canvas.itemconfig(self.player_box_images_refs[idx], image=self.player_insert_demo_image)
            if self.player_text_refs[idx]:
                canvas.delete(self.player_text_refs[idx])
            self.player_text_refs[idx] = canvas.create_text(
                400, 290 + idx * 100, text=player_name, font=("Comic Sans MS", 20), fill="#000000"
            )
        else:
            # Code for opening an entry widget for manual input
            if self.player_entries[idx]:
                self.player_entries[idx].destroy()

            if not self.clicked_boxes[idx]:
                canvas.itemconfig(self.player_box_images_refs[idx], image=self.player_insert_demo_image)
                self.clicked_boxes[idx] = True

            previous_name = str(self.gui.input_handler.players_names[idx]) if idx < len(
                self.gui.input_handler.players_names) else ""

            entry = tk.Entry(canvas, font=("Comic Sans MS", 20), width=20, bd=0, bg="#E5E8E8", fg="#000000",
                             highlightthickness=0, justify="left")

            if previous_name:
                entry.insert(0, previous_name)
            entry.place(x=x_position + 22, y=y_position + 16)
            entry.focus_set()

            def on_submit(event):
                new_name = entry.get().strip()
                # If the user press <Return> with nothing, should back to the original state without saving
                if new_name:
                    self.save_player_name(entry, idx, canvas)
                else:
                    self.delete_name(canvas, idx)  # Reset to original image if entry is empty

            entry.bind("<Return>", on_submit)
            entry.bind("<FocusOut>",
                       lambda e: on_submit(e) if entry.get().strip() else self.clear_entry(entry, idx, canvas))
            self.player_entries[idx] = entry

            if self.error_labels[idx]:
                self.error_labels[idx].destroy()

    def clear_entry(self, entry, idx, canvas):
        # Reset the player box to its original image without displaying any text
        entry.destroy()
        self.player_entries[idx] = None
        canvas.itemconfig(self.player_box_images_refs[idx], image=self.player_box_images[idx])

    def save_player_name(self, entry, idx, canvas):
        player_name = entry.get().strip()

        # Check if the name hasn't changed from the current one
        if self.gui.input_handler.players_names[idx] == player_name:
            self.show_msg(canvas, idx, "* Name did not change.", is_error=False)
            return

        # Check if the name is the same as another player
        if player_name in self.gui.input_handler.get_all_player_names():
            self.show_msg(canvas, idx, "* Name cannot be the same as another player.", is_error=True)
            return

        # Check if the previous player name has been entered (except for the first player)
        if idx > 0 and not self.gui.input_handler.players_names[idx - 1]:
            self.show_msg(canvas, idx, "* Previous player name must be entered first.", is_error=True)
            return

        # Check if the name is valid, if so, store it
        if len(player_name) <= 20 and self.gui.input_handler.validate_and_store_name(idx, player_name):
            # Clear any previous error messages
            if self.error_labels[idx]:
                self.error_labels[idx].destroy()
                self.error_labels[idx] = None

            # Remove any displayed name text reference and update with the new name
            if self.player_text_refs[idx]:
                canvas.delete(self.player_text_refs[idx])
                self.player_text_refs[idx] = None

            entry.delete(0, tk.END)  # Clear the entry to remove any leftover invalid text
            entry.insert(0, player_name)  # Ensure the valid name is displayed
            entry.destroy()

            x_text_position = 330
            y_text_position = 290 + idx * 100
            self.player_text_refs[idx] = canvas.create_text(
                x_text_position, y_text_position, text=player_name, font=("Comic Sans MS", 20), fill="#000000",
                anchor="w"
            )
        else:
            self.show_msg(canvas, idx, "* Name must be 1-20 characters.", is_error=True)
            entry.delete(0, tk.END)

    def show_msg(self, frame, idx, msg, is_error=False, x_position=None, y_position=None):
        if x_position is None:
            x_position = 325
        if y_position is None:
            y_position = 322 + idx * 100

        if self.error_labels[idx]:
            self.error_labels[idx].destroy()

        color = "red" if is_error else "green"
        self.error_labels[idx] = tk.Label(
            frame,
            text=msg,
            font=("Comic Sans MS", 16),
            fg=color,
            bg="#FBF8F5"
        )
        self.error_labels[idx].place(x=x_position, y=y_position)
        self.active_widgets.append(self.error_labels[idx])  # Track the label for later removal

    def check_and_start_game(self, input_handler):
        # Retrieve all player names
        player_names = input_handler.get_all_player_names()

        # Check for at least two valid player names
        if len([name for name in player_names if name]) < 2:
            # Show error message below play button if fewer than 2 players
            self.show_msg(self.gui.frames["new_game"], 0, "* At least two players are required to start the game.",
                          is_error=True, x_position=self.gui.image_width - 550, y_position=722)
            return False
        # If all checks pass, transition to the GameBoard frame
        print("Starting game with players:")
        for idx, name in enumerate(player_names, start=1):
            if name:
                print(f"Player {idx}: {name}")
        return True

    def confirm_exit_new_game(self, canvas):
        # Clear any previously saved positions
        self.hidden_widgets.clear()

        # Hide all tracked widgets by storing their positions and calling `place_forget`
        for widget in self.active_widgets:
            try:
                if widget.winfo_ismapped():  # Check if the widget is currently visible
                    self.hidden_widgets[widget] = widget.place_info()  # Save widget's position info
                    widget.place_forget()  # Hide the widget
            except tk.TclError:
                continue

        # Now display exit confirmation
        exit_hint = canvas.create_image(self.gui.image_width // 2 + 297, self.gui.image_height // 2 + 50,
                                        image=self.exit_new_game_hint_image)
        # Create Yes and No buttons in the popup
        yes_button = canvas.create_image(self.gui.image_width // 2 + 150, self.gui.image_height // 2 + 200,
                                         image=self.yes_button_image)
        no_button = canvas.create_image(self.gui.image_width // 2 + 440, self.gui.image_height // 2 + 200,
                                        image=self.no_button_image)

        # Bind actions for Yes and No buttons
        canvas.tag_bind(yes_button, "<Button-1>",
                        lambda e: self.exit_to_main_menu(canvas, exit_hint, yes_button, no_button))
        canvas.tag_bind(no_button, "<Button-1>",
                        lambda e: self.cancel_exit_and_restore_widgets(canvas, exit_hint, yes_button, no_button))

    def exit_to_main_menu(self, canvas, exit_hint, yes_button, no_button):
        # Clear player data, remove the exit hint, and go back to main menu
        self.clear_all_player_data(canvas)
        self.cancel_exit_and_restore_widgets(canvas, exit_hint, yes_button, no_button)
        self.gui.show_frame("main_menu")

        # Also clear all the hint messages shown in the new game frame before
        for idx in range(6):
            if self.error_labels[idx]:
                self.error_labels[idx].destroy()

    def cancel_exit_and_restore_widgets(self, canvas, exit_hint, yes_button, no_button):
        # Clear the exit hint and buttons
        canvas.delete(exit_hint)
        canvas.delete(yes_button)
        canvas.delete(no_button)

        # Restore all widgets to their original positions
        for widget, position_info in self.hidden_widgets.items():
            widget.place(**position_info)  # Re-position each widget
        self.hidden_widgets.clear()  # Clear the dictionary after restoring

    def clear_all_player_data(self, canvas):
        # Clear all entries for player data
        for idx in range(6):
            self.delete_name(canvas, idx)


class MainMenuFrame(DisplayManager):
    def __init__(self, gui):
        super().__init__(gui)
        # Main frame images
        # Main Menu images
        self.startup_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "main_menu_frame/startup_frame_background.png"))
        self.new_game_image = tk.PhotoImage(file=os.path.join(assets_base_path, "main_menu_frame/new_game_button.png"))
        self.load_game_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "main_menu_frame/load_game_button.png"))
        self.exit_image = tk.PhotoImage(file=os.path.join(assets_base_path, "main_menu_frame/exit_button.png"))
        self.info_image = tk.PhotoImage(file=os.path.join(assets_base_path, "main_menu_frame/info_button.png"))

    #------------------------------------# Main Menu Frame #------------------------------------#

    def setup_main_menu_frame(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.startup_background)

        # Button positions
        button_y_positions = [self.gui.image_height * 0.55, self.gui.image_height * 0.70, self.gui.image_height * 0.85]

        # Calculate dimensions for each button to set clickable areas
        new_game_width, new_game_height = self.calc_button_dim(self.new_game_image)
        load_game_width, load_game_height = self.calc_button_dim(self.load_game_image)
        exit_width, exit_height = self.calc_button_dim(self.exit_image)
        info_width, info_height = self.calc_button_dim(self.info_image)

        # "New Game" button and clickable area
        new_game_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[0],
                                              image=self.new_game_image)
        new_game_clickable_area = canvas.create_rectangle(
            (self.gui.image_width // 2) - (0.6 * new_game_width), button_y_positions[0] - (0.6 * new_game_height),
            (self.gui.image_width // 2) + (0.6 * new_game_width), button_y_positions[0] + (0.6 * new_game_height),
            outline="", fill=""
        )
        canvas.tag_bind(new_game_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("new_game"))

        # "Load Game" button and clickable area
        load_game_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[1],
                                               image=self.load_game_image)
        load_game_clickable_area = canvas.create_rectangle(
            (self.gui.image_width // 2) - (0.6 * load_game_width), button_y_positions[1] - (0.6 * load_game_height),
            (self.gui.image_width // 2) + (0.6 * load_game_width), button_y_positions[1] + (0.6 * load_game_height),
            outline="", fill=""
        )
        canvas.tag_bind(load_game_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("load_game"))

        # "Exit" button and clickable area
        exit_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[2], image=self.exit_image)
        exit_clickable_area = canvas.create_rectangle(
            (self.gui.image_width // 2) - (0.6 * exit_width), button_y_positions[2] - (0.6 * exit_height),
            (self.gui.image_width // 2) + (0.6 * exit_width), button_y_positions[2] + (0.6 * exit_height),
            outline="", fill=""
        )
        canvas.tag_bind(exit_clickable_area, "<Button-1>", lambda e: self.gui.quit())

        # "Info" button in the corner and clickable area
        info_button = canvas.create_image(self.gui.image_width - 85, 75, image=self.info_image)
        info_clickable_area = canvas.create_rectangle(
            (self.gui.image_width - 85) - (0.6 * info_width), 75 - (0.6 * info_height),
            (self.gui.image_width - 85) + (0.6 * info_width), 75 + (0.6 * info_height),
            outline="", fill=""
        )
        canvas.tag_bind(info_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("info"))

        return canvas


class LoadGameFrame(DisplayManager):
    def __init__(self, gui):
        super().__init__(gui)

        self.load_and_play_button_id = None
        self.saved_game_slots = []
        self.slot_item_ids = [] # Track item IDs for slots

        # Load Game frame images
        self.load_game_frame_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "load_game_frame/load_game_frame_background.png"))
        self.saved_game_slot1_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "load_game_frame/saved_game_slot1.png"))
        self.saved_game_slot2_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "load_game_frame/saved_game_slot2.png"))
        self.saved_game_slot3_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "load_game_frame/saved_game_slot3.png"))
        self.saved_game_slot4_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "load_game_frame/saved_game_slot4.png"))
        self.saved_game_slot5_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "load_game_frame/saved_game_slot5.png"))
        self.selected_saved_game_slot_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "load_game_frame/selected_saved_game_slot.png"))
        self.load_and_play_button_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "load_game_frame/load_and_play_button.png"))
        self.display_text = []
        self.save_base_path = os.path.join(os.path.dirname(__file__), "../../saves/games")

    # ------------------------------------# Load Game Frame #------------------------------------#

    def setup_load_game_frame(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.load_game_frame_background)

        # Saved game slot selection image positions
        self.saved_game_slot_positions = [
            (self.gui.image_width // 2, 370),
            (self.gui.image_width // 2, 452),
            (self.gui.image_width // 2, 534),
            (self.gui.image_width // 2, 616),
            (self.gui.image_width // 2, 698)
        ]

        # Saved game slot images
        self.saved_game_slots = [
            self.saved_game_slot1_image,
            self.saved_game_slot2_image,
            self.saved_game_slot3_image,
            self.saved_game_slot4_image,
            self.saved_game_slot5_image
        ]

        # Display saved game slots
        for i, slot_image in enumerate(self.saved_game_slots):
            slot_x, slot_y = self.saved_game_slot_positions[i]  # Unpack coordinates
            slot_id = canvas.create_image(slot_x, slot_y, image=slot_image)
            self.slot_item_ids.append(slot_id)

            # Create a clickable area for each slot
            clickable_area = canvas.create_rectangle(
                slot_x - (0.5 * slot_image.width()), slot_y - (0.5 * slot_image.height()),
                slot_x + (0.5 * slot_image.width()), slot_y + (0.5 * slot_image.height()),
                outline="", fill=""
            )

            # Bind click event to select the slot
            canvas.tag_bind(clickable_area, "<Button-1>",
                            lambda e, idx=i: self.select_saved_game_slot(canvas, idx))

        # Display the back button to return to the main menu
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)
        canvas.tag_bind(back_button, "<Button-1>", lambda e: self.gui.show_frame("main_menu"))

        self.show_save_file(canvas)

        return canvas

    def clear_selected_slots(self,canvas):
        for i, slot_id in enumerate(self.slot_item_ids):
            canvas.itemconfig(slot_id, image=self.saved_game_slots[i])

    def select_saved_game_slot(self, canvas, idx):
        # Clear any previously selected slots by resetting all slots to their original images
        self.clear_selected_slots(canvas)

        # Update only the selected slot with the highlight image
        canvas.itemconfig(self.slot_item_ids[idx], image=self.selected_saved_game_slot_image)
        self.gui.selected_saved_game_slot = idx

        # Display Load and Play button once a slot is selected
        if self.load_and_play_button_id is not None:
            canvas.delete(self.load_and_play_button_id)
        load_button_x, load_button_y = self.gui.image_width // 2, 835
        self.load_and_play_button_id = canvas.create_image(load_button_x, load_button_y,
                                                           image=self.load_and_play_button_image)
        load_and_play_clickable_area = canvas.create_rectangle(
            load_button_x - (0.5 * self.load_and_play_button_image.width()),
            load_button_y - (0.5 * self.load_and_play_button_image.height()),
            load_button_x + (0.5 * self.load_and_play_button_image.width()),
            load_button_y + (0.5 * self.load_and_play_button_image.height()),
            outline="", fill=""
        )

        canvas.tag_bind(load_and_play_clickable_area, "<Button-1>", lambda e: self.load_data(idx))

        return canvas

    def load_data(self,idx):
        from src.Controller.GameController import GameController
        g=GameController(self.gui)
        if idx<len(self.display_text):
            print(self.display_text[idx][2].split('.')[0])
            g.load_game(self.display_text[idx][2].split('.')[0])
            self.gui.show_game_play_frame()
            self.gui.show_frame("gameplay")

    def show_save_file(self,canvas):
        for obj in self.display_text:
            for i in range(2):
                canvas.delete(obj[i])
        self.display_text=[]

        file_info = []
        for filename in os.listdir(self.save_base_path):
            last_modified_time = os.path.getmtime(os.path.join(self.save_base_path, filename))
            last_modified_time_str = time.ctime(last_modified_time)
            file_info.append((filename, last_modified_time_str))

        for i in range(5):
            if i < len(file_info):
                text1=canvas.create_text(self.gui.image_width // 3, self.saved_game_slot_positions[i][1], text=file_info[i][0], anchor="center",
                                   font=("Comic Sans MS", 16), fill="#000000")
                text2=canvas.create_text(self.gui.image_width * 19 // 30, self.saved_game_slot_positions[i][1], text=file_info[i][1], anchor="center",
                                   font=("Comic Sans MS", 16), fill="#000000")
                self.display_text.append([text1,text2,file_info[i][0]])
                canvas.tag_bind(text1, "<Button-1>",
                                lambda e, idx=i: self.select_saved_game_slot(canvas, idx))
                canvas.tag_bind(text2, "<Button-1>",
                                lambda e, idx=i: self.select_saved_game_slot(canvas, idx))


class SaveGameFrame(DisplayManager):
    def __init__(self, gui):
        super().__init__(gui)

        self.save_button_id = None
        self.delete_button_id = None
        self.saved_game_slots = []
        self.slot_item_ids = [] # Track item IDs for slots

        # Load Game frame images
        self.save_game_frame_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "save_game_frame/save_game_frame_background.png"))
        self.saved_game_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "save_game_frame/saved_game.png"))
        self.selected_saved_game_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "save_game_frame/selected_saved_game.png"))
        self.save_button_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "save_game_frame/save.png"))
        self.delete_button_image = tk.PhotoImage(
            file=os.path.join(assets_base_path, "save_game_frame/delete.png"))
        self.back_arrow_image = tk.PhotoImage(file=os.path.join(assets_base_path, "info_frame/back_arrow.png"))
        self.home_icon_image=tk.PhotoImage(file=os.path.join(assets_base_path, "save_game_frame/home_button.png"))
        self.save_base_path = os.path.join(os.path.dirname(__file__), "../../saves/games")
        self.display_text=[]

        # ----------- buttons position and initialization -----------#
        self.delete_button_x, self.delete_button_y = self.gui.image_width // 3, 835
        self.save_button_x, self.save_button_y = self.gui.image_width * 2 // 3, 835


    # ------------------------------------# Load Game Frame #------------------------------------#

    def setup_save_game_frame(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.save_game_frame_background)

        # Saved game slot selection image positions
        self.saved_game_slot_positions = [
            (self.gui.image_width // 2, 370),
            (self.gui.image_width // 2, 452),
            (self.gui.image_width // 2, 534),
            (self.gui.image_width // 2, 616),
            (self.gui.image_width // 2, 698)
        ]

        # Saved game slot images
        self.saved_game_slots = [
            self.saved_game_image,
            self.saved_game_image,
            self.saved_game_image,
            self.saved_game_image,
            self.saved_game_image
        ]
        # create delete and save button and hide them from screen first
        canvas, delete_click_area = self.create_delete_button(canvas)
        canvas, save_click_area = self.create_save_button(canvas)

        # hide them
        self.hide_delete_button(canvas)
        self.hide_save_button(canvas)

        # save and delete clickable area, the first is the save button, second is the delete button
        save_delete_click_area = [save_click_area, delete_click_area]
        # Display the back button to return to the main menu
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)
        # canvas.tag_bind(back_button, "<Button-1>", lambda e: self.back_button(canvas))
        save_delete_click_area.append(back_button)

        # Display saved game slots
        for i, slot_image in enumerate(self.saved_game_slots):
            slot_x, slot_y = self.saved_game_slot_positions[i]  # Unpack coordinates
            slot_id = canvas.create_image(slot_x, slot_y, image=slot_image)
            self.slot_item_ids.append(slot_id)

            # Create a clickable area for each slot
            clickable_area = canvas.create_rectangle(
                slot_x - (0.5 * slot_image.width()), slot_y - (0.5 * slot_image.height()),
                slot_x + (0.5 * slot_image.width()), slot_y + (0.5 * slot_image.height()),
                outline="", fill=""
            )
            save_delete_click_area.append(clickable_area)

        home_button = canvas.create_image(self.gui.image_width-50, 50, image=self.home_icon_image)
        canvas.tag_bind(home_button, "<Button-1>", lambda e: self.gui.show_frame("main_menu"))

        self.show_save_file(canvas)

        return canvas, save_delete_click_area  # return to GUI, and the Controller will do operations on it

    # The functionality of a back button in game saving page
    def back_button(self, canvas):

        # Hide all delete and save button before going back to gameplay page
        self.hide_delete_button(canvas)
        self.hide_save_button(canvas)
        self.clear_selected_slots(canvas)
        self.gui.show_frame("gameplay")

    # ------------------------------------ Functions for Creating Delete and Save Button------------------------------------#
    def create_rectangle(self,canvas,x,y):

        clickable_area = canvas.create_rectangle(
            x - (0.5 * self.save_button_image.width()),
            y - (0.5 * self.save_button_image.height()),
            x + (0.5 * self.save_button_image.width()),
            y + (0.5 * self.save_button_image.height()),
            outline="", fill=""
        )
        return clickable_area

    def create_delete_button(self,canvas):
        # if self.delete_button_id is not None:
        #     canvas.delete(self.delete_button_id)

        self.delete_button_id = canvas.create_image(self.delete_button_x, self.delete_button_y,
                                                           image=self.delete_button_image)
        delete_clickable_area = self.create_rectangle(canvas,self.delete_button_x,self.delete_button_y)

        return canvas,delete_clickable_area

    def create_save_button(self,canvas):
        # save button
        # if self.save_button_id is not None:
        #     canvas.delete(self.save_button_id)
        self.save_button_id = canvas.create_image(self.save_button_x, self.save_button_y,
                                                  image=self.save_button_image)
        save_clickable_area = self.create_rectangle(canvas,self.save_button_x,self.save_button_y)

        return canvas,save_clickable_area

    # ------------------------------------ Functions for Showing Delete and Save Button--------------------------------------#
    def show_delete_button(self,canvas):
        canvas.coords(self.delete_button_id, self.delete_button_x, self.delete_button_y)

    def show_save_button(self,canvas):
        canvas.coords(self.save_button_id, self.save_button_x, self.save_button_y)

    # -----------------------------------------------------------------------------------------------------------------------#



    # ------------------------------------ Functions for Hiding Delete and Save Button---------------------------------------#
    def hide_delete_button(self,canvas):
        canvas.coords(self.delete_button_id, -100,-100)

    def hide_save_button(self,canvas):
        canvas.coords(self.save_button_id, -100,-100)
    # -----------------------------------------------------------------------------------------------------------------------#

    def clear_selected_slots(self,canvas):
        for i, slot_id in enumerate(self.slot_item_ids):
            canvas.itemconfig(slot_id, image=self.saved_game_slots[i])

    def select_saved_game_slot(self, canvas, idx):

        # Clear any previously selected slots by resetting all slots to their original images
        self.clear_selected_slots(canvas)

        # Update only the selected slot with the highlight image
        canvas.itemconfig(self.slot_item_ids[idx], image=self.selected_saved_game_image)
        self.gui.selected_saved_game_slot = idx

        #show delete button
        self.show_delete_button(canvas)

        # show save button
        self.show_save_button(canvas)

        return canvas

    def save_data(self, canvas):
        self.gui.show_frame("save_game")
        self.show_save_file(canvas)

    def delete_data(self, canvas):
        if self.gui.selected_saved_game_slot < len(self.display_text):
            filepath = os.path.join(self.save_base_path, self.display_text[self.gui.selected_saved_game_slot][2])
            os.remove(filepath)
        self.show_save_file(canvas)

    def show_save_file(self, canvas):
        for obj in self.display_text:
            for i in range(2):
                canvas.delete(obj[i])
        self.display_text = []

        file_info = []
        for filename in os.listdir(self.save_base_path):
            last_modified_time = os.path.getmtime(os.path.join(self.save_base_path, filename))
            last_modified_time_str = time.ctime(last_modified_time)
            file_info.append((filename, last_modified_time_str))

        for i in range(5):
            if i < len(file_info):
                text1 = canvas.create_text(self.gui.image_width // 3, self.saved_game_slot_positions[i][1],
                                           text=file_info[i][0], anchor="center",
                                           font=("Comic Sans MS", 16), fill="#000000")
                text2 = canvas.create_text(self.gui.image_width * 19 // 30, self.saved_game_slot_positions[i][1],
                                           text=file_info[i][1], anchor="center",
                                           font=("Comic Sans MS", 16), fill="#000000")
                self.display_text.append([text1, text2, file_info[i][0]])
                canvas.tag_bind(text1, "<Button-1>",
                                lambda e, idx=i: self.select_saved_game_slot(canvas, idx))
                canvas.tag_bind(text2, "<Button-1>",
                                lambda e, idx=i: self.select_saved_game_slot(canvas, idx))

class EnterNameFrame(SaveGameFrame):
    def __init__(self, gui):
        super().__init__(gui)
        self.enter_name_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "save_game_frame/enter_name.png"))
        self.save_photo = tk.PhotoImage(
            file=os.path.join(assets_base_path, "save_game_frame/color_save.png"))
        self.back_photo = tk.PhotoImage(
            file=os.path.join(assets_base_path, "save_game_frame/back.png"))
        self.name_entry=None
        self.error_label=None


    def setup_enter_name_frame(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.save_game_frame_background)
        # Saved game slot selection image positions
        self.saved_game_slot_positions = [
            (self.gui.image_width // 2, 370),
            (self.gui.image_width // 2, 452),
            (self.gui.image_width // 2, 534),
            (self.gui.image_width // 2, 616),
            (self.gui.image_width // 2, 698)
        ]

        # Saved game slot images
        self.saved_game_slots = [
            self.saved_game_image,
            self.saved_game_image,
            self.saved_game_image,
            self.saved_game_image,
            self.saved_game_image
        ]
        # create delete and save button and hide them from screen first
        canvas, delete_click_area = self.create_delete_button(canvas)
        canvas, save_click_area = self.create_save_button(canvas)

        # hide them
        self.hide_delete_button(canvas)
        self.hide_save_button(canvas)

        # save and delete clickable area, the first is the save button, second is the delete button
        save_delete_click_area = [save_click_area, delete_click_area]
        # Display saved game slots
        for i, slot_image in enumerate(self.saved_game_slots):
            slot_x, slot_y = self.saved_game_slot_positions[i]  # Unpack coordinates
            slot_id = canvas.create_image(slot_x, slot_y, image=slot_image)
            self.slot_item_ids.append(slot_id)

        # Display the back button to return to the main menu
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)

        home_button = canvas.create_image(self.gui.image_width-50, 50, image=self.home_icon_image)

        enter_name_background=canvas.create_image(self.gui.image_width // 2,self.gui.image_height // 2,image=self.enter_name_background,anchor="center")

        if self.name_entry!=None:
            canvas.delete(self.name_entry)
        self.name_entry = tk.Entry(frame, width=self.enter_name_background.width()*2//3, font=("Comic Sans MS", 40))
        self.name_entry.place(x=self.gui.image_width // 2, y=self.gui.image_height // 2-self.enter_name_background.height()/10, width=self.enter_name_background.width()*2//3, height=80,anchor="center")

        self.color_save_button=canvas.create_image(self.gui.image_width // 2,self.gui.image_height // 2+self.enter_name_background.height()/6,image=self.save_photo,anchor="center")
        self.enter_back_button=canvas.create_image(self.gui.image_width // 2,self.gui.image_height // 2+self.enter_name_background.height()/3,image=self.back_photo,anchor="center")



        #canvas.tag_bind(self.color_save_button, "<Button-1>",
        #               lambda e, idx=i: self.gui.show_frame("save_game"))

        canvas.tag_bind(self.enter_back_button, "<Button-1>",
                        lambda e, idx=i: self.back_to_save_game_frame())


        return canvas # return to GUI, and the Controller will do operations on

    def back_to_save_game_frame(self):
        self.clear_all_info()
        self.gui.show_frame("save_game")

    def wrong_save_name(self,frame):
        self.name_entry.delete(0, tk.END)
        self.show_msg(frame)

    def clear_all_info(self):
        self.name_entry.delete(0, tk.END)
        if self.error_label:
            self.error_label.place_forget()

    def show_msg(self, frame):
        x_position = 600
        y_position = 480
        #
        if self.error_label:
            self.error_label.destroy()
            self.error_label=None

        self.error_label = tk.Label(
            frame,
            text="Invalid Name. Please Enter Again",
            font=("Comic Sans MS", 16),
            fg="red",
            bg="#FBF8F5"
        )
        self.error_label.place(x=x_position, y=y_position)

class InfoPageFrame(DisplayManager):
    def __init__(self, gui):
        super().__init__(gui)

        # Info frame images
        self.info_frame_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "info_frame/info_frame_background.png"))

    # --------------------------------------# Info Page #---------------------------------------#

    def setup_info_page(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.info_frame_background)

        # Back button dimensions for creating a larger clickable area
        back_button_width, back_button_height = self.back_arrow_image.width(), self.back_arrow_image.height()

        # Display the back button to return to the main menu
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)

        # Create a clickable rectangle slightly larger than the back button image
        back_button_clickable_area = canvas.create_rectangle(
            50 - (0.2 * back_button_width), 50 - (0.2 * back_button_height),  # Top-left corner
            50 + back_button_width * 1.2, 50 + back_button_height * 1.2,  # Bottom-right corner
            outline="", fill=""
        )

        # Bind the enlarged clickable area to the main menu transition
        canvas.tag_bind(back_button_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("main_menu"))

        return canvas




class EditBoardFrame(GameplayFrame):
    def __init__(self, gui):
        super().__init__(gui)
        self.edit_board_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "edit_gameboard_frame/editboard_frame_background.png"))
        self.confirm_photo=tk.PhotoImage(
            file=os.path.join(assets_base_path, "edit_gameboard_frame/confirm.png"))
        self.cancel_photo=tk.PhotoImage(
            file=os.path.join(assets_base_path, "edit_gameboard_frame/cancel.png"))
        self.back_arrow_photo=tk.PhotoImage(
            file=os.path.join(assets_base_path, "edit_gameboard_frame/back_arrow.png"))

        self.property_coordinates=[[567, 820, 700, 953, 1], [431, 819, 568, 951, 2], [164, 817, 296, 953, 4], [27, 684, 160, 816, 6], [28, 549, 161, 684, 7],
                                   [28,278,160,413,9], [161,147,297,278,11], [433,144,567,279,13], [568,144,700,278,14], [700,278,833,413,16], [704,415,837,547,17], [701,685,835,817,19]]

        self.name_entry=None
        self.price_entry=None
        self.rent_entry=None
        self.current_frame=None
        self.grid_index=-1
        self.clear=[]
        self.canvas=None

    def setup_edit_board_frame(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.edit_board_background)
        self.current_frame=frame
        self.canvas=canvas
        cancel_click_area, canvas, cancel_id = self.create_button(canvas, 1051, 897, self.cancel_photo)
        confirm_click_area, canvas, confirm_id = self.create_button(canvas, 1318, 897, self.confirm_photo)
        back_click_area, canvas, back_id = self.create_button(canvas, 50, 50, self.back_arrow_photo)

        canvas.tag_bind(back_click_area, "<Button-1>", lambda e: self.gui.show_frame("new_game"))
        canvas.tag_bind(cancel_click_area, "<Button-1>", lambda e: self.remove_entries())
        canvas.tag_bind(confirm_click_area, "<Button-1>", lambda e: self.process_user_input())

        game_board_area = canvas.create_rectangle(27, 144, 836, 954, outline="", fill="", tags="game_board")
        canvas.tag_bind("game_board", '<Button-1>', self.on_game_board_click)
        self.display_tile_info(canvas)

    def on_game_board_click(self, event):
        self.remove_entries()
        x = event.x
        y = event.y
        print(f"Coordinates: ({x}, {y})")
        self.grid_index=self.check_click_grid(x,y)
        if self.grid_index!=-1:
            print(GameplayFrame.tile_info[self.grid_index])
            self.create_input_entries(self.current_frame)

    def check_click_grid(self,x,y):
        grid_index=-1
        for top_left_x,top_left_y,bottom_right_x,bottom_right_y,index in self.property_coordinates:
            if self.check_inside_grid(x,y,top_left_x,top_left_y,bottom_right_x,bottom_right_y):
                grid_index=index
                break
        return grid_index

    def check_inside_grid(self,x,y,top_left_x,top_left_y,bottom_right_x,bottom_right_y):
        return top_left_x<=x<=bottom_right_x and top_left_y<=y<=bottom_right_y

    def create_input_entries(self,frame):
        self.name_entry = tk.Entry(frame, width=400, font=("Comic Sans MS", 40))
        self.price_entry = tk.Entry(frame, width=400, font=("Comic Sans MS", 40))
        self.rent_entry = tk.Entry(frame, width=400, font=("Comic Sans MS", 40))
        self.name_entry.place(x=1188, y=390, width=400, height=80,anchor="center")
        self.price_entry.place(x=1188, y=570, width=400, height=80,anchor="center")
        self.rent_entry.place(x=1188, y=760, width=400, height=80,anchor="center")
        self.name_entry.insert(0, GameplayFrame.tile_info[self.grid_index][1]) # 1 is "name"
        self.price_entry.insert(0, GameplayFrame.tile_info[self.grid_index][2]) # 2 is "price"
        self.rent_entry.insert(0, GameplayFrame.tile_info[self.grid_index][3]) # 3 is "rent"

    def remove_entries(self):
        if self.name_entry is not None:
            self.name_entry.destroy()
        if self.price_entry is not None:
            self.price_entry.destroy()
        if self.rent_entry is not None:
            self.rent_entry.destroy()

    def process_user_input(self):
        name= self.name_entry.get()
        price= self.price_entry.get()
        rent= self.rent_entry.get()
        #check valid and if valid
        GameplayFrame.tile_info[self.grid_index][1] = name
        GameplayFrame.tile_info[self.grid_index][2] = price
        GameplayFrame.tile_info[self.grid_index][3] = rent
        self.remove_entries()
        self.canvas = self.remove_game_board_text(self.canvas)
        self.display_tile_info(self.canvas)
        self.canvas.update()
        print(GameplayFrame.tile_info)

    def remove_game_board_text(self,canvas):
        for j in range(0, 20):
            for i in range(5, 8):
                canvas.delete(GameplayFrame.tile_info[self.grid_index][i])
                GameplayFrame.tile_info[self.grid_index][i] = None
        return canvas
