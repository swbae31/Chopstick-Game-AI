from abc import ABC, abstractmethod
from src.Game_Engine.Game import HIT_ACTION, SPLIT_ACTION


class Player(ABC):
    """
    Base class for player
    """

    def __init__(self, name):
        # hands[0] is left hand, hands[1] is right hand
        self.hands = [1, 1]
        self.name = name
        self.lost = False
        self.game = None

    def pregame_prep(self):
        """
        Run any pregame preparation sequences.
        """
        pass

    @abstractmethod
    def play_turn(self):
        """

        :return: True if playable, False if game lost and no action to take
        """
        pass
    
    def reset(self):
        self.hands = [1, 1]
        self.lost = False

    def load(self, hands):
        self.hands = hands
        self.update_state()

    def hit(self, opponent, my_hand: int, opp_hand: int):
        """
        Action: hit another player's hand with my hand to add fingers
        :param opponent: player to hit
        :param my_hand: hand to hit with, 0 for left, 1 for right
        :param opp_hand: hand to hit, 0 for left, 1 for right
        :return: None
        """
        if self.hands[my_hand] == 0:
            raise Exception("Hand to hit with has 0 fingers!")
        if opponent.hands[opp_hand] == 0:
            raise Exception("Hand to hit has 0 fingers!")
        opponent.hands[opp_hand] += self.hands[my_hand]
        opponent.update_state()

    def split(self, hands):
        """
        Split my hand
        :param hands: the hand state to split
        :return: None
        :raises exception if input hand not valid
        """
        if len(hands) != len(self.hands):
            raise Exception("Number of hands don't match!")
        if sum(hands) != sum(self.hands):
            raise Exception("Sum of hand fingers don't match!")
        if hands[0] == self.hands[1] and hands[1] == self.hands[0]:
            raise Exception("Switching fingers not allowed!")
        if hands[0] == self.hands[0] and hands[1] == self.hands[1]:
            raise Exception("No change after splitting!")
        if hands[0] >= 5 or hands[1] >= 5:
            raise Exception("Cannot split to more than 5 fingers")

        self.hands = hands

    def update_state(self):
        """
        Update self player state after being hit
        :return:
        """
        for i in range(len(self.hands)):
            if self.hands[i] >= 5:
                self.hands[i] = 0

        # If all hand is 0, lost
        if sum(self.hands) == 0:
            self.lost = True

    def get_opponent(self):
        return [p for p in self.game.players if p != self][0]

    def perform_action_string(self, action_string):
        action_type, params = action_string.split('_')
        if action_type == HIT_ACTION:
            opponent = self.get_opponent()
            self.hit(opponent, int(params[0]), int(params[1]))
        elif action_type == SPLIT_ACTION:
            self.split([int(params[0]), int(params[1])])
