from src.Game_Engine.Game import Game
from src.Game_Engine.HumanPlayer import HumanPlayer
from src.AI_Player.DpPlayer import DpPlayer
from src.AI_Player.RandomPlayer import RandomPlayer
from collections import defaultdict

def play_game():
    p1 = DpPlayer("DP")
    p2 = RandomPlayer("Random")
    players = [p1, p2]
    game = Game(players, verbose=False)

    wins = {}
    wins[p1.name] = 0
    wins[p2.name] = 0

    turns = defaultdict(int)

    for i in range(100):
        winner = game.play()
        wins[winner] += 1
        turns[game.turn_count] += 1
        game.reset()

    print(wins)
    print(turns)


if __name__ == "__main__":
    play_game()