class ArduinoInterface:
    def __init__(self):
        pass


class InputHandler(ArduinoInterface):
    def __init__(self):
        super(InputHandler, self).__init__()


class OutputHandler(ArduinoInterface):
    def __init__(self):
        super(ArduinoInterface, self).__init__()

    def send_to_arduino(self, command):
        pass