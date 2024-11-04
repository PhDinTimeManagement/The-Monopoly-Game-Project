# Responsible for capturing and processing user input
# Converting it into actions that the GameController can use to update the game state.

class InputHandler:
    def __init__(self):
        self.players_names = []

    def set_num_players(self, num_players):
        self.players_names = [None] * num_players

    def process_player_names(self, idx, player_name):
        if 0 <= idx < len(self.players_names) and player_name and len(player_name) < 20:
            self.players_names[idx] = player_name

    @staticmethod
    # Used for the start of the game, get user settings for this game
    def get_name_or_players(prompt):
        while True:
            user_input = input(prompt).strip()

            # Handle the number input
            if user_input.isdigit():
                user_input = int(user_input)
                if 2 <= user_input <= 6:
                    return user_input
                else:
                    message = "The number of players must be between 1 and 6."
                    return message
            # Handle as a string input
            else:
                if len(user_input) < 20:
                    return user_input
                else:
                    message = "The name should be less than 20 characters."
                    return message


    @staticmethod
    # Player can roll the dice to generate a random name
    def generate_name():
        import random
        import string
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        return name
