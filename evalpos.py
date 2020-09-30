# evalpos.py = static evaluation of a position

"""
Make a static evaluation of a chess position

Evaluates boards in accordance with:

- material (1 pawn = 100 points; vales favouring W are +ve)
- Pawn structure
- mobility / K attack / K defence
- pieces under threat / repeated captures on a square

"""

from typing import Optional, Dict, List

import board
from board import *

#---------------------------------------------------------------------

def staticEval(b: Board) -> int:
    """ statically evlauate a position """
    v = material(b) + pawnStructure(b) + mobility(b)
    #v += swapOff(b)
    
    return v

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

""" for passed pawns, only consider the most advanced pawn for each
file 
"""
PASSED = 20 # for each file with a passed pawn (PP) on it
PROTECTED_PASSED = 30 # if PP has P on neighbouring ranks

# bonus for advanced PP, 0th to 8th ranks:
PASSED_ADVANCE = [None, None, 0, 5, 10, 40, 80, 200, None]

def pawnStructure(b: Board) -> int:
    """ pawn structure evaluation of a position """
    v = pawnStructureW(b) - pawnStructureW(b.getMirror())
    return v

def pawnStructureW(b: Board) -> int:
    """ Evaluation of a position wrt doubled, isolated and passed 
    pawns, for white. (Mirroring is used to evaluate for black.)
    
    wpFile[f] = the number of white pawns on file (f)
    wpNeigh[f] = the number of white pawns on neighbouring files 
        to (f)
    mostAdvanced[f] = the rank (2..7) of the most advanced WP
        on file (f), or 0 if none
    """
    v = 0
    
    # white pawns on each file:
    wpFile = [0]*9 
    mostAdvanced = [0]*9
    for f in files:
        for rk in [7,6,5,4,3,2]:
            sv: Sqv = b.getSq((f,rk))
            if sv==WP:
                wpFile[f] += 1
                if mostAdvanced[f]==0:
                    mostAdvanced[f] = rk
        #//for
    #//for   
    
    # W/B pawns on neighbouring files:
    wpNeigh = [0]*9
    for f in files:
        if f==1:
            wpNeigh[1] = wpFile[2]
        elif f==8: 
            wpNeigh[8] = wpFile[7]
        else:
            wpNeigh[f] = wpFile[f-1] + wpFile[f+1]
            
        #>>> doubled pawns:
        if wpFile[f]>=1:
            v += DOUBLED*(wpFile[f]-1)
            
        #>>> isolated pawns:
        if wpFile[f]>=1 and wpNeigh[f]==0:
            v += ISOLATED*wpFile[f]
    #//for
    
    passedV = 0
    #>>>>> claculate passed pawns
    for f in files:
        if mostAdvanced[f]>0:
            if not blackBlocking(b, f, mostAdvanced[f]):
                # it's a passed pawn
                passedV += PASSED
                if wpNeigh[f]:
                    passedV += PROTECTED_PASSED
                passedV += PASSED_ADVANCE[mostAdvanced[f]]    
    #//for f
    dpr("passedV=%r", passedV)
    v += passedV
    return v

def blackBlocking(b: Board, f: File, rk: Rank):
    """ W has a pawn at (f,rk). Is black bloacking it, by
    having a pawn ahead of it on that file or the fiels next 
    to it?
    """
    uf = [f]
    if f>1: uf += [f-1]
    if f<8: uf += [f+1]
    for cf in uf:
        for crk in range(rk+1,7+1):
            if b.getSq((cf,crk)) == BP:
                return True # blocking, not passed
        #//for crk    
    #//for cf
    return False # not blocking
    

#---------------------------------------------------------------------
# mobility and attack

""" 
Every square has a base value for being attacked (BASE)

On top of this, certain squares have bonuses for being attacked.
These are:

- the 4 inner center squares (CENTER)
- the 12 outer center squares (OUTER_CENTER)
- the square the enemy K is on (EK)
- squares one away (horiz/vert/diag) from enemy K (EK1)
- squares 2 away from enemy K (EK2)
"""

