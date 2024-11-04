from unittest import TestCase
from src.Controller.GameController import *
from src.Model.Gameboard import *

class TestGameController(TestCase):
    def test_save_game(self):
        GameController.save_game()

    def test_load_game(self):
        self.fail()
