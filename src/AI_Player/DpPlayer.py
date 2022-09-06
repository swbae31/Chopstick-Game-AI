from src.Game_Engine.Player import Player
from src.Game_Engine.Game import Game
import math

class DpPlayer(Player):
    """
    AI DP Player Class
    Builds a complete model of the environment using the Game Engine
    Then does a value iteration to find the estimated optimal policy
    """

    # Static class variables Model and QValue
    # Key: Non-terminal State tuple
    # Value: List of tuples (action, next state, reward of next state)
    # Total of 577 non-terminal states d
    model = {}
    # Key: (state tuple, action)
    # Value: Iterated value using DP
    # Total 2560 state-action pairs
    # Converges to optimal solution in 20 value iteration
    q_value = {}

    def __init__(self, name):
        Player.__init__(self, name)
        

    def pregame_prep(self):
        """
        1) Builds model from game engine if not loaded
        2) Builds q function using bellmen optimallity equation if not loaded
        3) Follows a greedy policy to maximize value using q function
        """
        if not self.model or not self.q_value:
            self.__build_model()
            self.__value_iteration()

    def play_turn(self):
        best_action, _ = self.__policy(self.game.get_game_state())
        self.perform_action_string(best_action)

    def __build_model(self):
        """
        Builds a model (python dictionary : self.model)
        Model's Input: Game State
        Output: List of available (action, next state, reward)
        """        
        # Assume that this will be called at begining of game
        # Build the model. Assume only 2 hands with 5 fingers each
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    for l in range(5):
                        self.__build_model_for_state((i, j, k, l))
        self.game.reset()

    def __build_model_for_state(self, state):
        game = self.game
        game.load(state)
        # Don't add to model if it is terminal state
        if game.determine_game_ended():
            return
        actions = game.get_current_available_actions()
        self.model[state] = []
        # Fix p1 to generate model
        p1 = game.players[0]
        for action in actions:
            game.load(state)
            p1.perform_action_string(action)
            game.current_player_index = (game.current_player_index + 1) % len(game.players)
            next_state = game.get_game_state()
            reward = 0
            if game.determine_game_ended():
                if p1 == game.winner:
                    reward = 1
                else:
                    reward = -1
            self.model[state].append((action, next_state, reward))

    def __value_iteration(self):
        """
        State-action value function.
        Uses DP to store results in self.q.memo
        """
        # Initialize q_value to 0
        for state in self.model.keys():
            for action, _, _ in self.model[state]:
                self.q_value[(state, action)] = 0

        # Perform Value Iteration, One-Step look ahead iteration
        epsilon = 0.001
        
        # sqrt since applied twice for the other agent turn, actual will be the number in sqrt
        discount_factor = math.sqrt(0.9)
        # Iterate until epsilon
        for iteration in range(1, 101):
            max_delta = 0
            # For all states
            for state in self.model.keys():
                # Look ahead once to update value
                for action, next_state, reward in self.model[state]:
                    # non-terminal state
                    if reward == 0:
                        # Negative, since the value will be of the opponent
                        cur_value = -self.__policy(next_state)[1] * discount_factor
                    # Terminal state
                    else:
                        cur_value = reward
                    max_delta = max(max_delta, abs(self.q_value[(state, action)] - cur_value))
                    self.q_value[(state, action)] = cur_value
            
            if max_delta < epsilon:
                break

    def __policy(self, state):
        """
        Given a state, return an action and its value according to the current policy
        """
        # Greedy policy using value function estimated by value iteration
        best_action = None
        best_value = float('-inf')
        for action, _, _ in self.model[state]:
            cur_value = self.q_value[(state, action)]
            if cur_value > best_value:
                best_action = action
                best_value = cur_value

        return best_action, best_value

        