BASE = 1
CENTER = 2
OUTER_CENTER = 1
EK = 4
EK1 = 2
EK2 = 1
FINAL_MULTIPLIER = 1


def mobility(b: Board) -> int:
    b.createMoves()
    wMob = mobilityW(b, b.wMovs)
    dpr("wMob={}", wMob)
    bMob = mobilityW(b.getMirror(), mirrorMoves(b.bMovs))
    dpr("bMob={}", bMob)
    v = wMob - bMob
    return v

def mobilityW(b: Board, movs: List[Move]) -> int:
    #attacks = b.getWAttacks()
    sqWeights = calcSqImportance(b)
    v = 0
    for sourceSq, destSq in movs:
        v += sqWeights[destSq]
    #//for  
    v = int(v * FINAL_MULTIPLIER)
    return v
    
def calcSqImportance(b: Board) -> List[int]:
    """ return how important each square is """
    si: List[int] = [0]*len(b.sq)
    
    bkLocation = getBkSq(b)
    for sx in sqixs:
        si[sx] = BASE
        if sx in [54,55,
                  64,65]: 
            si[sx] += CENTER
        elif sx in [43,44,45,46, 
                    53,      56, 
                    63,      66, 
                    73,74,75,76]: 
            si[sx] += OUTER_CENTER
            
        distBK = dist(sx, bkLocation)    
        if distBK == 0: 
            si[sx] += EK
        elif distBK == 1:
            si[sx] += EK1 
        elif distBK == 2:
            si[sx] += EK2  
    #//for sx
    return si
    
def getBkSq(b: Board) -> Optional[Sqix]:
    """ return the square with the black king on it, or None """
    for sx in sqixs:
        if b.sq[sx] == BK:
            return sx
    return None

def dist(sx1: Sqix, sx2: Sqix) -> int:
    """ return the distance between (sx1) and (sx2), in terms of 
    number of king moves 
    """
    f1, rk1 = sqixFR(sx1)
    f2, rk2 = sqixFR(sx2)
    df = abs(f1-f2)
    drk = abs(rk1-rk2)
    return max(df, drk)

#---------------------------------------------------------------------
   
def swapOff(b: Board) -> int:   
    """ can the mover profitably capture on a square """
    
    movAtt = b.moverAttacks()
    oppDef = b.opponentDefends()
    
    #lump mover attacks and opponent defends by destination sq
    movAttLump: lump(movAtt)
    oppDefLump = lump(oppDef)
    
    for dest in sqixs:
        if movAttLump[dest]:
            sosq = swapOffSq(b, movAttLump, oppDefLump, dest)
    #//for        
    
def lumpByDest(mvs: List[Move]) -> Dict[Sqix,List[Move]]: 
    """ lump a list of moves together by destination square """
    d: Dict[Sqix,List[Move]] = {sx:[] for sx in sqixs}
    for mv in mvs:
        _, dest = mv
        d[dest].append(mv)
    return d   

def swapOffSq(b: Board, 
              movAttLump:Dict[Sqix,List[Move]],
              oppDefLump:Dict[Sqix,List[Move]],
              dest: Sqix) -> int:
    """ calculate how much the attacker would gain, if anything, 
    by capturing on square (dest).
    """
    attPieces = [b.sq[src]
                 for src,_ in movAttLump[dest]]
    dpr("attPieces=%r", attPieces)
    attPieceValues = sorted(abs(pieceValues[p]) 
                            for p in attPieces)
    dpr("attPieceValues=%r", attPieceValues)
    #oppDef = b.sq[dest]
    #oppDefOthers = sorted(abs(pieceValues[b.sq[src]])
    #                      for src,_ in oppDefLump[dest]) 
    

            


#---------------------------------------------------------------------

#end
