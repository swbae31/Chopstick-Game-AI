from src.Game_Engine.Player import Player
from src.Game_Engine.Game import Game
from random import choice, uniform
from collections import defaultdict

class QLearningPlayer(Player):
    """
    Q Learning Player Class
    Trains using Q learning with 1 look ahead
    """

    # Centralized q function shared by agents
    # Key: (state tuple, action)
    # Value: Estimated q value
    q_value = None
    # Exploration Epsilon for training
    exploration_epsilon = None

    def __init__(self, name, training_mode = False):
        # hands[0] is left hand, hands[1] is right hand
        Player.__init__(self, name)
        self.training_mode = training_mode
        self.last_state = None
        self.last_action = None        

    def train(self):
        """
        Train the Q function by simulating games with itself
        After learning is done, use greedy policy using the q function to make decisions
        """

        # Don't train if already trained
        if QLearningPlayer.q_value:
            return
        # Don't recursively train if already in training mode
        if self.training_mode:
            return

        # 0) Init training vars
        # Init default q value to be 0
        QLearningPlayer.q_value = defaultdict(int)
        episodes = 10000
        learning_rate = 0.1
        discount_factor = 0.9
        QLearningPlayer.exploration_epsilon = 0.1

        # 1) Initialize game
        p1 = QLearningPlayer("q1", training_mode=True)
        p2 = QLearningPlayer("q2", training_mode=True)
        players = [p1, p2]
        game = Game(players, verbose=False)

        # Train for episodes
        for _ in range(episodes):
            game.reset()
            
            # Loop until episode ends
            while game.determine_game_ended() == False:
                current_player = game.get_current_player()
                game.process_turn()
                s1 = current_player.last_state
                a1 = current_player.last_action
                s2 = game.get_game_state()

                reward = 0
                if game.determine_game_ended():
                    if current_player == game.winner:
                        reward = 1
                    # The other player won, not a tie
                    elif game.winner != None:
                        reward = -1
                # Negative value since zero sum game.
                next_state_q_value = self.__policy(s2)[1] * -1
                QLearningPlayer.q_value[(s1, a1)] = QLearningPlayer.q_value[(s1, a1)] + learning_rate *(reward + discount_factor * next_state_q_value - QLearningPlayer.q_value[(s1, a1)])
        
    def __policy(self, state):
        """
        Given a state, return the greedy action by the q function
        """
        # Greedy policy using value function
        available_actions = self.game.get_current_available_actions()
        best_action = None
        best_value = float('-inf')
        for action in available_actions:
            cur_value = QLearningPlayer.q_value[(state, action)]
            if cur_value > best_value:
                best_action = action
                best_value = cur_value

        return best_action, best_value

    def __training_policy(self, state):
        """
        Epsilon greedy training policy
        """
        # Explore
        if uniform(0, 1) < self.exploration_epsilon:
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
        action = None
        state = self.game.get_game_state()
        # Greedy Policy
        if self.training_mode == False:
            action, _ = self.__policy(state)
        # Epsilon Greedy policy for training
        else:
            action = self.__training_policy(state)
            # Save last state and action for training
            self.last_state = state
            self.last_action = action

        self.perform_action_string(action)









