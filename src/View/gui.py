from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage

# Set up paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../assets/startup_frames")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Define functions for button actions
def start_new_game():
    print("Starting a new game...")
    # Add code here to initiate a new game or transition to another screen

def load_game():
    print("Loading game...")
    # Add code here to load game data or transition to a loading screen

def exit_game():
    print("Exiting game...")
    window.quit()  # Closes the application window

def show_info():
    # Show or hide the info frame image
    global info_frame_displayed
    if not info_frame_displayed:
        canvas.itemconfig(info_frame_canvas_id, state="normal")
        info_frame_displayed = True
    else:
        canvas.itemconfig(info_frame_canvas_id, state="hidden")
        info_frame_displayed = False

# Initialize window
window = Tk()
window.geometry("1512x982")
window.configure(bg="#FFFFFF")

# Create canvas
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=982,
    width=1512,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Load and place background image
background_image = PhotoImage(file=relative_to_assets("startup_frame_background_image.png"))
canvas.create_image(
    756, 491,  # Center the background image in the window
    image=background_image
)

# Load images for buttons
new_game_image = PhotoImage(file=relative_to_assets("new_game_button.png"))
load_game_image = PhotoImage(file=relative_to_assets("load_game_button.png"))
exit_image = PhotoImage(file=relative_to_assets("exit_button.png"))
info_image = PhotoImage(file=relative_to_assets("info_button.png"))

# Place button images on canvas and bind them to respective functions
new_game = canvas.create_image(756, 500, image=new_game_image)
canvas.tag_bind(new_game, "<Button-1>", lambda e: start_new_game())

load_game = canvas.create_image(756, 600, image=load_game_image)
canvas.tag_bind(load_game, "<Button-1>", lambda e: load_game())

exit_button = canvas.create_image(756, 700, image=exit_image)
canvas.tag_bind(exit_button, "<Button-1>", lambda e: exit_game())

info_button = canvas.create_image(1400, 50, image=info_image)
canvas.tag_bind(info_button, "<Button-1>", lambda e: show_info())

# Load the info frame image (hidden by default)
info_frame_photo = PhotoImage(file=relative_to_assets("../../assets/info_frame/info_frame.png"))
info_frame_canvas_id = canvas.create_image(
    756, 491,  # Center it on the canvas
    image=info_frame_photo,
    state="hidden"  # Hide initially
)

# Initialize state variable to track visibility of info frame
info_frame_displayed = False

window.resizable(False, False)
window.mainloop()