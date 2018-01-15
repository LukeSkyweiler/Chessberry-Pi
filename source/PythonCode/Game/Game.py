from BoardAPI.Board import Board
from BoardAPI.Animation import Animation


class Game:
    def __init__(self, players):
        self.players = players

        self.game_board = Board()

        self.opening_animation = Animation("O")
        self.game_over_animation = Animation("E")

    def __init_board(self):
        self.opening_animation.play_animation()

        self.game_board.initialize()

    def __game_over(self):
        self.game_over_animation.play_animation()

    def play(self):
        self.__init_board()

        while not self.game_board.game_over():

            for player in self.players:
                player.get_move(self.game_board)

        self.__game_over()
