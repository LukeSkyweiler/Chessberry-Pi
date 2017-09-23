import time
from Adafruit_GPIO import MCP230xx
import serial

class InputOutput():
    def __init__(self):
        self.__chip1 = MCP230xx.MCP23017(0x20)
        self.__chip2 = MCP230xx.MCP23017(0x21)
        self.__chip3 = MCP230xx.MCP23017(0x22)
        self.__chip4 = MCP230xx.MCP23017(0x23)
        self.__arduino = serial.Serial('/dev/ttyACM0',9600)
        for i in range(16):
            self.__chip1.setup(i,1)
            self.__chip2.setup(i,1)
            self.__chip3.setup(i,1)
            self.__chip4.setup(i,1)
        self.__board_pos = [b'0']*64
        self.__last_board_pos = [0]*64
        self.itt = 0
        self.temp = [b'0']*64
        self.last_byte = [b'0']*64
        
    def get_board_state(self):
        #Uncomment when running on pi
        for i in range(16):
            if not self.__chip1.input(i):
                self.__board_pos[i]=b'1'
                time.sleep(0.001)
            else: self.__board_pos[i]=b'0'
        for i in range(16):
            if not self.__chip2.input(i):
                self.__board_pos[i+16]=b'1'
                time.sleep(0.001)
            else: self.__board_pos[i+16]=b'0'
        for i in range(16):
            if not self.__chip3.input(i):
                self.__board_pos[i+32]=b'1'
                time.sleep(0.001)
            else:self.__board_pos[i+32]=b'0'
        for i in range(16):
            if not self.__chip4.input(i):
                self.__board_pos[i+48]=b'1'
                time.sleep(0.001)
            else: self.__board_pos[i+48]=b'0'
        return self.__board_pos
    
    def write_arduino_data(self, board_state):
        #print("given values")
        #print(board_state)
        for i in board_state:
            self.__arduino.write(i)
    
    def read_arduino_data(self):

        data = self.__arduino.read()
        print(data)
        if (data=='R'):
            print(data)
            return False
        else: return True
'''  
class InputOutput():
    def __init__(self):
        self.__board_pos = [b'0'] * 64
        self.__last_board_pos = [0] * 64
        self.itt = 0
        
    def get_board_state(self):
        #Dummy board_state for testing
        if self.itt == 3:self.itt = 0
        for i in range(64):
            if i < 16: self.__board_pos[i] = b'1'
            elif i >= 48 and i < 64: self.__board_pos[i] = b'1'
            #if i==14 and self.itt==1:
            #    self.__board_pos[14] = b'0'
            #    self.__board_pos[17] = b'1'
            #For FEN
            if i == 16 and self.itt == 1: 
            #pick up piece
                self.__board_pos[i] = b'0'
                self.__board_pos[15] = b'0'
            elif i ==16 and self.itt == 2: 
            #piece is off of board
                self.__board_pos[i] = b'1'
                self.__board_pos[15] = b'0'
            #elif i==51 and self.itt == 3:
            ###piece is placed on board
            #    self.__board_pos[i] = b'0'
            #    self.__board_pos[35] = b'0'     
            #elif i == 35 and self.itt == 4:
            #    self.__board_pos[i] = b'1'
            #    self.__board_pos[51] = b'0'    
            #if i == 9 and self.itt ==0: 
            ##pick up piece
            #    self.__board_pos[i] = b'1'
            #    self.__board_pos[25] = b'0'
            #elif i ==9 and self.itt ==1: 
            ##piece is off of board
            #    self.__board_pos[i] = b'0'
            #    self.__board_pos[25] = b'0'
            #elif i==9 and self.itt==2:
            ##piece is placed on board
            #    self.__board_pos[i] = b'0'
            #    self.__board_pos[25] = b'1'     
            #elif i==55 and self.itt==3:
            #    self.__board_pos[i] = b'0'
            #    self.__board_pos[39] = b'0' 
            #elif i==55 and self.itt==4:
            #    self.__board_pos[i] = b'0'
            #    self.__board_pos[39] = b'1'
            #elif i==8 and self.itt==5:
            #    self.__board_pos[i] = b'0'
            #    self.__board_pos[23]=b'0'
            #elif i==8 and self.itt==6:
            #    self.__board_pos[i]=b'0'
            #    self.__board_pos[23]=b'1'
            #elif i==39 and self.itt==7:
            #    self.__board_pos[i] = b'0'
            #elif i==25 and self.itt==8:
            #    self.__board_pos[i] = b'0'
            #elif i==25 and self.itt==9:
            #    self.__board_pos[i] = b'1' 
            #if self.itt>5: self.__board_pos[8]=b'0'
            #if self.itt>1: self.__board_pos[9]=b'0'
            #if self.itt >3: self.__board_pos[55]=b'0'
            #elif i==55 and self.itt==4:
            #    self.__board_pos[i] = b'0'
            #    self.__board_pos[39] = b'1'
            #elif i==16 and self.itt==4:
            #    self.__board_pos[i] = b'1'
            #    self.__board_pos[15] = b'0'
            #elif i==16 and self.itt==5:
            #    self.__board_pos[i] = b'0'
            #    self.__board_pos[15] = b'0' 
            self.__last_board_pos[i] = self.__board_pos[i]
        self.itt +=1
        return self.__board_pos
    
    def write_arduino_data(self, board_state):
        for i in board_state:
            pass

    def read_arduino_data(self): pass
'''