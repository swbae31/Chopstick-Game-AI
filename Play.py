from src.Game_Engine.Game import Game
from src.Game_Engine.HumanPlayer import HumanPlayer
from src.AI_Player.RandomPlayer import RandomPlayer
from collections import defaultdict


def play_game():
    p1 = HumanPlayer("p1")
    p2 = RandomPlayer("p2")
    players = [p1, p2]
    game = Game(players, verbose=True)
    game.load([3,3,3,3])
    game.play()


if __name__ == "__main__":
    play_game()