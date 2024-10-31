from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage

# Set up paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../assets")

def relative_to_assets(path: str) -> Path:
    abs_path = ASSETS_PATH / Path(path)
    print(f"Trying to open asset at: {abs_path}")  # Debugging line
    return abs_path

# Define functions for button actions
def start_new_game():
    print("Starting a new game...")

def load_game():
    print("Loading game...")

def exit_game():
    print("Exiting game...")
    window.quit()

def show_info():
    global info_frame_displayed
    if not info_frame_displayed:
        canvas.itemconfig(info_frame_canvas_id, state="normal")
        canvas.itemconfig(back_arrow_canvas_id, state="normal")
        canvas.itemconfig(new_game, state="hidden")
        canvas.itemconfig(load_game, state="hidden")
        canvas.itemconfig(exit_button, state="hidden")
        canvas.itemconfig(info_button, state="hidden")
        info_frame_displayed = True
    else:
        hide_info_frame()

def hide_info_frame():
    global info_frame_displayed
    canvas.itemconfig(info_frame_canvas_id, state="hidden")
    canvas.itemconfig(back_arrow_canvas_id, state="hidden")
    canvas.itemconfig(new_game, state="normal")
    canvas.itemconfig(load_game, state="normal")
    canvas.itemconfig(exit_button, state="normal")
    canvas.itemconfig(info_button, state="normal")
    info_frame_displayed = False

# Initialize window
window = Tk()

window.geometry("1512x982")
#window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
window.configure(bg="#FFFFFF")
window.title("Monopoly Hong Kong Special Edition")

# Create canvas
canvas = Canvas(window, bg="#FFFFFF", height=982, width=1512, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# Load and place background image
background_image = PhotoImage(file=relative_to_assets("startup_frames/startup_frame_background_image.png"))
canvas.create_image(756, 491, image=background_image)

# Load images for buttons and bind them to respective functions
new_game_image = PhotoImage(file=relative_to_assets("startup_frames/new_game_button.png"))
load_game_image = PhotoImage(file=relative_to_assets("startup_frames/load_game_button.png"))
exit_image = PhotoImage(file=relative_to_assets("startup_frames/exit_button.png"))
info_image = PhotoImage(file=relative_to_assets("startup_frames/info_button.png"))

new_game = canvas.create_image(756, 550, image=new_game_image)
canvas.tag_bind(new_game, "<Button-1>", lambda e: start_new_game())

load_game = canvas.create_image(756, 690, image=load_game_image)
canvas.tag_bind(load_game, "<Button-1>", lambda e: load_game())

exit_button = canvas.create_image(756, 830, image=exit_image)
canvas.tag_bind(exit_button, "<Button-1>", lambda e: exit_game())

info_button = canvas.create_image(1410, 50, image=info_image)
canvas.tag_bind(info_button, "<Button-1>", lambda e: show_info())

# Load the info frame image (hidden by default)
info_frame_photo = PhotoImage(file=relative_to_assets("info_frame/info_frame.png"))
info_frame_canvas_id = canvas.create_image(756, 491, image=info_frame_photo, state="hidden")

# Load the back arrow image and place it in the top-left corner (hidden by default)
back_arrow_photo = PhotoImage(file=relative_to_assets("info_frame/back_arrow.png"))
back_arrow_canvas_id = canvas.create_image(60, 50, image=back_arrow_photo, state="hidden")
canvas.tag_bind(back_arrow_canvas_id, "<Button-1>", lambda e: hide_info_frame())

info_frame_displayed = False

window.resizable(False, False)
window.mainloop()