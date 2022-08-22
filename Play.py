from src.Game_Engine.Game import Game
from src.Game_Engine.HumanPlayer import HumanPlayer
from src.AI_Player.RandomPlayer import RandomPlayer
from collections import defaultdict


def play_game():
    p1 = RandomPlayer("p1")
    p2 = RandomPlayer("p2")
    players = [p1, p2]
    game = Game(players, verbose=False)
    win_count = defaultdict(int)
    game_turns = []
    for i in range(1000):
        winner = game.play()
        win_count[winner] += 1
        game_turns.append(game.turn_count)
        game.reset()
    print(win_count)
    print(sum(game_turns) / len(game_turns))


if __name__ == "__main__":
    play_game()