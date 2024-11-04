import tkinter as tk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Load background image and set the window size based on it
        imgpath = "../../assets/startup_frame/startup_frame_background.png"
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
        self.main_menu()

        # Initially show the main menu
        self.show_frame("MainMenu")

    def main_menu(self):
        frame = tk.Frame(self)
        self.frames["MainMenu"] = frame
        frame.place(x=0, y=0, width=self.image_width, height=self.image_height)

        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.image_height, width=self.image_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        # Define button images
        new_game_image = tk.PhotoImage(file="../../assets/startup_frame/new_game_button.png")
        load_game_image = tk.PhotoImage(file="../../assets/startup_frame/load_game_button.png")
        exit_image = tk.PhotoImage(file="../../assets/startup_frame/exit_button.png")
        info_image = tk.PhotoImage(file="../../assets/startup_frame/info_button.png")

        # Button positions
        button_y_positions = [self.image_height * 0.55, self.image_height * 0.70, self.image_height * 0.85]

        new_game = canvas.create_image(self.image_width // 2, button_y_positions[0], image=new_game_image)
        canvas.tag_bind(new_game, "<Button-1>", lambda e: self.show_frame("GamePage"))

        load_game = canvas.create_image(self.image_width // 2, button_y_positions[1], image=load_game_image)
        canvas.tag_bind(load_game, "<Button-1>", lambda e: self.show_frame("LoadPage"))

        exit_button = canvas.create_image(self.image_width // 2, button_y_positions[2], image=exit_image)
        canvas.tag_bind(exit_button, "<Button-1>", lambda e: self.quit())

        info_button = canvas.create_image(self.image_width - 85, 75, image=info_image)
        canvas.tag_bind(info_button, "<Button-1>", lambda e: self.show_frame("InfoPage"))

        # Keep references to button images
        self.new_game_image = new_game_image
        self.load_game_image = load_game_image
        self.exit_image = exit_image
        self.info_image = info_image

        # Store the canvas itself in the instance to maintain a reference to it
        self.canvas = canvas

        # Load other pages after setting up main menu
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
        frame.place(x=0, y=0, width=self.image_width, height=self.image_height)

        # Create a canvas to place the info frame and back button
        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.image_height, width=self.image_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Load the background image
        self.info_frame_background_image = tk.PhotoImage(file="../../assets/info_frame/info_frame_background.png")
        self.back_arrow_image = tk.PhotoImage(file="../../assets/info_frame/back_arrow.png")

        # Display the background image
        canvas.create_image(0, 0, anchor="nw", image=self.info_frame_background_image)

        # Display the back button as a button
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)
        canvas.tag_bind(back_button, "<Button-1>", lambda e: self.show_frame("MainMenu"))

        # Store the canvas itself in the instance to maintain a reference to it
        self.info_canvas = canvas

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[frame_name].place(x=0, y=0, width=self.image_width, height=self.image_height)


# Run the GUI
gui = GUI()
gui.mainloop()