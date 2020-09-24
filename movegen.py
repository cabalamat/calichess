# movegen.py = move generation

from typing import List, Literal, Tuple, Union, cast

from board import *

#---------------------------------------------------------------------


def pmovs(b: Board, p: Player) -> List[Move]:
    """ a pmov (for pseudo-move) is a move that would be legal 
    for the player if there were no special rules for check.
    Returns all the pmovs for player (p) in position (b) """
    r: List[Move] = []
    for sqix in sqixs:
        sv = b.sq[sqix]
        if isPlayer(sv, p):
            r += pmovsFor(b, p, sqix, sv)
    #//for
    return r

def pmovsFor(b: Board, p: Player, sqix: Sqix, sv: Sqv) -> List[Move]:
    """ return the pseudo-moves for the piece (sv) on square (sqix) 
    of board (b) """
    if sv==WP:
        return whitePawnMovs(b, sqix)
    elif sv==BP:
        return blackPawnMovs(b, sqix)
    elif sv in knightSet:
        return knightMovs(b, p, sqix)
    elif sv in brqSet:
        return brqMovs(b, p, sqix, sv)
    elif sv in kingSet:
        return kingMovs(b, p, sqix)
    else:
        raise ShouldntGetHere
    
def whitePawnMovs(b: Board, sqix: Sqix) -> List[Move]:
    """ moves for white pawn on (sqix) """
    r: List[Move] = []
    
    # 1 move ahead:
    if b.sq[sqix+WP_MOV]==EMPTY:
        r += [(sqix, sqix+WP_MOV)]
        
    # captures:
    for d in WP_CAPTURE:
        if b.sq[sqix+d] in blackSet:
            r += [(sqix, sqix+d)]
    
    # double first move
    rk = sqixFR(sqix)[1]
    if (rk==2 
        and b.sq[sqix+WP_MOV]==EMPTY 
        and b.sq[sqix+WP_MOV*2]==EMPTY):        
        r += [(sqix, sqix+WP_MOV*2)]
    
    return r
    
def blackPawnMovs(b: Board, sqix: Sqix) -> List[Move]:
    """ moves for black pawn on (sqix) """
    r: List[Move] = []
    
    # 1 move ahead:
    if b.sq[sqix+BP_MOV]==EMPTY:
        r += [(sqix, sqix+BP_MOV)]
        
    # captures:
    for d in BP_CAPTURE:
        if b.sq[sqix+d] in whiteSet:
            r += [(sqix, sqix+d)]
    
    # double first move
    rk = sqixFR(sqix)[1]
    if (rk==7
        and b.sq[sqix+BP_MOV]==EMPTY 
        and b.sq[sqix+BP_MOV*2]==EMPTY):        
        r += [(sqix, sqix+BP_MOV*2)]
        
    return r
    
def knightMovs(b: Board, p: Player, sqix: Sqix) -> List[Move]:
    """ moves for (p)'s knight on (sqix) """
    r: List[Move] = []
    for d in N_MOV:
        if b.sq[sqix+d]==EMPTY or isOpponent(b.sq[sqix+d], p):
            r += [(sqix, sqix+d)]
    #//for d    
    return r
    
def brqMovs(b: Board, p: Player, sqix: Sqix, sv: Sqv) -> List[Move]:
    """ moves for (p)'s piece on (sqix), which is a B/R/Q """
    r: List[Move] = []
    
    if sv in bishopSet:
        ds = B_DIR
    elif sv in rookSet: 
        ds = R_DIR
    else:   
        # (sv) must be a queen
        ds = Q_DIR
    
    #dpr("p={} sqix={} ({}) sv=%r", p, sqix, sqixAlge(sqix), sv)
    for d in ds:
        bound = 1
        
        while True:
            destSqix = sqix + bound*d
            #dpr("d={} bound={} sqix={} ({}) destSqix={} ({})",
            #    d, bound, sqix, sqixAlge(sqix),
            #    destSqix, sqixAlge(destSqix))
            if b.sq[destSqix] == OFFBOARD: break
            if isPlayer(b.sq[destSqix], p): break
            if b.sq[destSqix] == EMPTY:
                r += [(sqix, destSqix)]
            if isOpponent(b.sq[destSqix], p):
                r += [(sqix, destSqix)]
                break
            bound += 1
        #//while    
    #//for d        
    return r
     
def kingMovs(b: Board, p: Player, sqix: Sqix) -> List[Move]:
    """ moves for (p)'s king on (sqix) """
    r: List[Move] = []
    for d in Q_DIR:
        destSqix = sqix+d
        if b.sq[destSqix] == EMPTY or isOpponent(b.sq[destSqix], p):
            r += [(sqix, destSqix)]
    #//for d
    return r
    


#---------------------------------------------------------------------

def main():
    b = Board.startPosition()
    prn("board:\n{}", b)
    wmvs = pmovs(b, 'W') # white's moves from starting position
    prn("white moves = {}", [movAlge(mv) for mv in wmvs]) 
    
    bmvs = pmovs(b, 'B') # blacks's moves from starting position
    prn("black moves = {}", [movAlge(mv) for mv in bmvs]) 

def shortGame():
    b = Board.startPosition()
    prn("board b:\n{}", b.termStr())
    
    b2 = b.makeMove("e2e4")
    prn("board b2:\n{}", b2.termStr())
    
    b3 = b2.makeMove("c7c5")
    prn("board b3:\n{}", b3.termStr())

if __name__=='__main__':
    #main()
    shortGame()


#end
