import Game.ChessGame as ChessGame
import Game.Player as Player


class UserInterface:
    def __init__(self):
        self.game_select = None
        self.player_list = []
        self.game = None

    def menu(self):
        print("Select Type of Game")
        self.select_game()

        print("Select Game Mode")
        self.select_mode()

        print("Launching Game")
        self.launch_game()

    def select_game(self):
        self.game_select = input("Chess")

    def select_mode(self):

        player_list = []
        for i in range(2):
            player_list.append(input("1: Player\n2: AI"))

        self.create_players(player_list)

    def create_players(self, players):

        for player in players:
            if player == "1":
                self.player_list.append(Player.Human())

            elif player == "2":
                self.player_list.append(Player.Computer())

    def launch_game(self):

        if self.game_select == "1":
            self.game = ChessGame.ChessGame(self.player_list)

        self.game.play()


if __name__ == '__main__':
    ui = UserInterface()

    ui.menu()
