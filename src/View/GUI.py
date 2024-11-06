# main.py
import tkinter as tk
import os
from src.View.DisplayManager import DisplayManager
from src.Controller.InputHandler import InputHandler

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        imgpath = os.path.join(os.path.dirname(__file__), "../../assets/startup_frame/startup_frame_background.png")

        self.background_image = tk.PhotoImage(file=imgpath)
        self.image_width = self.background_image.width()
        self.image_height = self.background_image.height()

        # Set window size and center it
        self.geometry(f"{self.image_width}x{self.image_height}+"
                      f"{int((self.winfo_screenwidth() - self.image_width) / 2)}+"
                      f"{int((self.winfo_screenheight() - self.image_height) / 2)}")

        self.resizable(False, False)  # Disable resizing
        self.configure(bg="#FFFFFF")
        self.title("Monopoly Hong Kong Special Edition")

        self.frames = {}  # Store different pages (frames)

        # Initialize InputHandler
        self.display_manager = DisplayManager(self)
        self.input_handler = InputHandler()

        # Initialize DisplayManager
        self.display_manager = DisplayManager(self)

        # Set up frames
        self.main_menu()
        self.new_game_page()
        self.load_game_page()
        self.load_info_page()

        # Initially show the main menu
        self.show_frame("MainMenu")

    # Show the main menu
    def main_menu(self):
        frame = tk.Frame(self)
        self.frames["MainMenu"] = frame
        self.canvas = self.display_manager.setup_main_menu(frame)

    # Load the previous game record
    def load_game_page(self):
        frame = tk.Frame(self)
        self.frames["LoadPage"] = frame
        label = tk.Label(frame, text="This is the Load Game Page")
        label.pack(pady=20)
        back_button = tk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("MainMenu"))
        back_button.pack(pady=10)

    # Start a new game
    def new_game_page(self):
        frame = tk.Frame(self)
        self.frames["NewGamePage"] = frame
        self.new_game_canvas = self.display_manager.setup_new_game_page(frame, self.input_handler)

    # Show the game information
    def load_info_page(self):
        frame = tk.Frame(self)
        self.frames["InfoPage"] = frame
        self.info_canvas = self.display_manager.setup_info_page(frame)

    # Enter the main game board
    def enter_game(self):
        frame = tk.Frame(self)
        self.frames["GameBoard"] = frame
        self.game_canvas = self.display_manager.setup_game_board(frame)

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[frame_name].place(x=0, y=0, width=self.image_width, height=self.image_height)


# Run the GUI
gui = GUI()
gui.mainloop()