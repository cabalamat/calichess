# test_board.py = test <board.py>

from ulib import lintest

import board
from board import frix, pmovs, algeSqix, movAlge, toSqix

#---------------------------------------------------------------------

class T_conversionFunctions(lintest.TestCase):
    """ convert between indexes, algebraic, etc """
    
    def test_toSqix(self):
        ad = (1,1)
        r = toSqix(ad)
        self.assertSame(r, 21, "location (1,1) == index 21")
 
#---------------------------------------------------------------------

class T_Board(lintest.TestCase):
    """ test Board class """
    
    def test_empty(self):
        b = board.Board() # empty board
        self.assertSame(b.sq[0], board.OFFBOARD, "sq[0] is off-board")
        self.assertSame(b.sq[120], board.OFFBOARD, "sq[120] is off-board")
        
        sv = b.sq[frix(1,1)] #a1
        self.assertSame(sv, board.EMPTY, "square a1 empty")
        sv = b.sq[frix(1,8)] #a8
        self.assertSame(sv, board.EMPTY, "a8 empty")
        sv = b.sq[frix(2,3)] #b3
        self.assertSame(sv, board.EMPTY, "b3 empty")
        sv = b.sq[frix(8,7)] #h7
        self.assertSame(sv, board.EMPTY, "h7 empty")
    
    def test_startPosition(self):
        b = board.Board.startPosition()
        
        self.assertSame(b.sq[0], board.OFFBOARD, "sq[0] is off-board")
        self.assertSame(b.sq[120], board.OFFBOARD, "sq[120] is off-board")
        
        sv = b.sq[frix(1,1)] #a1
        self.assertSame(sv, board.WR, "square a1 = WR")
        sv = b.sq[frix(1,8)] #a8
        self.assertSame(sv, board.BR, "a8 BR")
        sv = b.sq[frix(2,3)] #b3
        self.assertSame(sv, board.EMPTY, "b3 empty")
        sv = b.sq[frix(8,7)] #h7
        self.assertSame(sv, board.BP, "h7 BP")

#---------------------------------------------------------------------
 
class T_moveGeneration(lintest.TestCase):
    """ test generating moves """
    
    def test_empty(self):
        b = board.Board() # empty board
        mvs = pmovs(b, 'W')
        self.assertSame(mvs, [], "empty board, no moves for white")
        
        mvs = pmovs(b, 'B')
        self.assertSame(mvs, [], "empty board, no moves for black")
        
    def test_king(self): 
        b = board.Board() # empty board
        b.sq[algeSqix("a3")] = 'k' # WK on a3
        mvs = pmovs(b, 'W')
        alMvs = sorted(movAlge(mv) for mv in mvs)
        sb = ['a3a2', 'a3a4', 'a3b2', 'a3b3', 'a3b4']
        self.assertSame(alMvs, sb, "5 king moves")
        
    def test_king_ppop(self):
        """ test king moves with player's and opponent's pieces """
        b = board.Board() # empty board
        b.sq[algeSqix("a3")] = 'k' # WK on a3
        b.sq[algeSqix("a2")] = 'p' # WP on a2
        b.sq[algeSqix("b4")] = 'R' # BR on b4
        
        mvs = pmovs(b, 'W')
        alMvs = sorted(movAlge(mv) for mv in mvs)
        sb = ['a3a4', 'a3b2', 'a3b3', 'a3b4']
        self.assertSame(alMvs, sb, "4 king moves")
      
#---------------------------------------------------------------------


group = lintest.TestGroup()
group.add(T_conversionFunctions)
group.add(T_Board)
group.add(T_moveGeneration)

if __name__=='__main__': group.run()

#end
