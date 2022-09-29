from src.Game_Engine.Game import Game
from src.Game_Engine.HumanPlayer import HumanPlayer
from src.AI_Player.DpPlayer import DpPlayer
from src.AI_Player.RandomPlayer import RandomPlayer
from src.AI_Player.QLearningPlayer import QLearningPlayer
from collections import defaultdict


def play_game():
    p1 = QLearningPlayer("Q 5000")
    p2 = DpPlayer("DP")
    p1.train(epochs=5000)
    p2.train()
    players = [p1, p2]
    game = Game(players, verbose=False)

    wins = defaultdict(int)
    turns = defaultdict(int)

    play_count = 10000
    for i in range(play_count):
        winner = game.play()
        wins[winner] += 1
        turns[game.turn_count] += 1
        # Swap order to play fair game, going second has absolute advantage
        game.switch_player_order()

    print(wins)
    print(f"P1 Win rate: {wins[p1.name]/play_count*100}")
    print(sorted(turns.items()))


if __name__ == "__main__":
    play_game()
