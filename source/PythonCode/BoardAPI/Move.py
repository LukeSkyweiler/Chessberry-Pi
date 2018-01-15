import BoardAPI.IOHandler as IOHandler
import BoardAPI.Animation as Animation

class Move:
    def __init__(self, command):
        self.animation = Animation.Animation(command)

    def playAnimation(self):
        self.animation.play_animation()


class ValidMove(Move):
    def __init__(self):
        self.animation_command = "v"
        super().__init__(self.animation_command)


class InvalidMove(Move):
    def __init__(self):
        self.animation_command = "i"
        super().__init__(self.animation_command)


class MoveException(Exception):
    pass