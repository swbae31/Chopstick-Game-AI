from src.Game_Engine.Player import Player
from src.Game_Engine.Game import Game
from src.AI_Player.DpPlayer import DpPlayer
from src.AI_Player.RandomPlayer import RandomPlayer
from random import choice, uniform
from collections import defaultdict
import time
from tqdm import tqdm


class QLearningPlayer(Player):
    """
    Q Learning Player Class
    Trains using Q learning with 1 look ahead TD(0)
    """
    def __init__(self, name):
        # hands[0] is left hand, hands[1] is right hand
        Player.__init__(self, name)
        self.last_state = None
        self.last_action = None
        # Key: (state tuple, action)
        # Value: Estimated q value
        self.q_value = None
        self.exploration_epsilon = None
        # Training mode to enable epsilon greedy policy
        self.training_mode = False

    def train(self, epochs=5000, init_learning_rate=0.9, min_learning_rate=0.001, lr_decay=0.9995, discount_factor=0.9, init_epsilon=1.0, min_epsilon=0.01, epsilon_decay=0.999):
        """
        Train the Q function by simulating games with itself
        After learning is done, use greedy policy using the q function to make decisions.
        Stably coverges to the near optimal policy with the default hyperparameters. (About 48/52 against optimal dp agent)
        """
        print("Training q agent " + self.name + "... ")
        start = time.perf_counter()
        # 0) Init training vars
        # Init default q value to be 0
        self.q_value = defaultdict(int)
        self.training_mode = True
        main_game = self.game
        lr = init_learning_rate
        # 1) Initialize game
        p1 = self
        # Copy of self which shares the q value
        p2 = QLearningPlayer('self copy')
        p2.training_mode = True
        self.exploration_epsilon = p2.exploration_epsilon = init_epsilon
        p2.q_value = self.q_value
        players = [p1, p2]
        game = Game(players, verbose=False)
        average_turns = 0
        for _ in tqdm(range(epochs)):
            game.reset()
            
            # Loop until episode ends
            while not game.determine_game_ended():
                current_player = game.get_current_player()
                game.process_turn()
                s1 = current_player.last_state
                a1 = current_player.last_action
                s2 = game.get_game_state()

                reward = 0
                if game.determine_game_ended():
                    # Game ended, won game
                    reward = 100
                    # Terminal state q value is always 0
                    next_state_q_value = 0
                else:
                    # Negative value since zero sum game.
                    next_state_q_value = self.__policy(s2)[1] * -1

                self.q_value[(s1, a1)] = self.q_value[(s1, a1)] + lr * (reward + discount_factor * next_state_q_value - self.q_value[(s1, a1)])
            # Decay epsilon and learning rate
            p1.exploration_epsilon = p2.exploration_epsilon = max(p1.exploration_epsilon * epsilon_decay, min_epsilon)
            lr = max(lr * lr_decay, min_learning_rate)
            average_turns += game.turn_count
        # Set game back
        self.game = main_game
        # Perf
        print("Q Training took: " + str(time.perf_counter()-start) + " seconds")
        print("Average turn per episode " + str(average_turns/epochs))

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
        if not self.training_mode:
            action, _ = self.__policy(state)
        # Epsilon Greedy policy for training
        else:
            action = self.__training_policy(state)
            # Save last state and action for training
        self.last_state = state
        self.last_action = action

        self.perform_action_string(action)









