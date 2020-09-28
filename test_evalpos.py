# test_evalpos.py  = test <evalpos.py>

from ulib import lintest

from board import *
import evalpos
from evalpos import staticEval, material

#---------------------------------------------------------------------

class T_material(lintest.TestCase):
    """ test materal evaluation """
    
    def test_empty(self):
        b = Board() 
        v = material(b)
        self.assertSame(v, 0, "material ev for empty board")
        
    def test_start(self):
        b = Board.startPosition() 
        v = material(b)
        self.assertSame(v, 0, "material ev for start position")
        
    def test_pawn(self):
        b = Board()
        b.setSq("a2", WP)
        v = material(b)
        self.assertSame(v, evalpos.P_VALUE, "pawn value")
        
    def test_knight(self):
        b = Board()
        b.setSq("a2", BN)
        v = material(b)
        self.assertSame(v, -evalpos.N_VALUE, "knight value")
        
    def test_bishop(self):
        b = Board()
        b.setSq("a2", WB)
        v = material(b)
        self.assertSame(v, evalpos.B_VALUE, "bishop value")
        
    def test_rook(self):
        b = Board()
        b.setSq("f2", BR)
        v = material(b)
        self.assertSame(v, -evalpos.R_VALUE, "rook value")
        
    def test_queen(self):
        b = Board()
        b.setSq("g2", WQ)
        v = material(b)
        self.assertSame(v, evalpos.Q_VALUE, "queen value")
        
    def test_king(self):
        b = Board()
        b.setSq("h5", BK)
        v = material(b)
        self.assertSame(v, -evalpos.K_VALUE, "king value")

    
#---------------------------------------------------------------------

class T_pawnStructure(lintest.TestCase):
    """ test pawn structure """
    
    def test_doubledIsolated_empty(self):
        b = Board()
        v = evalpos.pawnStructureW(b)
        self.assertSame(v, 0, "no doubled/isolated pawns on empty board")
   
    def test_doubledIsolated_start(self):
        b = Board.startPosition()
        v = evalpos.pawnStructureW(b)
        self.assertSame(v, 0, "no doubled/isolated pawns on start position")
        
        
    def test_isolated(self):
        b = Board()
        b.setSq("b2", WP)
        v = evalpos.pawnStructureW(b)
        self.assertSame(v, evalpos.ISOLATED+evalpos.PASSED, 
            "passed isolated pawn on b2")
        
        
    def test_doubledIsolatedWhite(self):
        b = Board()
        b.setSq("f7", BP)
        b.setSq("f6", BP)
        b.setSq("f4", BP)
        v = evalpos.pawnStructureW(b)
        self.assertSame(v, 0, 
            "no white pawns")
        
        v = evalpos.pawnStructureW(b.getMirror())
        self.assertSame(v, 
            evalpos.ISOLATED*3 + evalpos.DOUBLED*2 
            + evalpos.PASSED + evalpos.PASSED_ADVANCE[9-4], 
            "black->white tripled isolated pawns on f-file, but passed")
        
 
    
#---------------------------------------------------------------------

class T_mobility(lintest.TestCase):
    """ test mobility (and king attack/defence) """
    
    def test_calcSqImportance(self):
        b = Board.startPosition()
        sqImp = evalpos.calcSqImportance(b)
        self.assertSame(len(sqImp), len(b.sq), 
            "square-importance array (sqImp) is the right length")
        prn("square importance:")
        prn("    a b c d e f g h")
        for rk in ranks[::-1]:
            pr("{} : ", rk)
            for f in files:
                pr("{} ", sqImp[toSqix((f,rk))])
            #//for f
            pr("\n")
        #//for rk    
            
        
#---------------------------------------------------------------------

group = lintest.TestGroup()
group.add(T_material)
group.add(T_pawnStructure)
group.add(T_mobility)

if __name__=='__main__': group.run()


#end
