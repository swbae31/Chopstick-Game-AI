from src.Game_Engine.Player import Player
from random import choice


class DpPlayer(Player):
    """
    AI DP Player Class
    Builds a complete model of the environment using the Game Engine
    Then does a full search with memo (DP) to build optimal value (action state) & policy functions
    """

    def __init__(self, name):
        # hands[0] is left hand, hands[1] is right hand
        Player.__init__(self, name)
        self.model = None
        self.q = None

    def play_turn(self):
        """
        1) Builds model from game engine if not loaded
        2) Builds q function using bellmen optimallity equation if not loaded
        3) Follows a greedy policy to maximize value using q function
        """
        available_actions = self.game.get_current_available_actions()
        random_action = choice(available_actions)
        self.perform_action_string(random_action)

    def __build_model(self):
        """
        Builds a model (python dictionary)
        Model's Input: Game State
        Output: List of available (action, next state, reward)
        """
        pass

    def __build_q_function(self):
        """
        Build a value function (python dictionary)
        Input: Game State, Action
        Output: Value
        """
        pass