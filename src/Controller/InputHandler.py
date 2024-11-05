# InputHandler.py
class InputHandler:
    def __init__(self):
        self.players_names = [None] * 6  # Support up to 6 players

    def set_num_players(self, num_players):
        self.players_names = [None] * num_players

    def validate_and_store_name(self, idx, player_name):
        if 0 <= idx < len(self.players_names):
            if player_name and len(player_name) <= 20:
                self.players_names[idx] = player_name
                return True  # Name is valid
            else:
                return False  # Name is invalid

    def get_all_player_names(self):
        return [name for name in self.players_names if name]

    @staticmethod
    # Player can roll the dice to generate a random name
    def generate_name():
        import random
        import string
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        return name
