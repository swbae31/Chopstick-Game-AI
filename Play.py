from src.Game_Engine.Game import Game
from src.Game_Engine.HumanPlayer import HumanPlayer
from src.AI_Player.RandomPlayer import RandomPlayer


def play_game():
    p1 = HumanPlayer("p1")
    p2 = HumanPlayer("p2")
    players = [p1, p2]
    game = Game(players)

    game.play()


if __name__ == "__main__":
    play_game()