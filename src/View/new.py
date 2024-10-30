import tkinter as tk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.screen_width, self.screen_height = self.winfo_screenwidth(),self.winfo_screenheight()
        print(self.screen_width, self.screen_height)
    def main_menu(self):
        pass
    
gui=GUI()
gui.mainloop()