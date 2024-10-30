import tkinter as tk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.screen_width, self.screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.configure(bg="#FFFFFF")
        self.title("Monopoly Hong Kong")

        self.frames = {}  # 儲存不同的頁面（Frame）
        
        # 加載主菜單
        self.main_menu()
        
        print("screen size:", self.screen_width, self.screen_height)

    def main_menu(self):
        frame = tk.Frame(self)
        self.frames["MainMenu"] = frame
        frame.place(x=0, y=0, width=self.screen_width, height=self.screen_height)

        imgpath = r"assets\startup_frames\startup_frame_background_image.png"
        self.img = tk.PhotoImage(file=imgpath)
        zoom_level = 8
        self.img = self.img.zoom(zoom_level)
        self.img = self.img.subsample(max(self.img.width() // self.screen_width, self.img.height() // self.screen_height) + 1)

        canvas = tk.Canvas(frame, bg="#FFFFFF", height=self.screen_height, width=self.screen_width, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        new_game_image = tk.PhotoImage(file=r"assets\startup_frames\new_game_button.png")
        load_game_image = tk.PhotoImage(file=r"assets\startup_frames\load_game_button.png")
        exit_image = tk.PhotoImage(file=r"assets\startup_frames\exit_button.png")
        info_image = tk.PhotoImage(file=r"assets\startup_frames\info_button.png")

        canvas.create_image(self.screen_width // 2, self.screen_height // 2, image=self.img)
        
        new_game = canvas.create_image(self.screen_width // 2, self.screen_height // 4, image=new_game_image)
        canvas.tag_bind(new_game, "<Button-1>", lambda e: self.show_frame("GamePage"))

        load_game = canvas.create_image(self.screen_width // 2, self.screen_height * 2 // 4, image=load_game_image)
        canvas.tag_bind(load_game, "<Button-1>", lambda e: self.show_frame("LoadPage"))

        exit_button = canvas.create_image(self.screen_width // 2, self.screen_height * 3 // 4, image=exit_image)
        canvas.tag_bind(exit_button, "<Button-1>", lambda e: self.quit())

        info_button = canvas.create_image(self.screen_width // 20, self.screen_height // 20, image=info_image)
        canvas.tag_bind(info_button, "<Button-1>", lambda e: self.show_frame("InfoPage"))

        self.new_game_image = new_game_image
        self.load_game_image = load_game_image
        self.exit_image = exit_image
        self.info_image = info_image

        # 加載其他頁面
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
        # 隱藏所有頁面
        for frame in self.frames.values():
            frame.place_forget()
        # 顯示指定的頁面
        self.frames[frame_name].place(x=0, y=0, width=self.screen_width, height=self.screen_height)

gui = GUI()
gui.mainloop()