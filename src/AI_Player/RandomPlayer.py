from src.Game_Engine.Player import Player
from random import choice


class RandomPlayer(Player):
    """
    AI Random Player Class
    Plays random available action
    """

    def __init__(self, name):
        # hands[0] is left hand, hands[1] is right hand
        Player.__init__(self, name)

    def play_turn(self):
        """
        Picks random action
        """
        available_actions = self.game.get_current_available_actions()
        random_action = choice(available_actions)
        self.perform_action_string(random_action)
