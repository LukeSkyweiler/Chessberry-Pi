
class set_of_pieces():
    def __init__(self, piece_color):
        self.piece_color = piece_color
        self.LED_color = None
        self.list_of_pieces = []
        self.__initialize_set()

    def __initialize_set(self):
        #This function cretes and appends each chess piece for each team
        if self.piece_color =="Black":
            for piece in range(8):
                self.list_of_pieces.append(board_piece('Pawn',piece+8,8,b'P','w'))
            for piece in range(2):
                if piece == 0:
                    self.list_of_pieces.append(board_piece('Rook',piece,2,b'R','w'))
                    self.list_of_pieces.append(board_piece('Knight',piece+1,2,b'N','w'))
                    self.list_of_pieces.append(board_piece('Bishop',piece+2,2,b'B','w'))
                    self.list_of_pieces.append(board_piece('Queen',piece+3,1,b'Q','w'))
                else:
                    self.list_of_pieces.append(board_piece('Rook',piece+6,2,b'R','w'))
                    self.list_of_pieces.append(board_piece('Knight',piece+5,2,b'N','w'))
                    self.list_of_pieces.append(board_piece('Bishop',piece+4,2,b'B','w'))
                    self.list_of_pieces.append(board_piece('King',piece+3,1,b'K','w'))
        else:
            for piece in range(8):
                self.list_of_pieces.append(board_piece('Pawn',63-piece-8,8,b'p','b'))
            for piece in range(2):
                if piece == 0:
                    self.list_of_pieces.append(board_piece('Rook',63-piece,piece,b'r','b'))
                    self.list_of_pieces.append(board_piece('Knight',63-piece-1,piece,b'n','b'))
                    self.list_of_pieces.append(board_piece('Bishop',63-piece-2,piece,b'b','b'))
                    self.list_of_pieces.append(board_piece('Queen',63-piece-3,1,b'q','b'))
                else:
                    self.list_of_pieces.append(board_piece('Rook',63-piece-6,piece,b'r','b'))
                    self.list_of_pieces.append(board_piece('Knight',63-piece-5,piece,b'n','b'))
                    self.list_of_pieces.append(board_piece('Bishop',63-piece-4,piece,b'b','b'))
                    self.list_of_pieces.append(board_piece('King',63-piece-3,1,b'k','b'))
    

class board_piece():
    def __init__(self,piece_type,starting_pos,piece_number,color_byte,piece_team):
        self.piece_type = piece_type
        self.piece_team = piece_team
        self.starting_pos = starting_pos
        self.current_pos = starting_pos
        self.old_pos = starting_pos
        self.was_taken_off_board = False
        self.was_placed_on_board = False
        self.was_moved = False
        self.color_byte = color_byte
        if piece_type=="Knight": self.tag = 'N'
        else: self.tag = piece_type[:1]
        if(self.piece_team=="b"): self.tag = self.tag.lower()
        self.piece_id = self.tag+str(self.starting_pos)
        self.FEN_pos = None
        self.coord_pos = [None]*2
        self.color = None
        self.is_alive = True
        self.allowable_move = None
        self.engine_moved = False
        
