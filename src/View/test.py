class EditBoardFrame(GameplayFrame):
    def __init__(self, gui):
        super().__init__(gui)
        self.canvas = None
        self.current_tile_index = -1  # To track the selected tile for editing

        # Entry fields and dropdown for editing
        self.name_entry = None
        self.color_menu = None
        self.price_entry = None
        self.rent_entry = None
        self.color_var = tk.StringVar()  # To hold the selected color

        # Available colors for the dropdown
        self.available_colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "None"]

    def setup_edit_board_frame(self, frame):
        self.canvas = self.clear_widgets_create_canvas_set_background(frame, self.edit_board_background)

        # Display tile information (from GameplayFrame)
        self.display_tile_info(self.canvas)

        # Make tiles interactive for editing
        self.make_tiles_editable()

    def make_tiles_editable(self):
        # Bind click events to each tile's name, price, rent, or color for editing
        for i, tile in enumerate(GameplayFrame.tile_info):
            if tile[0] == "property":  # Only for properties
                self.canvas.tag_bind(tile[5], "<Button-1>", lambda e, idx=i: self.edit_tile(idx))  # Name
                self.canvas.tag_bind(tile[6], "<Button-1>", lambda e, idx=i: self.edit_tile(idx))  # Price
                self.canvas.tag_bind(tile[7], "<Button-1>", lambda e, idx=i: self.edit_tile(idx))  # Rent
                self.canvas.tag_bind(tile[8], "<Button-1>", lambda e, idx=i: self.edit_tile(idx))  # Owner (color)

    def edit_tile(self, tile_index):
        self.current_tile_index = tile_index
        self.remove_entries()  # Clear any previous entries

        # Get tile info for the selected tile
        tile = GameplayFrame.tile_info[tile_index]
        name, price, rent, color = tile[1], tile[2], tile[3], tile[4]

        # Place entry fields for editing
        self.name_entry = tk.Entry(self.canvas.master, font=("Comic Sans MS", 14))
        self.name_entry.insert(0, name)
        self.name_entry.place(x=self.__tile_info_coord[tile_index][0], y=self.__tile_info_coord[tile_index][1] - 20)

        self.color_var.set(color)  # Set current color in the dropdown
        self.color_menu = tk.OptionMenu(self.canvas.master, self.color_var, *self.available_colors)
        self.color_menu.place(x=self.__tile_info_coord[tile_index][6], y=self.__tile_info_coord[tile_index][7] - 20)

        self.price_entry = tk.Entry(self.canvas.master, font=("Comic Sans MS", 14))
        self.price_entry.insert(0, price)
        self.price_entry.place(x=self.__tile_info_coord[tile_index][2], y=self.__tile_info_coord[tile_index][3] - 20)

        self.rent_entry = tk.Entry(self.canvas.master, font=("Comic Sans MS", 14))
        self.rent_entry.insert(0, rent)
        self.rent_entry.place(x=self.__tile_info_coord[tile_index][4], y=self.__tile_info_coord[tile_index][5] - 20)

        # Add a button to confirm changes
        confirm_button = tk.Button(
            self.canvas.master, text="Save", font=("Comic Sans MS", 14), command=self.process_user_input
        )
        confirm_button.place(x=self.__tile_info_coord[tile_index][0], y=self.__tile_info_coord[tile_index][1] + 40)

    def remove_entries(self):
        # Remove previous editing fields
        if self.name_entry:
            self.name_entry.destroy()
            self.name_entry = None
        if self.color_menu:
            self.color_menu.destroy()
            self.color_menu = None
        if self.price_entry:
            self.price_entry.destroy()
            self.price_entry = None
        if self.rent_entry:
            self.rent_entry.destroy()
            self.rent_entry = None

    def process_user_input(self):
        if self.current_tile_index == -1:
            return  # No tile selected

        # Update tile info with new values
        GameplayFrame.tile_info[self.current_tile_index][1] = self.name_entry.get()
        GameplayFrame.tile_info[self.current_tile_index][2] = self.price_entry.get()
        GameplayFrame.tile_info[self.current_tile_index][3] = self.rent_entry.get()
        GameplayFrame.tile_info[self.current_tile_index][4] = self.color_var.get()

        # Remove entry fields
        self.remove_entries()

        # Refresh the tile display
        self.remove_game_board_text()  # Clear current tile info display
        self.display_tile_info(self.canvas)  # Redisplay updated info