# test_board.py = test <board.py>

from ulib import lintest

import board
from board import frix, algeSqix, toSqix, movAlmov

#---------------------------------------------------------------------

class T_conversionFunctions(lintest.TestCase):
    """ convert between indexes, algebraic, etc """
    
    def test_toSqix(self):
        ad = (1,1)
        r = toSqix(ad)
        self.assertSame(r, 21, "location (1,1) == index 21")
        
        ad = (3,7)
        r = toSqix(ad)
        self.assertSame(r, 47, "location (3,7) == index 47")
        
        ad = (8,8)
        r = toSqix(ad)
        self.assertSame(r, 98, "location (8,8) == index 98")
        
        ad = 21
        r = toSqix(ad)
        self.assertSame(r, 21, "location 21 == index 21 (no conversion)")
        
        ad = 47
        r = toSqix(ad)
        self.assertSame(r, 47, "location 47 == index 47 (no conversion)")
        
        ad = "a1"
        r = toSqix(ad)
        self.assertSame(r, 21, "location a1 == index 21")
        
        ad = "c7"
        r = toSqix(ad)
        self.assertSame(r, 47, "location c7 == index 47")
        
        ad = "g8"
        r = toSqix(ad)
        self.assertSame(r, 88, "location g8 == index 88")
        
    def toAlge(self):
        ad = (1,1)
        r = toAlge(ad)
        self.assertSame(r, "a1", "location (1,1) == a1")
        
        ad = (3,7)
        r = toAlge(ad)
        self.assertSame(r, "c7", "location (3,7) == c7")
        
        ad = (8,8)
        r = toAlge(ad)
        self.assertSame(r, "h8", "location (8,8) == h8")
        
        ad = 21
        r = toAlge(ad)
        self.assertSame(r, "a1", "location 21 == a1")
        
        ad = 47
        r = toAlge(ad)
        self.assertSame(r, "c7", "location 47 == c7")
        
        ad = "a1"
        r = toAlge(ad)
        self.assertSame(r, "a1", "location a1 == a1 (duh!)")
        
        ad = "c7"
        r = toAlge(ad)
        self.assertSame(r, "c7", "location c7 == c7 (duh!")
        
        ad = "g8"
        r = toAlge(ad)
        self.assertSame(r, "g8", "location g8 == g8 (duh!")
 
#---------------------------------------------------------------------

class T_Board(lintest.TestCase):
    """ test Board class """
    
    def test_empty(self):
        b = board.Board() # empty board
        self.assertSame(b.sq[0], board.OFFBOARD, "sq[0] is off-board")
        self.assertSame(b.sq[120], board.OFFBOARD, "sq[120] is off-board")
        
        sv = b.sq[toSqix("a1")]
        self.assertSame(sv, board.EMPTY, "square a1 empty")
        sv = b.sq[toSqix("a8")]
        self.assertSame(sv, board.EMPTY, "a8 empty")
        sv = b.sq[toSqix("b3")]
        self.assertSame(sv, board.EMPTY, "b3 empty")
        sv = b.sq[toSqix("h7")]
        self.assertSame(sv, board.EMPTY, "h7 empty")
    
    def test_startPosition(self):
        b = board.Board.startPosition()
        
        self.assertSame(b.sq[0], board.OFFBOARD, "sq[0] is off-board")
        self.assertSame(b.sq[120], board.OFFBOARD, "sq[120] is off-board")
        
        sv = b.sq[toSqix("a1")]
        self.assertSame(sv, board.WR, "square a1 = WR")
        sv = b.sq[toSqix("a8")]
        self.assertSame(sv, board.BR, "a8 BR")
        sv = b.sq[toSqix("b3")]
        self.assertSame(sv, board.EMPTY, "b3 empty")
        sv = b.sq[toSqix("h7")]
        self.assertSame(sv, board.BP, "h7 BP")
        
    def test_fen(self):
        b = board.Board.startPosition()
        r = b.toFen()
        self.assertSame(r, 
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1",
            "FEN for start position")
        

#---------------------------------------------------------------------

group = lintest.TestGroup()
group.add(T_conversionFunctions)
group.add(T_Board)

if __name__=='__main__': group.run()

#end
