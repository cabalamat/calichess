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
    r = material(b) + pawnStructure(b)
    
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
# pawn structure

DOUBLED =  -20 # penalty for every pawn after 1st on a file
ISOLATED = -40 # panalty for each isolated pawn

def pawnStructure(b: Board) -> int:
    """ pawn structure evaluation of a position """
    return doubledIsolated(b)

def doubledIsolated(b: Board) -> int:
    """ evaluation of a position wrt doubled and isolated pawns """
    v = 0
    
    # white/black pawns on each file:
    wpFile = [0]*9
    bpFile = [0]*9
    for f in files:
        for rk in ranks:
            sv: Sqv = b.getSq((f,rk))
            if sv==WP:
                wpFile[f] += 1
            elif sv==BP:
                bpFile[f] += 1
        #//for
    #//for   
    
    # W/B pawns on neighbouring files:
    wpNeigh = [0]*9
    bpNeigh = [0]*9 
    for f in files:
        if f==1:
            wpNeigh[1] = wpFile[2]
            bpNeigh[1] = bpFile[2]
        elif f==8: 
            wpNeigh[8] = wpFile[7]
            bpNeigh[8] = bpFile[7]   
        else:
            wpNeigh[f] = wpFile[f-1] + wpFile[f+1]
            bpNeigh[f] = bpFile[f-1] + bpFile[f+1]
            
        #>>> doubled pawns:
        if wpFile[f]>=1:
            v += DOUBLED*(wpFile[f]-1)
        if bpFile[f]>=1:
            v -= DOUBLED*(bpFile[f]-1)
            
        #>>> isolated pawns:
        if wpFile[f]>=1 and wpNeigh[f]==0:
            v += ISOLATED*wpFile[f]
        if bpFile[f]>=1 and bpNeigh[f]==0:
            v -= ISOLATED*bpFile[f]
    #//for
    return v


#---------------------------------------------------------------------

#end
