from Player import Player

HIT_ACTION = "HIT"
SPLIT_ACTION = "SPLIT"


class HumanPlayer(Player):
    """
    Human Player Class
    """

    def __init__(self, name):
        # hands[0] is left hand, hands[1] is right hand
        Player.__init__(self, name)

    def play_turn(self):
        """

        :return: True if playable, False if game lost and no action to take
        """
        # Loop until valid input
        while True:
            try:
                action = input("Select your action: HIT or SPLIT\n")
                action = action.upper()

                if action == HIT_ACTION:
                    # TODO: add opponent name for input for multiple players
                    my_hand, opp_hand = \
                        input("Enter hand to hit with (0 or 1) and hand to hit (0 or 1). Sample: 0, 1\n").split(",")
                    opponent = [p for p in self.game.players if p != self][0]
                    self.hit(opponent, int(my_hand), int(opp_hand))

                elif action == SPLIT_ACTION:
                    left, right = \
                        input("Fingers for left and right hand. Example: 2, 2\n").split(",")
                    self.split([int(left), int(right)])
                else:
                    raise Exception("Unknown action entered!")
                break
            except Exception as e:
                print(e)
