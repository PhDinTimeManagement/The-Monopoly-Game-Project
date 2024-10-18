# This model defines methods to get the user input and pass it to the model and view

class InputHandler:
    def __init__(self):
        pass

    # Used for the start of the game, get user settings for this game
    @staticmethod
    def get_name_or_players(self, prompt):
        while True:
            user_input = input(prompt).strip()

            # Handle the number input
            if user_input.isdigit():
                user_input = int(user_input)
                if 2 <= user_input <= 6:
                    return user_input
                else:
                    print("The number of players must be between 1 and 6.")
            # Handle as a string input
            else:
                if len(user_input) < 20:
                    return user_input
                else:
                    print("The name should be less than 20 characters.")

    @staticmethod
    # Player can roll the dice to generate a random name
    def generate_name(self):
        import random
        import string
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        return name




