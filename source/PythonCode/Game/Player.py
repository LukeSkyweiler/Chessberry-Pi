

class Player:
    def get_move(self, board):
        pass


class Human(Player):
    def get_move(self, board):
        board.update_board()


class Computer(Player):
    def get_move(self, board):
        pass