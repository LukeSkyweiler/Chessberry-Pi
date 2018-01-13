import BoardAPI.IOHandler as IOHandler


class Move:
    def playAnimation(self):
        pass


class ValidMove(Move):
    def playAnimation(self):
        pass


class InvalidMove(Move):
    def playAnimation(self):
        pass


class MoveException(Exception):
    pass