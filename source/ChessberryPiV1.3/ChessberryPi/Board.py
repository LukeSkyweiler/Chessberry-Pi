import Pieces
import InputOutput
import time

class Board():
    def __init__(self):
        self.InputOutput = InputOutput.InputOutput()
        self.current_byte_state = [0] * 64
        self.raw_input_state = [b'0'] * 64
        self.last_raw_input_state = [b'0'] * 64
        self.reset_state = [b'0'] * 64
        self.last_state = None
        self.moved_piece_index = 64
        self.alive_pieces_off_board = []
        self.dead_pieces_off_board = []
        self.piece_just_moved = None
        self.move_coord = [0] * 2
        self.teams = []
        self.board_map = [[0 for y in range(8)] for x in range(8)]
        self.current_board_pieces = [0] * 64
        self.last_board_pieces = [0] * 66
        self.piece_off_board = False
        self.__FEN_Move = [0] * 2
        self.piece_moved = [0] * 2
        self.initialize_game()
        self.piece_was_placed = False    
        self.SQUARE_NAMES = ['a1','b1','c1','d1','e1','f1','g1','h1','h2','g2','f2','e2','d2','c2','b2','a2','a3','b3','c3','d3','e3','f3','g3','h3','h4','g4','f4','e4','d4','c4','b4','a4','a5','b5','c5','d5','e5','f5','g5','h5','h6','g6','f6','e6','d6','c6','b6','a6','a7','b7','c7','d7','e7','f7','g7','h7','h8','g8','f8','e8','d8','c8','b8','a8']

    def initialize_game(self):
        for i in range(2):
            if i == 0:
                self.teams.append(Pieces.set_of_pieces("White"))
            else:
                self.teams.append(Pieces.set_of_pieces("Black"))
            #Piece position starts the same for each game
        #self.get_board_raw()
        #self.check_state_change()
        for team in self.teams:
            for piece in team.list_of_pieces:
                self.current_board_pieces[piece.current_pos] = piece
        for i in range(64):
            if self.current_board_pieces[i].__class__ == Pieces.board_piece:
                self.raw_input_state[i] = b'1'
        #Update Arduino byte state
        self.update_Arduino(self.current_board_pieces,"pieces")
        #####Needs Work
        #if (self.alive_piece_off_board == None):
        #    self.set_reset_state(self.current_byte_state)
        self.update_map()
       
    def set_reset_state(self,state):
        for i in range(64): self.reset_state[i] = state[i]
    
    def update_board_pieces(self,write_arduino=True):
        for piece in self.alive_pieces_off_board:
            self.current_board_pieces[piece.old_pos] = 1
        if self.piece_was_placed:
            for n,i in enumerate(self.current_board_pieces):
                if i == 1: self.current_board_pieces[n] = 0          

        for team in self.teams:
            for piece in team.list_of_pieces:
                try:
                    self.current_board_pieces[piece.current_pos] = piece
                except: pass
        if write_arduino: self.update_Arduino(self.current_board_pieces,"pieces")

        #Update Arduino byte state
    def update_Arduino(self,state,type):
        if type == "bytes": 
            #print(state)
            self.InputOutput.write_arduino_data(state)
        elif type == "pieces":
            byte_state = [b'0'] * 64
            for i in range(64):
                if state[i] == 0:
                    byte_state[i] = b'0'
                elif state[i] == 1:
                    byte_state[i] = b'3'
                else: 
                    byte_state[i] = state[i].color_byte
            #print(byte_state)
            self.InputOutput.write_arduino_data(byte_state)
        
        #if (self.alive_piece_off_board == None):
         #   self.set_reset_state(self.current_byte_state)

    def compare_board_pieces(self):
        for i in range(64):
            if (self.last_board_pieces[i].piece_id != self.current_board_pieces[i].piece_id):
                return False

    def check_state_change(self):
        state_was_changed = False
        for i in range(64):
            self.last_raw_input_state[i] = self.raw_input_state[i]

        self.get_board_raw()
        move_type = None
        for i in range(64):
            if (self.raw_input_state[i] != self.last_raw_input_state[i]):
            #if a move was detected, determine what piece moved
                state_was_changed = True
                if (self.raw_input_state[i] == b'0' and self.last_raw_input_state[i] == b'1'):
                #piece was removed from board ASSUMED to Always preceed adding
                #a piece
                    for team in self.teams:
                        for piece in team.list_of_pieces:
                            if (piece.current_pos == i and piece.is_alive):
                            #Trigger true if the piece is off the board, but
                            #alive
                                self.piece_was_placed = False
                                piece.was_moved = True
                                piece.old_pos = piece.current_pos
                                piece.current_pos = None
                                self.alive_pieces_off_board.append(piece)
                                if(self.piece_moved[0] == 0): self.piece_moved[0] = piece
                                if (self.piece_just_moved != None): self.piece_just_moved = None
                                self.piece_moved[1] = 0
                                self.current_board_pieces[piece.old_pos] = 0

                if (self.raw_input_state[i] == b'1' and self.last_raw_input_state[i] == b'0'):
                    #piece was placed on board
                    for team in self.teams:
                        for piece in team.list_of_pieces:
                            if (piece in self.alive_pieces_off_board):
                                if (len(self.alive_pieces_off_board) > 1):
                                    if piece.old_pos == i:
                                        #this piece is getting captured
                                        self.dead_pieces_off_board.append(piece)
                                        self.alive_pieces_off_board.remove(piece)
                                        piece.is_alive = False
                                        break
                                    else:
                                        self.alive_pieces_off_board.remove(piece)
                                        self.alive_pieces_off_board[0].is_alive = False

                                        self.dead_pieces_off_board.append(self.alive_pieces_off_board[0])                                        
                                        self.alive_pieces_off_board[:] = []
                                        self.piece_was_placed = True
                                        piece.was_moved = True
                                        self.move_coord[0] = piece.old_pos
                                        piece.old_pos = piece.current_pos
                                        piece.current_pos = i 
                                        self.move_coord[1] = piece.current_pos                                        
                                        self.current_board_pieces[piece.current_pos] = piece
                                        self.piece_moved[1] = piece
                                        self.piece_moved[0] = 0
                                        break

                                self.piece_was_placed = True
                                piece.was_moved = True
                                self.move_coord[0] = piece.old_pos
                                piece.old_pos = piece.current_pos
                                piece.current_pos = i 
                                self.move_coord[1] = piece.current_pos
                                #self.current_board_pieces[piece.current_pos] =
                                #piece
                                if self.current_board_pieces[piece.current_pos] == 1:
                                    move_type = "Capture"
                                else: move_type = "Move"
                                self.current_board_pieces[piece.current_pos] = piece
                                #print(move_type)
                                self.moved_piece_index = self.move_coord[0]
                                #if (self.alive_piece_off_board!=None and
                                #piece.piece_id ==
                                #self.alive_piece_off_board.piece_id):
                                #self.piece_just_moved = piece
                                #Take piece off of off-board list
                                self.alive_pieces_off_board.remove(piece)
                                self.piece_moved[1] = piece
                                self.piece_moved[0] = 0
        return state_was_changed
        #determine if board state has changed, return true or false while
        #waiting for input
                
    def get_board_raw(self):
        self.raw_input_state = self.InputOutput.get_board_state()

    def check_reset_state(self, reset_state):
        waiting = True
        pieces_are_wrong = False
        bytes = [b'0'] * 64
        while(waiting):
            self.get_board_raw()
            for i in range(64):  
                try:
                    if reset_state[i].__class__ == Pieces.board_piece and self.raw_input_state[i] == b'1':
                        bytes[i] = reset_state[i].color_byte 
                except:
                    if reset_state[i] == 0 and self.raw_input_state[i] == b'0':
                        bytes[i] = b'0'
                    else:
                        bytes[i] = b'E'
                        pieces_are_wrong = True
            if (pieces_are_wrong):
                waiting = True
            else: waiting = False
            for i in range(64): 
                if(reset_state[i].__class__ == Pieces.board_piece):print(reset_state[i].tag)
                else: print(reset_state[i])
            print(bytes)
            self.update_Arduino(bytes,"bytes")

    def wait_for_correct_state(self, correct_state):
        waiting = True
        self.generate_reset_bytes(correct_state)
        while(waiting):
            if self.check_state_change():
                self.update_board_pieces(write_arduino=False)
                self.generate_reset_bytes(correct_state)
            for i in range(64):
                if correct_state[i].__class__ != self.current_board_pieces[i].__class__:
                    waiting = True
                    break
                else:
                    waiting = True
                    #try:
                    #    if correct_state[i].piece_id != self.current_board_pieces[i].piece_id: 
                    #        waiting = True
                    #        break
                    #except:
                    #    if correct_state[i] != self.current_board_pieces[i]:
                    #        waiting = True  
                    #        break
                waiting = False

    def process_engine_move(self,move,state):
        fen = move.uci()
        from_pos = fen[0:2]
        to_pos = fen[2:5]
        to_int = self.SQUARE_NAMES.index(to_pos)
        #from_int = None  
        from_int = self.SQUARE_NAMES.index(from_pos)
        print("From int: "+str(from_int))
        print("From FEN: "+from_pos)
        #from_int = self.SQUARE_NAMES.index(from_pos)       
        #to_int = None
        #find corresponding piece
        for i in range(64):
            try:
                if state[i].FEN_pos==from_pos:
                    state[i].engine_moved = True
                    #from_int = i
            except:
                pass
        #state[from_int].engine_moved = True
        #state[to_pos] = state[from_pos]
        #state[from_pos] = 4
        try:
            state[to_int] = state[from_int]
            state[to_int].engine_moved = True
            state[from_int] = 4
        except:
            for i in range(64):
                try:
                    print(str(i)+" - "+state[i].tag)
                except: print(str(i)+" - "+str(state[i]))
            print("Error, Piece not found")
            print("To"+str(to_int))
            print("From"+str(from_int))
            while(True):pass
 
        return state

    def parse_castle(self, move, kingside, state):
        fen = move.uci()
        from_pos = fen[0:2]
        to_pos = fen[2:5]
        to_int = self.SQUARE_NAMES.index(to_pos)
        from_int = self.SQUARE_NAMES.index(from_pos)
        print(from_int,to_int)
        #determine rook to move
        try:
            if (to_int == 2 and not kingside):
                state[0].engine_moved = True
                state[3] = state[0]
                state[0] = 4 
            elif (to_int == 6 and kingside):
                state[7].engine_moved = True
                state[5] = state[7]
                state[7] = 4
            elif (to_int == 59 and not kingside):
                state[7].engine_moved = True
                state[60] = state[63]
                state[63] = 4
            elif (to_int ==57 and kingside):
                state[7].engine_moved = True
                state[58] = state[56]
                state[56] = 4
        except: pass
        return state


    def generate_reset_bytes(self,state):
        byte_state = [b'0'] * 64 
        for i in range(64):
                try:
                    #If the board squares are equal
                    if (state[i].piece_id == self.current_board_pieces[i].piece_id):
                        if state[i].__class__ == Pieces.board_piece:
                            #not getting hit Python 2 vs 3
                            byte_state[i] = state[i].color_byte 
                        elif state[i] == 0: 
                            byte_state[i] = b'0'
                    else:
                        #If both board squares are pieces, but wrong pieces
                        byte_state[i] = b'3'
                #This will trigger if a square is a piece in one and an int in
                #another
                except:
                    if (self.current_board_pieces[i] == 0 and state[i] == 0):
                        
                        byte_state[i] = b'0'
                    elif(self.current_board_pieces[i] == 0 and state[i].__class__ == Pieces.board_piece):
                        if state[i].engine_moved==False:
                            byte_state[i] = b'A'
                        else: byte_state[i] = b'E'
                    elif(self.current_board_pieces[i] == 1 and state[i] == 0):
                        byte_state[i] = b'3' 
                    elif self.current_board_pieces[i].__class__ == Pieces.board_piece and state[i] == 0:
                        byte_state[i] = b'A'
                    elif (state[i]==4 and self.current_board_pieces[i].__class__==Pieces.board_piece):
                        byte_state[i] = b'E'
                    elif (state[i]==4 and self.current_board_pieces[i] == 1):
                        byte_state[i] = b'3'
                        state[i]=0
        self.update_Arduino(byte_state,"bytes")

    def update_map(self):
        '''This function updates the board state with each piece's tag - Used in UI'''
        self.board_map = [[0 for y in range(8)] for x in range(8)]
        for team in self.teams:
            for piece in team.list_of_pieces:
                if piece.current_pos == None:
                    pass
                else:
                    row = piece.current_pos/8
                    try:
                        if row<1:
                            self.board_map[0][7-piece.current_pos] = piece.tag
                            piece.FEN_pos = self.get_column(piece.current_pos)+'1'
                            piece.coord_pos[0] = (piece.current_pos)
                            piece.coord_pos[1] = 0
                        elif (row>=1 and row<2):
                            self.board_map[1][(piece.current_pos-8)] = piece.tag
                            piece.FEN_pos = self.get_column(7-(piece.current_pos-8))+'2'
                            piece.coord_pos[0] = (7-(piece.current_pos-8))
                            piece.coord_pos[1] = 1
                        elif (row>=2 and row<3):
                            self.board_map[2][7-(piece.current_pos-16)] = piece.tag
                            piece.FEN_pos = self.get_column(piece.current_pos-16)+'3'
                            piece.coord_pos[0] = (piece.current_pos -16)
                            piece.coord_pos[1] = 2
                        elif (row>=3 and row<4):
                            self.board_map[3][(piece.current_pos-24)] = piece.tag
                            piece.FEN_pos = self.get_column(7-(piece.current_pos-24))+'4'
                            piece.coord_pos[0] = (7-(piece.current_pos-24))
                            piece.coord_pos[1] = 3
                        elif (row>=4 and row<5):
                            self.board_map[4][7-(piece.current_pos-32)] = piece.tag
                            piece.FEN_pos = self.get_column(piece.current_pos-32)+'5'
                            piece.coord_pos[0] = (piece.current_pos-32)
                            piece.coord_pos[1] = 4
                        elif (row>=5 and row<6):
                            self.board_map[5][(piece.current_pos-40)] = piece.tag
                            piece.FEN_pos = self.get_column(7-(piece.current_pos-40))+'6'
                            piece.coord_pos[0] = 7-(piece.current_pos-40)
                            piece.coord_pos[1] = 5
                        elif (row>=6 and row<7):
                            self.board_map[6][7-(piece.current_pos-48)] = piece.tag
                            piece.FEN_pos = self.get_column(piece.current_pos-48)+'7'
                            piece.coord_pos[0] = piece.current_pos-48
                            piece.coord_pos[1] = 6
                        elif (row>=7):
                            self.board_map[7][(piece.current_pos-56)] = piece.tag
                            piece.FEN_pos = self.get_column(7-(piece.current_pos-56))+'8'
                            piece.coord_pos[0] = 7-(piece.current_pos-56)
                            piece.coord_pos[1] = 7
                    except IndexError:
                        if (piece.current_pos >=64): pass
                    continue
        self.print_board_map()

    def parse_engine(self,FEN_move):
        pass
    
    def print_board_map(self):
        print("\n")
        for row in reversed(self.board_map):
            temp = [str(a) for a in reversed(row)]
            print (','.join(temp))

    def get_column(self,indx):
        if indx==0:return 'a'
        elif indx==1:return 'b'
        elif indx==2:return 'c'
        elif indx==3:return 'd'
        elif indx==4:return 'e'
        elif indx==5:return 'f'
        elif indx==6:return 'g'
        elif indx==7:return 'h'
        else: return 'off'

    def convert_FEN(self,fen):
        column = fen[0]
        row = fen[1]
        number = None
        if row=='1':  pass

    def send_arduino_animation(self, animation):
        self.InputOutput.write_arduino_data(animation)
        print("Waiting on Arduino")
        while(self.InputOutput.read_arduino_data()): pass
        print("Recieved")
        