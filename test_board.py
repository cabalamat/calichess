# test_board.py = test <board.py>

from ulib import lintest

import board
from board import frix, pmovs, algeSqix, toSqix, movAlmov

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
        b.sq[toSqix("a3")] = 'k' # WK on a3
        mvs = pmovs(b, 'W')
        alMvs = sorted(movAlmov(mv) for mv in mvs)
        sb = ['a3a2', 'a3a4', 'a3b2', 'a3b3', 'a3b4']
        self.assertSame(alMvs, sb, "5 king moves")
        
    def test_king_ppop(self):
        """ test king moves with player's and opponent's pieces """
        b = board.Board() # empty board
        b.sq[toSqix("a3")] = 'k' # WK on a3
        b.sq[toSqix("a2")] = 'p' # WP on a2
        b.sq[toSqix("b4")] = 'R' # BR on b4
        
        mvs = pmovs(b, 'W')
        alMvs = sorted(movAlmov(mv) for mv in mvs)
        sb = ['a3a4', 'a3b2', 'a3b3', 'a3b4']
        self.assertSame(alMvs, sb, "4 king moves")
        
    def test_queen(self):
        b = board.Board()
        b.setSq("c2", "q")
        b.setSq("c4", "p")
        b.setSq("e4", "N")
        
        mvs = pmovs(b, 'W')
        alMvs = [movAlmov(mv) for mv in mvs]
        alMvsQ = sorted(almv for almv in alMvs if almv[:2]=='c2')
        sb = sorted([
            'c2b1', 
            'c2b2', 'c2a2',
            'c2b3', 'c2a4',
            'c2c3', 
            'c2d3', 'c2e4',
            'c2d2', 'c2e2', 'c2f2', 'c2g2', 'c2h2',
            'c2d1',
            'c2c1'])
        self.assertSame(alMvsQ, sb, "15 Q moves, including 1 capture")
        
        alMvsP = sorted(almv for almv in alMvs if almv[:2]=='c4')
        self.assertSame(alMvsP, ['c4c5'], "1 P move")
        
    def test_makeMove(self):
        b = board.Board.startPosition()
        self.assertSame(b.getSq("e2"), "p", "WP on e2")
        self.assertSame(b.getSq("e1"), "k", "WK on e1")
        
        b2 = b.makeMove("e2e4")
        self.assertSame(b2.getSq("e2"), " ", "nothing on e2")
        self.assertSame(b2.getSq("e4"), "p", "WP on e4")
        
      
#---------------------------------------------------------------------


group = lintest.TestGroup()
group.add(T_conversionFunctions)
group.add(T_Board)
group.add(T_moveGeneration)

if __name__=='__main__': group.run()

#end
