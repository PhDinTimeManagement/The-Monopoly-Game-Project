from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../assets/game_starter")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_button_1_click(event):
    print("Button 1 clicked")

def on_button_2_click(event):
    print("Button 2 clicked")

window = Tk()
window.geometry("900x600")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=600,
    width=900,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Background image
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(
    450.0,
    300.0,
    image=image_image_1
)

# Button 1 as an image on Canvas
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = canvas.create_image(
    450.0, 300.0,
    image=button_image_1
)
# Bind the button click event
canvas.tag_bind(button_1, "<Button-1>", on_button_1_click)

# Button 2 as an image on Canvas
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = canvas.create_image(
    450.0, 480.0,
    image=button_image_2
)
# Bind the button click event
canvas.tag_bind(button_2, "<Button-1>", on_button_2_click)

window.resizable(False, False)
window.mainloop()