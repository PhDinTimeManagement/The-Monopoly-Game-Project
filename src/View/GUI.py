import tkinter as tk
from PIL import Image, ImageTk


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set the window size to 3/4 of the screen
        self.screen_width, self.screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.window_width, self.window_height = int(self.screen_width * 0.75), int(self.screen_height * 0.75)

        # Position the window to be centered on the screen
        self.geometry(
            f"{self.window_width}x{self.window_height}+"
            f"{int((self.screen_width - self.window_width) / 2)}+"
            f"{int((self.screen_height - self.window_height) / 2)}")

        # Disable window resizing
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        self.title("Monopoly Hong Kong Special Edition")

        self.frames = {}  # Store different pages (frames)

        # Load main menu
        self.main_menu()

    def main_menu(self):
        frame = tk.Frame(self)
        self.frames["MainMenu"] = frame
        frame.place(x=0, y=0, width=self.window_width, height=self.window_height)

        # Load and resize the background image to fill the window size
        imgpath = "../../assets/startup_frames/startup_frame_background_image.png"
        bg_img = Image.open(imgpath)
        bg_img = bg_img.resize((self.window_width, self.window_height), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(bg_img)

        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.window_height, width=self.window_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        # Load button images
        new_game_image = ImageTk.PhotoImage(Image.open(r"../../assets/startup_frames/new_game_button.png"))
        load_game_image = ImageTk.PhotoImage(Image.open(r"../../assets/startup_frames/load_game_button.png"))
        exit_image = ImageTk.PhotoImage(Image.open(r"../../assets/startup_frames/exit_button.png"))
        info_image = ImageTk.PhotoImage(Image.open(r"../../assets/startup_frames/info_button.png"))

        # Place buttons centered vertically and horizontally
        button_y_positions = [self.window_height * 0.55, self.window_height * 0.70, self.window_height * 0.85]

        new_game = canvas.create_image(self.window_width // 2, button_y_positions[0], image=new_game_image)
        canvas.tag_bind(new_game, "<Button-1>", lambda e: self.show_frame("GamePage"))

        load_game = canvas.create_image(self.window_width // 2, button_y_positions[1], image=load_game_image)
        canvas.tag_bind(load_game, "<Button-1>", lambda e: self.show_frame("LoadPage"))

        exit_button = canvas.create_image(self.window_width // 2, button_y_positions[2], image=exit_image)
        canvas.tag_bind(exit_button, "<Button-1>", lambda e: self.quit())

        # Place the info button at the top-right corner
        info_button = canvas.create_image(self.window_width - 85, 75, image=info_image)
        canvas.tag_bind(info_button, "<Button-1>", lambda e: self.show_frame("InfoPage"))

        # Keep references to button images to prevent garbage collection
        self.new_game_image = new_game_image
        self.load_game_image = load_game_image
        self.exit_image = exit_image
        self.info_image = info_image

        # Load other pages
        self.load_game_page()
        self.load_info_page()

    def load_game_page(self):
        frame = tk.Frame(self)
        self.frames["GamePage"] = frame
        label = tk.Label(frame, text="This is the Game Page")
        label.pack(pady=20)
        back_button = tk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("MainMenu"))
        back_button.pack(pady=10)

    def load_info_page(self):
        frame = tk.Frame(self)
        self.frames["InfoPage"] = frame
        label = tk.Label(frame, text="This is the Info Page")
        label.pack(pady=20)
        back_button = tk.Button(frame, text="Back to Main Menu", command=lambda: self.show_frame("MainMenu"))
        back_button.pack(pady=10)

    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.place_forget()
        # Show the specified frame
        self.frames[frame_name].place(x=0, y=0, width=self.window_width, height=self.window_height)


# Run the GUI
gui = GUI()
gui.mainloop()