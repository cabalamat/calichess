# evalpos.py = static evaluation of a position

"""
Make a static evaluation of a chess position

Evaluates boards in accordance with:

- material (1 pawn = 100 points; vales favouring W are +ve)
- Pawn structure
- mobility / K attack / K defence
- pieces under threat / repeated captures on a square

"""

import board
from board import *

#---------------------------------------------------------------------

def staticEval(b: Board) -> int:
    """ statically evlauate a position """
    r = material(b)
    
    return r

#---------------------------------------------------------------------
# material

P_VALUE =  100
N_VALUE =  300
B_VALUE =  310
R_VALUE =  490
Q_VALUE =  900
K_VALUE = 9000

pieceValues = {
    WP: P_VALUE,
    WN: N_VALUE,
    WB: B_VALUE,
    WR: R_VALUE,
    WQ: Q_VALUE,
    WK: K_VALUE,
    BP: -P_VALUE,
    BN: -N_VALUE,
    BB: -B_VALUE,
    BR: -R_VALUE,
    BQ: -Q_VALUE,
    BK: -K_VALUE,
}    

def material(b: Board) -> int:
    """ material evaluation of a position """
    v = 0
    for sqix in sqixs:
        v += pieceValues.get(b.sq[sqix], 0)
    return v




#---------------------------------------------------------------------

#end
