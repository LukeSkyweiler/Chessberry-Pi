import Board
import chess
import chess.uci



class Game():
    def __init__(self):
        self.Board = Board.Board()
        self.chess = chess.Board()
        self.engine = chess.uci.popen_engine("stockfish")
        self.engine.uci()
        self.game_over = False
        self.FEN_Move = [0]*2
        self.piece_Move = [0]*2
        self.list_of_moves = []
        self.invalid_move_reset = [b'0']*64
        self.reset_state = self.Board.current_board_pieces[:]
        self.valid_move_animation = b'v'
        self.opening_animation = b'$'
        self.invalid_move_reset_animation = b'i'
        self.correct_engine_move_animation = b'@'
        self.check_animation = b'c'
        self.checkmate_animation = b'C'
        self.textmove = ""


    def engines_play(self): 
        self.InitializeGame()
        self.engineWhite = chess.uci.popen_engine("stockfish")
        self.engineWhite.uci()
        self.engineWhite.setoption({"Skill Level":18})
        self.engine.setoption({"Skill Level":1})
        self.chess.clear_stack()
        print(self.chess)
        while (not self.game_over):
            white_move = None
            black_move = None

            self.engineWhite.position(self.chess)
            white_move = self.engineWhite.go(movetime=2000)
            print(white_move.bestmove)
            self.Engine_move(white_move.bestmove)
            if (self.chess.is_castling(white_move.bestmove)):
                print("Castling") 
                state = self.Board.current_board_pieces[:]
                castle_state = self.Board.parse_castle(white_move.bestmove, self.chess.is_kingside_castling(white_move.bestmove), state)
                self.Board.wait_for_correct_state(castle_state)
            self.chess.push(white_move.bestmove)
            if(self.chess.is_check()):
                self.Board.send_arduino_animation(self.check_animation)
                self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")
            else:
                self.Board.send_arduino_animation(self.correct_engine_move_animation)
                self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")
            if (self.chess.is_game_over()):
                print(self.checkmate_animation)
                self.Board.send_arduino_animation(self.checkmate_animation)
                self.game_over = True
            print(self.chess)


            self.engine.position(self.chess)
            black_move = self.engine.go(movetime=500)
            print(black_move.bestmove)
            self.Engine_move(black_move.bestmove)
            if (self.chess.is_castling(black_move.bestmove)):
                print("Castling") 
                state = self.Board.current_board_pieces[:]
                castle_state = self.Board.parse_castle(black_move.bestmove, self.chess.is_kingside_castling(black_move.bestmove), state)
                self.Board.wait_for_correct_state(castle_state)
            self.chess.push(black_move.bestmove)
            if(self.chess.is_check()):
                self.Board.send_arduino_animation(self.check_animation)
                self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")
            else:
                self.Board.send_arduino_animation(self.correct_engine_move_animation)
                self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")
            if (self.chess.is_game_over()):
                self.Board.send_arduino_animation(self.checkmate_animation)
                self.game_over = True
            print(self.chess)

    def play_AI_game(self):
        print("Starting Game - Set Pieces in to correct positions")
        self.Board.wait_for_correct_state(self.reset_state)
        self.InitializeGame()
        self.engine.setoption({'Skill Level':1})
        #print(self.engine.options)
        current_FEN_move = [0]*2
        self.chess.clear_stack()

        while(not self.game_over):
            result = self.wait_for_valid_move()
            print(self.chess)
            print("\nSending board to engine")
            self.engine.position(self.chess)
            output = self.engine.go(movetime=100)
            print(output.bestmove)
            if (self.chess.is_castling(output.bestmove)):
                print("Castling") 
                state = self.Board.current_board_pieces[:]
                castle_state = self.Board.parse_castle(output.bestmove, self.chess.is_kingside_castling(output.bestmove), state)
                self.Board.wait_for_correct_state(castle_state)
            self.Engine_move(output.bestmove)
            self.chess.push(output.bestmove)
            self.reset_state = self.Board.current_board_pieces[:]
            #self.Board.wait_for_correct_state(self.reset_state)
            #plays animation if in check
            if(self.chess.is_check()):
                self.Board.send_arduino_animation(self.check_animation)
                self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")
            else:
                self.Board.send_arduino_animation(self.correct_engine_move_animation)
                self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")
            if (self.chess.is_game_over()):
                self.Board.send_arduino_animation(self.checkmate_animation)
                print("Checkmate... Suck My Dick Human")
                self.game_over = True
            print(self.chess)
            print("Engine moved")

    def wait_for_valid_move(self, desired_move = None):
        if desired_move == None:
            changed = False
            FEN_Move = [0]*2
            move_not_complete = True
            from_xy = None
            to_xy = None
            xy_move = [None]*2
            valid_move = False
            while(move_not_complete):
                changed = self.Board.check_state_change()
                if changed:
                    self.Board.update_board_pieces()
                    self.Board.update_map()
                    if (self.Board.piece_moved[0] != 0):
                        FEN_Move[0] = self.Board.piece_moved[0].FEN_pos
                        from_xy = tuple(self.Board.piece_moved[0].coord_pos[:])
                        self.piece_Move[0] = self.Board.piece_moved[0]
                    elif (self.Board.piece_moved[1] != 0): 
                        FEN_Move[1] = self.Board.piece_moved[1].FEN_pos
                        to_xy = tuple(self.Board.piece_moved[1].coord_pos[:])
                        
                        #validmoves = self.chess.getValidMoves(from_xy)
                        #self.textmove = "".join(FEN_Move[0]+FEN_Move[1])
                        #if (self.Board.piece_moved[1].tag=='P' or self.Board.piece_moved[1].tag=='p'):
                        #    san = "".join(FEN_Move[0]+FEN_Move[1])
                        #    move = self.chess.Move.from_uci(san)
                        #else:
                        #    san = "".join(self.Board.piece_moved[1].tag.upper()+FEN_Move[1])
                        self.textmove = "".join(FEN_Move[0]+FEN_Move[1])
                        move = chess.Move.from_uci(self.textmove)
                        try:
                            #print("Is Casteling? - ")
                            #print(self.chess.is_castling(move))
                            if move in self.chess.legal_moves:
                                self.chess.push(move)
                            else: raise ValueError('Invalid move')
                            if (self.chess.is_castling(move)):
                                print("Castling") 
                                state = self.Board.current_board_pieces[:]
                                castle_state = self.Board.parse_castle(move, self.chess.is_kingside_castling(move), state)
                                self.Board.wait_for_correct_state(castle_state)
                            #self.chess.push(move)
                            valid_move = True
                            print("Valid Move")
                            self.reset_state = self.Board.current_board_pieces[:]
                            #self.Board.wait_for_correct_state(self.reset_state)
                            move_not_complete = False
                            xy_move[0] = from_xy
                            xy_move[1] = to_xy
                            if(self.chess.is_check()): 
                                self.Board.send_arduino_animation(self.check_animation)
                                self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")
                            else:
                                self.Board.send_arduino_animation(self.valid_move_animation)
                                self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")
                            if (self.chess.is_game_over()):
                                self.Board.send_arduino_animation(self.checkmate_animation)
                                print("Checkmate")
                                self.game_over = True
                        except ValueError as e:
                            print(e.args)
                            print("Invalid Move - Reset Board")
                            self.Board.send_arduino_animation(self.invalid_move_reset_animation)
                            self.Board.wait_for_correct_state(self.reset_state)
                            for i in range(2): self.Board.piece_moved[i] = 0
                            for i in range(2): FEN_Move[i] = 0
                            print("Board reset")

                        self.piece_Move[1] = self.Board.piece_moved[1]
                        self.list_of_moves.append(self.piece_Move)
                        self.piece_Move = [0]*2
                if(0 not in FEN_Move): move_not_complete = False    
                changed = False
            if valid_move: return True
        else: pass

    def InitializeGame(self): 
        self.Board.send_arduino_animation(self.opening_animation)
        self.Board.update_board_pieces()

    def Engine_move(self,move):
        engine_state = self.Board.current_board_pieces[:]
        engine_state = self.Board.process_engine_move(move,engine_state)
        self.Board.wait_for_correct_state(engine_state)
        #self.Board.send_arduino_animation(self.correct_engine_move_animation)
        #self.Board.update_Arduino(self.Board.current_board_pieces,"pieces")

