HIT_ACTION = "HIT"
SPLIT_ACTION = "SPLIT"
TIE_RESULT = "TIE"


class Game:

    def __init__(self, players, verbose=True):
        self.is_verbose = verbose
        self.players = players
        self.turn_count = 1
        self.winner = None
        # Round robins all players for turns
        self.current_player_index = 0
        for player in players:
            player.game = self
            player.train()

    def reset(self):
        for player in self.players:
            player.reset()
        self.turn_count = 1
        self.winner = None
        self.current_player_index = 0

    def switch_player_order(self):
        self.players = self.players[::-1]

    def load(self, game_state, turn_count=0):
        """
        Loads the game with the game_state and turn count
        """
        self.reset()
        self.turn_count = turn_count
        index = 0
        for player in self.players:
            player.load([game_state[index], game_state[index+1]])
            index += len(player.hands)

    def play(self):
        """
        Starts Game
        :return: Winner player name, None if tie
        """
        self.print_board()
        while not self.determine_game_ended():
            self.process_turn()

        if self.winner:
            winner_name = self.winner.name
        else:
            winner_name = TIE_RESULT

        self.verbose_print(f"Game ended! Winner of the game is {winner_name}!")

        return winner_name

    def process_turn(self):
        """
        Process a turn. Receive input from human players.
        """
        current_player = self.get_current_player()
        self.verbose_print(f"{current_player.name}'s turn:")
        current_player.play_turn()
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.turn_count += 1
        self.print_board()

    def print_board(self):
        """
        Prints Board
        :return: None
        """
        self.verbose_print(f"Turn: {self.turn_count}\n")
        for player in self.players:
            self.verbose_print(f"Player {player.name} {type(player).__name__}")
            self.verbose_print(f"Alive: {not player.lost}, Hands: {player.hands}\n")

    def determine_game_ended(self):
        """
        Determines if game has ended, set winner if game has ended
        :return: True if game ended, False if not
        """
        alive_players = [player for player in self.players if player.lost is False]
        if len(alive_players) == 1:
            self.winner = alive_players[0]
            return True
        # If turn count is 200, consider it a tie
        if self.turn_count >= 200:
            self.winner == None
            return True
        return False

    def get_game_state(self):
        """
        Return game state as tuple. (CurrentPlayer hand 1, Current player hand 2, other player hand 1, other player hand 2)
        example: (1, 1, 1, 1) at start of game
        """
        game_state = []
        current_player = self.get_current_player()
        game_state.extend(current_player.hands)

        for player in self.players:
            if player == current_player:
                continue
            game_state.extend(player.hands)
        return tuple(game_state)

    def get_current_available_actions(self):
        """
        Return list of all available action from current state.
        """
        actions = []
        current_player = self.get_current_player()
        # Valid hit src hand with more than 0 fingers
        hit_src = [i for i in range(len(current_player.hands)) if current_player.hands[i] != 0]
        # Hit actions
        for player in self.players:
            if player == current_player:
                continue
            for hit_hand_index in hit_src:
                for j, hit_dst in enumerate(player.hands):
                    if hit_dst == 0:
                        continue
                    actions.append(f"{HIT_ACTION}_{hit_hand_index}{j}")

        # Split actions
        finger_sum = sum(current_player.hands)
        for i in range(finger_sum + 1):
            left = i
            right = finger_sum - i
            # Invalid split with more than 5 fingers
            if left >= 5 or right >= 5:
                continue
            # Invalid split with same hand state (no switching allowed)
            if [left, right] == current_player.hands or [right, left] == current_player.hands:
                continue
            actions.append(f"{SPLIT_ACTION}_{left}{right}")

        return actions

    def get_current_player(self):
        return self.players[self.current_player_index]

    def verbose_print(self, string):
        if self.is_verbose:
            print(string)
