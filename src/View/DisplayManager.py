# display.py
import tkinter as tk

class DisplayManager:
    def __init__(self, gui):
        self.gui = gui  # Reference to the main GUI instance

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
        # Replace the player box image with the demo image
        canvas.itemconfig(self.player_box_images_refs[idx], image=self.player_insert_demo_image)

        # If an entry already exists, remove it
        if self.player_entries[idx]:
            self.player_entries[idx].destroy()

        # Create a transparent entry field
        # Set the bg to E5E8E8 for "transparent" entry box
        entry = tk.Entry(canvas, font=("Arial", 20), width=20, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0,
                         justify="left")

        # Position entry based on the specific x_position and y_position passed
        entry.place(x=x_position + 22, y=y_position + 18)  # Adjust as needed within the image

        entry.focus_set()  # Focus the entry field for immediate typing

        # Bind focus out to save input and remove entry box
        entry.bind("<FocusOut>", lambda e: self.save_player_name(entry, idx, canvas))
        self.player_entries[idx] = entry  # Store the entry widget reference

    def save_player_name(self, entry, idx, canvas):
        # Get the player's name from the entry field
        player_name = entry.get().strip()

        # Store the name as needed (e.g., send to input handler or print it for now)
        print(f"Player {idx + 1} name: {player_name}")  # Placeholder; replace with actual handling

        # Destroy the entry widget and reset to original player box image if empty
        entry.destroy()
        self.player_entries[idx] = None  # Clear the entry reference

        # Optionally, reset the image if no name is entered, or keep the demo image if a name is set
        if not player_name:
            canvas.itemconfig(self.player_box_images_refs[idx], image=self.player_box_images[idx])

    def start_game(self, input_handler):
        # Start the game with the processed player names
        player_names = input_handler.get_all_player_names()
        print("Starting game with players:", player_names)