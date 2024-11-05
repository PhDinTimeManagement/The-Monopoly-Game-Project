# display.py
import tkinter as tk

class DisplayManager:
    def __init__(self, gui):
        self.gui = gui  # Reference to the main GUI instance
        self.error_labels = [None] * 6  # To hold error messages for player names
        self.player_entries = []  # To hold player name entry widgets
        self.player_box_images_refs = []  # To hold player box image references
        self.player_text_refs = [None] * 6  # To store references to the text displayed in each player box
        self.clicked_boxes = [False] * 6  # Add a flag list to track clicked boxes


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

        # Calculate dimensions for each button to set clickable areas
        new_game_width, new_game_height = self.new_game_image.width(), self.new_game_image.height()
        load_game_width, load_game_height = self.load_game_image.width(), self.load_game_image.height()
        exit_width, exit_height = self.exit_image.width(), self.exit_image.height()
        info_width, info_height = self.info_image.width(), self.info_image.height()

        # "New Game" button and clickable area
        new_game_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[0],
                                              image=self.new_game_image)
        new_game_clickable_area = canvas.create_rectangle(
            (self.gui.image_width // 2) - (0.6 * new_game_width), button_y_positions[0] - (0.6 * new_game_height),
            (self.gui.image_width // 2) + (0.6 * new_game_width), button_y_positions[0] + (0.6 * new_game_height),
            outline="", fill=""
        )
        canvas.tag_bind(new_game_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("NewGamePage"))

        # "Load Game" button and clickable area
        load_game_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[1],
                                               image=self.load_game_image)
        load_game_clickable_area = canvas.create_rectangle(
            (self.gui.image_width // 2) - (0.6 * load_game_width), button_y_positions[1] - (0.6 * load_game_height),
            (self.gui.image_width // 2) + (0.6 * load_game_width), button_y_positions[1] + (0.6 * load_game_height),
            outline="", fill=""
        )
        canvas.tag_bind(load_game_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("LoadPage"))

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
        canvas.tag_bind(info_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("InfoPage"))

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

        # Bind the enlarged clickable area to the "MainMenu" frame switch
        canvas.tag_bind(back_button_clickable_area, "<Button-1>", lambda e: self.gui.show_frame("MainMenu"))

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
            # Get dimensions of the player box image
            image_width = player_box_image.width()
            image_height = player_box_image.height()

            # Display each player box image
            player_box = canvas.create_image(x_position, y_position, anchor="nw", image=player_box_image)
            self.player_box_images_refs.append(player_box)  # Store the image reference

            # Create a clickable rectangle that matches the image dimensions
            clickable_area = canvas.create_rectangle(
                x_position, y_position, x_position + 1.2 * image_width, y_position + 1.2 * image_height,
                outline="", fill=""
            )

            # Bind click event to the clickable area instead of just the image
            canvas.tag_bind(clickable_area, "<Button-1>",
                            lambda e, idx=i, x=x_position, y=y_position: self.show_insert_entry(canvas, idx, x, y))

            y_position += 100  # Adjust y-position for the next player box

        # Display Edit Board and Play buttons on the right side
        edit_board_button = canvas.create_image(self.gui.image_width - 450, 430, image=self.edit_board_button_image)
        play_button = canvas.create_image(self.gui.image_width - 450, 650, image=self.start_game_image)

        # Calculate the centered position of Edit Board button and Play button
        edit_board_x = self.gui.image_width - 450
        edit_board_y = 430
        play_button_x = self.gui.image_width - 450
        play_button_y = 650

        # Get image dimensions
        edit_board_width = self.edit_board_button_image.width()
        edit_board_height = self.edit_board_button_image.height()
        play_button_width = self.start_game_image.width()
        play_button_height = self.start_game_image.height()

        # Create clickable rectangles slightly larger than the images, centered on the image position
        edit_board_clickable_area = canvas.create_rectangle(
            edit_board_x - (edit_board_width * 0.6),  # Left edge
            edit_board_y - (edit_board_height * 0.6),  # Top edge
            edit_board_x + (edit_board_width * 0.6),  # Right edge
            edit_board_y + (edit_board_height * 0.6),  # Bottom edge
            outline="", fill=""
        )

        play_button_clickable_area = canvas.create_rectangle(
            play_button_x - (play_button_width * 0.6),  # Left edge
            play_button_y - (play_button_height * 0.6),  # Top edge
            play_button_x + (play_button_width * 0.6),  # Right edge
            play_button_y + (play_button_height * 0.6),  # Bottom edge
            outline="", fill=""
        )

        # Bind actions for Edit Board and Play clickable areas
        canvas.tag_bind(edit_board_clickable_area, "<Button-1>",
                        lambda e: print("Edit board clicked"))  # Placeholder action
        canvas.tag_bind(play_button_clickable_area, "<Button-1>", lambda e: self.start_game(input_handler))

        return canvas

    def show_insert_entry(self, canvas, idx, x_position, y_position):
        # Always show player_insert_demo_image when a box is clicked
        if not self.clicked_boxes[idx]:
            canvas.itemconfig(self.player_box_images_refs[idx], image=self.player_insert_demo_image)
            self.clicked_boxes[idx] = True  # Mark this box as clicked

        # Retrieve the current name to display in the entry box if it exists
        previous_name = str(
            self.gui.input_handler.players_names[idx] if idx < len(self.gui.input_handler.players_names) else "")

        # If an entry already exists, remove it
        if self.player_entries[idx]:
            self.player_entries[idx].destroy()

        # Create an entry field for input with the existing name (if any)
        entry = tk.Entry(canvas, font=("Comic Sans MS", 20), width=20, bd=0, bg="#E5E8E8", fg="#000000",
                         highlightthickness=0, justify="left")
        if previous_name:  # Only insert if there's an existing name
            entry.insert(0, previous_name)  # Populate entry with existing name
        entry.place(x=x_position + 22, y=y_position + 16)
        entry.focus_set()

        # Define actions for Enter key and focus out
        def on_submit(event):
            new_name = entry.get().strip()
            if new_name != previous_name:
                self.save_player_name(entry, idx, canvas)  # Save only if the name changed
            else:
                self.clear_entry(entry, idx, canvas, revert_name=True)  # Keep the original name if unchanged

        entry.bind("<Return>", on_submit)
        entry.bind("<FocusOut>",
                   lambda e: on_submit(e) if entry.get().strip() != previous_name else self.clear_entry(entry, idx,
                                                                                                        canvas,
                                                                                                        revert_name=True))
        self.player_entries[idx] = entry

        # Clear any previous error message
        if self.error_labels[idx]:
            self.error_labels[idx].destroy()

    def clear_entry(self, entry, idx, canvas, revert_name=False):
        """Clear the entry field and revert to the previous name if `revert_name` is True."""
        entry.destroy()
        self.player_entries[idx] = None

        # If reverting and there's a previous name, keep it visible
        if revert_name and self.player_text_refs[idx]:
            # Do nothing, keep the text as it is
            pass
        else:
            canvas.itemconfig(self.player_box_images_refs[idx],
                              image=self.player_box_images[idx])  # Reset to original box image

    def save_player_name(self, entry, idx, canvas):
        player_name = entry.get().strip()

        # Check if the entered name is already in use by another player
        if player_name in self.gui.input_handler.get_all_player_names():
            self.show_error(canvas, idx, "* Name cannot be the same as another player.")
            return

        # Check if the previous player name has been entered (except for the first player)
        if idx > 0 and not self.gui.input_handler.players_names[idx - 1]:
            self.show_error(canvas, idx, "* Previous player name must be entered first.")
            return

        # Validate and store the name if it's under the character limit
        if len(player_name) <= 20 and self.gui.input_handler.validate_and_store_name(idx, player_name):
            # Clear any previous error message and reset the entry box if it had an error
            if self.error_labels[idx]:
                self.error_labels[idx].destroy()
                self.error_labels[idx] = None  # Reset the error label

            # Remove any existing text reference for the current player
            if self.player_text_refs[idx]:
                canvas.delete(self.player_text_refs[idx])
                self.player_text_refs[idx] = None

            # Store and display the valid player name
            print(f"Player {idx + 1} name saved: {player_name}")  # Debug info
            entry.delete(0, tk.END)  # Clear the entry to remove any leftover invalid text
            entry.insert(0, player_name)  # Ensure the valid name is displayed
            entry.destroy()  # Close the entry widget once saved

            # Display the name as static text on the canvas
            self.player_text_refs[idx] = canvas.create_text(
                348, 290 + idx * 100, text=player_name, font=("Comic Sans MS", 20), fill="#000000"
            )

        else:
            # Show error if name is invalid (too short or too long) and clear the entry
            self.show_error(canvas, idx, "* Name must be 1-20 characters.")
            entry.delete(0, tk.END)  # Clear the input to prompt re-entry

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