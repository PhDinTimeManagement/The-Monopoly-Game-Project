# display.py
import tkinter as tk

class DisplayManager:
    def __init__(self, gui):
        self.gui = gui  # Reference to the main GUI instance
        self.error_labels = [None] * 6  # To hold error messages for player names
        self.player_entries = []  # To hold player name entry widgets
        self.player_box_images_refs = []  # To hold player box image references
        self.player_text_refs = [None] * 6  # To store references to the text displayed in each player box


        # Main Menu images
        self.startup_background = tk.PhotoImage(file="../../assets/startup_frame/startup_frame_background.png")
        self.new_game_image = tk.PhotoImage(file="../../assets/startup_frame/new_game_button.png")
        self.load_game_image = tk.PhotoImage(file="../../assets/startup_frame/load_game_button.png")
        self.exit_image = tk.PhotoImage(file="../../assets/startup_frame/exit_button.png")
        self.info_image = tk.PhotoImage(file="../../assets/startup_frame/info_button.png")

        # Info frame images
        self.info_frame_background = tk.PhotoImage(file="../../assets/info_frame/info_frame_background.png")
        self.back_arrow_image = tk.PhotoImage(file="../../assets/info_frame/back_arrow.png")

        # New game frame images
        self.new_game_frame_background = tk.PhotoImage(file="../../assets/new_game_frame/new_game_frame_background.png")
        self.player_box_images = [
            tk.PhotoImage(file="../../assets/new_game_frame/player1_box.png"),
            tk.PhotoImage(file="../../assets/new_game_frame/player2_box.png"),
            tk.PhotoImage(file="../../assets/new_game_frame/player3_box.png"),
            tk.PhotoImage(file="../../assets/new_game_frame/player4_box.png"),
            tk.PhotoImage(file="../../assets/new_game_frame/player5_box.png"),
            tk.PhotoImage(file="../../assets/new_game_frame/player6_box.png")
        ]
        self.player_insert_demo_image = tk.PhotoImage(file="../../assets/new_game_frame/player_insert_demo.png")
        self.edit_board_button_image = tk.PhotoImage(file="../../assets/new_game_frame/edit_board_button.png")
        self.start_game_image = tk.PhotoImage(file="../../assets/new_game_frame/play_button.png")

    def setup_main_menu(self, frame):
        # Clear any existing widgets in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.gui.image_height, width=self.gui.image_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.startup_background)

        # Button positions
        button_y_positions = [self.gui.image_height * 0.55, self.gui.image_height * 0.70, self.gui.image_height * 0.85]

        # "New Game" button
        new_game_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[0], image=self.new_game_image)
        canvas.tag_bind(new_game_button, "<Button-1>", lambda e: self.gui.show_frame("NewGamePage"))

        # "Load Game" button
        load_game_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[1], image=self.load_game_image)
        canvas.tag_bind(load_game_button, "<Button-1>", lambda e: self.gui.show_frame("LoadPage"))

        # "Exit" button
        exit_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[2], image=self.exit_image)
        canvas.tag_bind(exit_button, "<Button-1>", lambda e: self.gui.quit())

        # "Info" button in the corner
        info_button = canvas.create_image(self.gui.image_width - 85, 75, image=self.info_image)
        canvas.tag_bind(info_button, "<Button-1>", lambda e: self.gui.show_frame("InfoPage"))

        return canvas

    def setup_info_page(self, frame):
        # Clear any existing widgets in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Create the canvas and set the background image
        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.gui.image_height, width=self.gui.image_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.info_frame_background)

        # Display the back button to return to the main menu
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)

        # Use tag_bind to associate the back button click with show_frame("MainMenu")
        canvas.tag_bind(back_button, "<Button-1>", lambda e: self.gui.show_frame("MainMenu"))

        return canvas

    def setup_new_game_page(self, frame, input_handler):
        # Clear any existing widgets in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Create the canvas and set the background image
        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.gui.image_height, width=self.gui.image_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.new_game_frame_background)

        # Display the back button to return to the main menu
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)
        canvas.tag_bind(back_button, "<Button-1>", lambda e: self.gui.show_frame("MainMenu"))

        # Store references to player input entries and images
        self.player_entries = [None] * 6  # To hold the entry widgets
        self.player_box_images_refs = []  # To hold image references for updating

        # Display six player insert boxes on the left side
        x_position = 300  # X position for the player boxes
        y_position = 260  # Starting Y position for player boxes

        for i, player_box_image in enumerate(self.player_box_images):
            # Display each player box image
            player_box = canvas.create_image(x_position, y_position, anchor="nw", image=player_box_image)
            self.player_box_images_refs.append(player_box)  # Store the image reference

            # Bind click event to show insert demo and entry box
            canvas.tag_bind(player_box, "<Button-1>",
                            lambda e, idx=i, x=x_position, y=y_position: self.show_insert_entry(canvas, idx, x, y))

            y_position += 100  # Adjust y-position for the next player box

        # Display Edit Board and Play buttons on the right side
        edit_board_button = canvas.create_image(self.gui.image_width - 450, 430, image=self.edit_board_button_image)
        play_button = canvas.create_image(self.gui.image_width - 450, 650, image=self.start_game_image)

        # Bind actions for Edit Board and Play buttons
        canvas.tag_bind(edit_board_button, "<Button-1>", lambda e: print("Edit board clicked"))  # Placeholder action
        canvas.tag_bind(play_button, "<Button-1>", lambda e: self.start_game(input_handler))

        return canvas

    def show_insert_entry(self, canvas, idx, x_position, y_position):
        # Replace player box image with the demo image
        canvas.itemconfig(self.player_box_images_refs[idx], image=self.player_insert_demo_image)

        # If an entry already exists, remove it
        if self.player_entries[idx]:
            self.player_entries[idx].destroy()

        # Create an entry field for input
        entry = tk.Entry(canvas, font=("Comic Sans MS", 20), width=20, bd=0, bg="#E5E8E8", fg="#000000",
                         highlightthickness=0, justify="left")
        entry.place(x=x_position + 22, y=y_position + 16)
        entry.focus_set()

        # Bind Enter key to submit input
        entry.bind("<Return>", lambda e: self.save_player_name(entry, idx, canvas))
        entry.bind("<FocusOut>", lambda e: self.clear_entry(entry, idx, canvas))
        self.player_entries[idx] = entry

        # Clear previous error message if present
        if self.error_labels[idx]:
            self.error_labels[idx].destroy()

    def save_player_name(self, entry, idx, canvas):
        player_name = entry.get().strip()

        # Check if the entered name is already in use by another player
        if player_name in self.gui.input_handler.get_all_player_names():
            self.show_error(canvas, idx, "* Name cannot be the same as another player.")
            return

        # Check if the previous player name has been entered (except for the first player)
        if idx > 0 and not self.gui.input_handler.players_names[idx - 1]:  # Corrected line
            self.show_error(canvas, idx, "* Previous player name must be entered first.")
            return

        # Validate and store the name if it's not empty and under the character limit
        if self.gui.input_handler.validate_and_store_name(idx, player_name):
            print(f"Player {idx + 1} name saved: {player_name}")  # Debug info, delete later
            entry.destroy()
            self.player_entries[idx] = None  # Clear reference

            # Clear previous text if it exists
            if self.player_text_refs[idx]:
                canvas.delete(self.player_text_refs[idx])  # Remove previous text

            # Display the new name within the text box
            self.player_text_refs[idx] = canvas.create_text(
                348, 290 + idx * 100, text=player_name, font=("Comic Sans MS", 20), fill="#000000"
            )
        else:
            # Show error if name is invalid (too short or too long)
            self.show_error(canvas, idx, "* Name must be 1-20 characters.")

    def show_error(self, canvas, idx, message):
        """Display an error message below the entry box."""
        x_position = 325
        y_position = 322 + idx * 100  # Below each player box
        if self.error_labels[idx]:
            self.error_labels[idx].destroy()

        self.error_labels[idx] = tk.Label(
            canvas,
            text=message,
            font=("Comic Sans MS", 16),  # Adjust font size here
            fg="red",
            bg="#FBF8F5"
        )
        self.error_labels[idx].place(x=x_position, y=y_position)

    def clear_entry(self, entry, idx, canvas):
        entry.destroy()
        self.player_entries[idx] = None
        canvas.itemconfig(self.player_box_images_refs[idx],
                          image=self.player_box_images[idx])  # Reset to original box image

    def start_game(self, input_handler):
        # Start the game with the processed player names
        player_names = input_handler.get_all_player_names()
        print("Starting game with players:", player_names)