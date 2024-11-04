import tkinter as tk

class DisplayManager:
    def __init__(self, gui):
        self.gui = gui  # Reference to the main GUI instance

        # Load images once and store them in attributes
        self.startup_background = tk.PhotoImage(file="../../assets/startup_frame/startup_frame_background.png")
        self.new_game_image = tk.PhotoImage(file="../../assets/startup_frame/new_game_button.png")
        self.load_game_image = tk.PhotoImage(file="../../assets/startup_frame/load_game_button.png")
        self.exit_image = tk.PhotoImage(file="../../assets/startup_frame/exit_button.png")
        self.info_image = tk.PhotoImage(file="../../assets/startup_frame/info_button.png")
        self.info_frame_background = tk.PhotoImage(file="../../assets/info_frame/info_frame_background.png")
        self.back_arrow_image = tk.PhotoImage(file="../../assets/info_frame/back_arrow.png")

    def setup_main_menu(self, frame):
        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.gui.image_height, width=self.gui.image_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.startup_background)

        # Button positions
        button_y_positions = [self.gui.image_height * 0.55, self.gui.image_height * 0.70, self.gui.image_height * 0.85]

        new_game = canvas.create_image(self.gui.image_width // 2, button_y_positions[0], image=self.new_game_image)
        canvas.tag_bind(new_game, "<Button-1>", lambda e: self.gui.show_frame("GamePage"))

        load_game = canvas.create_image(self.gui.image_width // 2, button_y_positions[1], image=self.load_game_image)
        canvas.tag_bind(load_game, "<Button-1>", lambda e: self.gui.show_frame("LoadPage"))

        exit_button = canvas.create_image(self.gui.image_width // 2, button_y_positions[2], image=self.exit_image)
        canvas.tag_bind(exit_button, "<Button-1>", lambda e: self.gui.quit())

        info_button = canvas.create_image(self.gui.image_width - 85, 75, image=self.info_image)
        canvas.tag_bind(info_button, "<Button-1>", lambda e: self.gui.show_frame("InfoPage"))

        # Return canvas reference to maintain
        return canvas

    def setup_info_page(self, frame):
        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.gui.image_height, width=self.gui.image_width, bd=0,
                           highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.info_frame_background)

        # Display the back button as a button
        back_button = canvas.create_image(50, 50, image=self.back_arrow_image)
        canvas.tag_bind(back_button, "<Button-1>", lambda e: self.gui.show_frame("MainMenu"))

        return canvas