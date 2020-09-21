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
        self.assertSame(v, evalpos.P_VALUE)

      
#---------------------------------------------------------------------

group = lintest.TestGroup()
group.add(T_material)

if __name__=='__main__': group.run()


#end
