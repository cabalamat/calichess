# test_movegen.py = test <movegen.py>


from ulib import lintest

import board
from movegen import *

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
group.add(T_moveGeneration)

if __name__=='__main__': group.run()


#end
