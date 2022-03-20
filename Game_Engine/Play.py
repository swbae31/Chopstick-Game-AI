from Game import Game
from HumanPlayer import HumanPlayer


def play_game():
    p1 = HumanPlayer("p1")
    p2 = HumanPlayer("p2")
    players = [p1, p2]
    game = Game(players)

    for player in players:
        player.game = game

    game.play()


if __name__ == "__main__":
    play_game()