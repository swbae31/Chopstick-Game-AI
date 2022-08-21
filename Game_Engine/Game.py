import Player


class Game:

    def __init__(self, players):
        self.players = players
        for player in players:
            player.game = self
        self.turn_count = 0
        self.game_ended = False
        self.winner: Player = None

    def play(self):
        """
        Starts Game
        :return: None
        """
        self.print_board()
        while not self.game_ended:
            self.process_turn()
            if self.determine_game_ended():
                self.game_ended = True
                break
        print(f"Game ended! Winner of the game is {self.winner.name}!")

    def process_turn(self):
        """
        Process a turn. Receive input from human players.
        :return: True if game ended, False if game did not end
        """
        self.turn_count += 1
        for player in self.players:
            print(f"{player.name}'s turn:")
            if not player.lost:
                player.play_turn()
                self.print_board()

    def print_board(self):
        """
        Prints Board
        :return: None
        """
        print(f"Turn: {self.turn_count}\n")
        for player in self.players:
            print(f"Player {player.name}")
            print(f"Alive: {not player.lost}, Hands: {player.hands}\n")

    def determine_game_ended(self):
        """
        Determines if game has ended, set winner if game has ended
        :return: True if game ended, False if not
        """
        alive_players = []
        for player in self.players:
            if not player.lost:
                alive_players.append(player)
        if len(alive_players) == 1:
            self.winner = alive_players[0]
            return True
        return False
