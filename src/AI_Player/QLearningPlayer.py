from src.Game_Engine.Player import Player
from src.Game_Engine.Game import Game
from random import choice, uniform


class QLearningPlayer(Player):
    """
    Q Learning Player Class
    Trains using Q learning with 1 look ahead
    """

    # Centralized q function shared by agents
    # Key: (state tuple, action)
    # Value: Estimated q value
    q_value = {}

    def __init__(self, name, training_mode = False):
        # hands[0] is left hand, hands[1] is right hand
        Player.__init__(self, name)
        self.training_mode = training_mode

    def pregame_prep(self):
        """
        Trains the q function if not available
        """
        if not self.q_value and not training_mode:
            self.train()

    def train(self):
        """
        Train the Q function by simulating games with itself
        After learning is done, use greedy policy using the q function to make decisions
        """

        # 1) Initialize game
        p1 = QLearningPlayer("q1", training_mode=True)
        p2 = QLearningPlayer("q2", training_mode=True)
        players = [p1, p2]
        game = Game(players, verbose=False)

        # Train for 10000 games
        for _ in range(10000):
            
            s1 = game.get_game_state()
            
        


    def __policy(self, state):
        """
        Given a state, return the greedy action by the q function
        """
        # Greedy policy using value function
        available_actions = self.game.get_current_available_actions()
        best_action = None
        best_value = float('-inf')
        for action in available_actions:
            cur_value = self.q_value[(state, action)]
            if cur_value > best_value:
                best_action = action
                best_value = cur_value

        return best_action, best_value

    def __training_policy(self, state):
        """
        Epsilon greedy training policy
        """
        exploration_epsilon = 0.1
        # Explore
        if uniform(0, 1) < exploration_epsilon:
            available_actions = self.game.get_current_available_actions()
            action = choice(available_actions)
        # Greedy
        else:
            action, _ = self.__policy(state)
        
        return action

    def play_turn(self):
        """
        Play using greedy policy using q function
        OR
        Epsilon Greedy for training
        """
        if self.training_mode == False:
            best_action, _ = self.__policy(self.game.get_game_state())
            self.perform_action_string(best_action)
        else:
            action = self.__training_policy(self.game.get_game_state())
            self.perform_action_string(action)










