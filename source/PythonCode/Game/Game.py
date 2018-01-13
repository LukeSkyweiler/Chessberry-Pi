from BoardAPI.Board import Board


class Game:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player

        self.game_board = Board()

    def play(self):
        pass
