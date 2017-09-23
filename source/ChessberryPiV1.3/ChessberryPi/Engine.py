import subprocess, time

class Engine():
    def __init__(self):
        self.engine = subprocess.Popen(
            "stockfish",
            universal_newlines = True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        print("engine connected")
        self.skill = "5"
        self.movetime = "6000"
        self.moves = ""
        self.start_engine = "go movetime "+ self.movetime
        self.new_game()


    def wait_for_engine(self):
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
        stx=""
        self.engine.stdin.write("isready\n")
        print('\nengine:')
        while True :
            text = self.engine.stdout.readline().strip()
            if text == 'readyok':
                break
            if text !='':   
                print('\t'+text)
            if text[0:8] == 'bestmove':
                return text

    def get_board(self):
        pass

    def new_game(self):
        self.wait_for_engine()
        self.send_to_engine('uci')
        self.wait_for_engine()
        self.send_to_engine('setoption name Skill Level value ' + self.skill)
        self.wait_for_engine()
        self.send_to_engine('setoption name Hash value 128')
        self.wait_for_engine()
        self.send_to_engine('setoption name best book move value true')
        self.wait_for_engine()
        self.send_to_engine('setoption name ownbook value true')
        self.wait_for_engine()
        self.send_to_engine('uci')
        self.wait_for_engine()
        self.send_to_engine('ucinewgame')
                
    def send_to_engine(self, command):
        print('\nyou:\n\t' + command)
        self.engine.stdin.write(command+'\n')

    def communicate_engine(self,move):
        self.moves = self.moves + " " + move
        engine_command = "position startpos moves" + self.moves
        #print(engine_command)
        self.send_to_engine(engine_command)
        self.send_to_engine(self.start_engine)