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
    # Total of 577 non-terminal states
    model = {}
    # Key: (state tuple, action)
    # Value: Iterated value using DP
    # Total 2560 state-action pairs
    # Converges to optimal solution in 20 iterations
    q_value = {}

    def __init__(self, name):
        Player.__init__(self, name)

    def train(self):
        """
        1) Builds model from game engine if not loaded
        2) Builds q function using bellmen optimallity equation if not loaded
        3) Follows a greedy policy to maximize value using q function
        """
        if not DpPlayer.model or not DpPlayer.q_value:
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
        # Build the model. Assume only 2 hands with 5 fingers each
        p1 = DpPlayer("dp1")
        p2 = DpPlayer("dp2")
        players = [p1, p2]
        training_game = Game(players, verbose=False)

        for i in range(5):
            for j in range(5):
                for k in range(5):
                    for l in range(5):
                        self.__build_model_for_state(training_game, (i, j, k, l))

    def __build_model_for_state(self, game, state):
        game.load(state)
        # Don't add to model if it is terminal state
        if game.determine_game_ended():
            return
        actions = game.get_current_available_actions()
        DpPlayer.model[state] = []
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
                # The other player won, not a tie
                elif game.winner:
                    reward = -1
            DpPlayer.model[state].append((action, next_state, reward))

    def __value_iteration(self):
        """
        State-action value function.
        Uses DP to store results in self.q.memo
        """
        # Initialize q_value to 0
        for state in DpPlayer.model.keys():
            for action, _, _ in DpPlayer.model[state]:
                DpPlayer.q_value[(state, action)] = 0

        # Perform Value Iteration, One-Step look ahead iteration
        epsilon = 0.001
        
        # sqrt since applied twice for the other agent turn, actual will be the number in sqrt
        discount_factor = math.sqrt(0.9)
        # Iterate until epsilon
        for iteration in range(1, 101):
            max_delta = 0
            # For all states
            for state in DpPlayer.model.keys():
                # Look ahead once to update value
                for action, next_state, reward in DpPlayer.model[state]:
                    # non-terminal state
                    if reward == 0:
                        # Negative, since the value will be of the opponent
                        cur_value = -self.__policy(next_state)[1] * discount_factor
                    # Terminal state
                    else:
                        cur_value = reward
                    max_delta = max(max_delta, abs(DpPlayer.q_value[(state, action)] - cur_value))
                    DpPlayer.q_value[(state, action)] = cur_value
            
            if max_delta < epsilon:
                break

    def __policy(self, state):
        """
        Given a state, return an action and its value according to the current policy
        """
        # Greedy policy using value function estimated by value iteration
        best_action = None
        best_value = float('-inf')
        for action, _, _ in DpPlayer.model[state]:
            cur_value = DpPlayer.q_value[(state, action)]
            if cur_value > best_value:
                best_action = action
                best_value = cur_value

        return best_action, best_value

        









