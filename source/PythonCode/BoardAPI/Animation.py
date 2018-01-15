from BoardAPI.IOHandler import OutputHandler


class Animation:
    def __init__(self, command):
        self.command = command
        self.output = OutputHandler()

    def play_animation(self):
        self.output.send_to_arduino(self.command)