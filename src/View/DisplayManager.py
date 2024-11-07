import tkinter as tk
import os

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


class GameplayFrame(DisplayManager):
    def __init__(self, gui):
        super().__init__(gui)

        # New Gameplay frame images
        self.new_gameplay_frame_background = tk.PhotoImage(
            file=os.path.join(assets_base_path, "gameplay_frame/gameplay_frame_background.png"))
        self.roll_dice_image = tk.PhotoImage(file = os.path.join(assets_base_path, "gameplay_frame/roll_dice.png"))
        self.save_quit_image = tk.PhotoImage(file = os.path.join(assets_base_path, "gameplay_frame/save_quit.png"))

        # Gameboard tiles colors empty list, will get loaded from the Gameboard model
        self.tile_colors = []

        # Tile color coordinates from anchor (reference point) "NW" corner
        self.__tile_color_coord = [
            None,
            [565, 818],
            [430, 818],
            None,
            [160, 818],
            None,
            [118, 683],
            [118, 548],
            None,
            [118, 278],
            None,
            [565, 236],
            None,
            [430, 236],
            [160, 236],
            None,
            [700, 278],
            [700, 413],
            None,
            [700, 683]
        ]

# ------------------------------------# Game Play Frame #------------------------------------#

    def set_color(self, pos, color):
        self.tile_colors[pos] = color

    def get_color_coord(self, pos):
        return self.__tile_color_coord[pos]

    # from the gameboard information loads the appropriate colors in the game frame
    def load_tile_colors(self):
        for i in range(0,20):
            color = self.tile_colors[i]
            if color:
                self.modify_tile_color(color, i)

    # gets the information from the lists above and display all the tiles colors
    def overlay_tile_colors(self, canvas):
        for i in range(0, 20):
            color_tuple = self.__tile_color_coord[i]
            if color_tuple: # if None (meaning at that position there is a tile that has no color) doesn't execute
                x_pos = color_tuple[0]
                y_pos = color_tuple[1]
                tile_color = self.tile_colors[i]
                canvas.create_image(x_pos, y_pos, anchor="nw", image=tile_color)

    # rolls the dice
    def roll_dice(self):
        print("Rolling dice...")

    def save_quit(self):
        print("Saving quit...")

    # called to set up the entire gameplay_frame
    def setup_new_gameplay_frame(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.new_gameplay_frame_background)

        # loads tile colors and displays them
        self.load_tile_colors()
        self.overlay_tile_colors(canvas)

        # buttons dimensions
        roll_dice_width, roll_dice_height = self.calc_button_dim(self.roll_dice_image)
        save_quit_width, save_quit_height = self.calc_button_dim(self.save_quit_image)

        # roll_dice_button & clickable area
        # position based on center
        roll_dice_x_pos = self.gui.image_width * 2 / 7
        roll_dice_y_pos = self.gui.image_height * 2 / 5
        roll_dice_button = canvas.create_image(roll_dice_x_pos, roll_dice_y_pos, anchor="center", image=self.roll_dice_image)
        roll_dice_clickable_area = canvas.create_rectangle(
            (roll_dice_x_pos - roll_dice_width // 2), (roll_dice_y_pos - roll_dice_height // 2),
            (roll_dice_x_pos + roll_dice_width // 2), (roll_dice_y_pos + roll_dice_height // 2),
            outline="", fill=""
        )
        canvas.tag_bind(roll_dice_clickable_area, "<Button-1>", lambda e:self.roll_dice())

        # save_quit button & clickable area
        save_quit_x_pos = self.gui.image_width * 10 / 14
        save_quit_y_pos = self.gui.image_height * 9 / 10
        save_quit_button = canvas.create_image(save_quit_x_pos, save_quit_y_pos, anchor="center", image=self.save_quit_image)
        save_quit_clickable_area = canvas.create_rectangle(
            (save_quit_x_pos - roll_dice_width // 2), (save_quit_y_pos - roll_dice_height // 2),
            (save_quit_x_pos + roll_dice_width // 2), (save_quit_y_pos + roll_dice_height // 2),
            outline="", fill=""
        )
        canvas.tag_bind(save_quit_clickable_area, "<Button-1>", lambda e:self.save_quit())
        return canvas

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
        self.tile_colors[tile_position] = tk.PhotoImage(file=image_color_path)


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
                        lambda e: print("Edit board clicked"))  # Placeholder action
        canvas.tag_bind(play_button_clickable_area, "<Button-1>", lambda e: self.check_and_start_game(input_handler))

        return canvas

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
        # Check if the previous player name has been entered (except for the first player)
        if idx > 0 and not self.gui.input_handler.players_names[idx - 1]:
            self.show_msg(canvas, idx, "* Previous player name must be entered first.", is_error=True)
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
        self.gui.show_game_play_frame()  # TODO uncomment this line later

        # Retrieve all player names
        player_names = input_handler.get_all_player_names()

        # Check for at least two valid player names
        if len([name for name in player_names if name]) < 2:
            # Show error message below play button if fewer than 2 players
            self.show_msg(self.gui.frames["new_game"], 0, "* At least two players are required to start the game.",
                          is_error=True, x_position=self.gui.image_width - 550, y_position=722)
            return

        # If all checks pass, transition to the GameBoard frame
        print("Starting game with players:")
        for idx, name in enumerate(player_names, start=1):
            if name:
                print(f"Player {idx}: {name}")

        # Show the GameBoard frame
        self.gui.show_frame("gameplay")

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

    # ------------------------------------# Load Game Frame #------------------------------------#

    def setup_load_game_frame(self, frame):
        canvas = self.clear_widgets_create_canvas_set_background(frame, self.load_game_frame_background)

        # Saved game slot selection image positions
        saved_game_slot_positions = [
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
            slot_x, slot_y = saved_game_slot_positions[i]  # Unpack coordinates
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

        return canvas

    def select_saved_game_slot(self, canvas, idx):
        # Clear any previously selected slots by resetting all slots to their original images
        for i, slot_id in enumerate(self.slot_item_ids):
            canvas.itemconfig(slot_id, image=self.saved_game_slots[i])

        # Update only the selected slot with the highlight image
        canvas.itemconfig(self.slot_item_ids[idx], image=self.selected_saved_game_slot_image)
        self.gui.selected_saved_game_slot = idx

        # Display Load and Play button once a slot is selected
        if not hasattr(self, 'load_and_play_button_id'):
            # Reuse this Load and Play button
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

            # TODO Once the button is clicked, pass the json file name to the controller to load the game board
            # canvas.tag_bind(load_and_play_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("gameplay"))

        return canvas


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


class EditBoardFrame(DisplayManager):
    def __init__(self, gui):
        super().__init__(gui)

