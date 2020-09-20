# board.py = cheaa board

"""
Codes for a chess board. Allows all the moves from a board position
to be calculated.

Given a poard position, makes a move, returning a new board position.

At the momnet, doesn't deal with castling, en passant or check.
"""

from typing import List, Literal, Tuple, Union

from ulib.butil import form, pr, prn, dpr, printargs

#---------------------------------------------------------------------
# types

Rank = int # chess rank 1..8
File = int # chess file a..h as 1..8
RankFile = Tuple[Rank,File]
ranks = [1,2,3,4,5,6,7,8]
files = [1,2,3,4,5,6,7,8]

Sqix = int # address as index of Board.sq

def frix(f: File, r: Rank) -> Sqix:
    """ convert file and rank to index of sq[] """
    return 10 + f + 10*r

def sqixFR(sqix: Sqix) -> Tuple[File, Rank]:
    """ convert a square index to  file and rank """
    rk = int(sqix/10) - 1
    f = sqix % 10
    return (f,rk)

def sqixAlge(sqix: Sqix) -> str:
    """ convert a Sqix to algebraic notation  e.g. 'a1' """
    f, rk = sqixFR(sqix)
    s = form("{}{}", "?abcdefghij"[f], rk)
    return s

def algeSqix(a: str) -> Sqix:
    """ convert from algebraic notation to Sqix """
    fi = ord(a[0]) - ord('a') + 1
    rk = int(a[1])
    return frix(fi, rk)
    
SqLocation = Union[RankFile, str, Sqix]

def toSqix(ad: SqLocation) -> Sqix:
    """ convert a location to a square index, from
    - a square indedx (do nothing)
    - a RankFile, e.g. (2,4)=>34
    - algebraic, e.g. b4 => 34
    """
    if isinstance(ad, Sqix):
        return ad
    elif isinstance(ad, RankFile):
        return frix(ad[0], ad[1])
    elif isinstance(ad, str):
        return algeSqix(ad)
    else:
        ShouldntGetHere

# a list of all the valid square addresses
sqixs = [frix(f,r) 
         for f in files 
         for r in ranks]

# a move is a 4-tuple of Sqix e.g. "e2e4" would be (62,64)
Move = Tuple[Sqix,Sqix]

# a player is either White or Black
Player = Literal['W', 'B']

class ShouldntGetHere(Exception): pass

def movAlge(mv: Move) -> str:
    """ convert a move to algebraic notation  e.g. 'e2e4' """
    return sqixAlge(mv[0]) + sqixAlge(mv[1])
    
#---------------------------------------------------------------------
# values that can go in sq[]:

WP='p'
WN='n'
WB='b'
WR='r'
WQ='q'
WK='k'

BP='P'
BN='N'
BB='B'
BR='R'
BQ='Q'
BK='K'

EMPTY=' '
OFFBOARD='-'

# a square-value is what can go in a Board.sq[] element
Sqv = Literal['p', 'n', 'b', 'r', 'q', 'k',
              'P', 'N', 'B', 'R', 'Q', 'K',
              ' ', '-']

whiteSet = frozenset([WP,WN,WB,WR,WQ,WK])
blackSet = frozenset([BP,BN,BB,BR,BQ,BK])
pawnSet = frozenset([WP, BP])
knightSet = frozenset([WN, BN])
bishopSet = frozenset([WB, BB])
rookSet = frozenset([WR, BR])
brqSet = frozenset([WB, WR, WQ, BB, BR, BQ])
queenSet = frozenset([WQ, BQ])
kingSet = frozenset([WK, BK])

def isPlayer(sv: Sqv, p: Player) -> bool:
    """ does (sv) belong to player (p)? """
    return ((p=='W' and sv in whiteSet)
            or (p=='B' and sv in blackSet))

def isOpponent(sv: Sqv, p: Player) -> bool:
    """ does (sv) belong to the opponent of player (p)? """
    oppo: Player = "W" if p=="B" else "B"
    return isPlayer(sv, oppo)

# directions of movement
NDIR = [-21, -19, -12, -8, 8, 12, 19, 21]
BDIR = [-11, -9, 9, 11]
RDIR = [-10, -1, 1, 10]
QDIR = BDIR + RDIR

#---------------------------------------------------------------------

class Board:
    def __init__(self):
        """ create an empty board """
        self.sq = [OFFBOARD]*121
        for sqix in sqixs:
            self.sq[sqix] = EMPTY
        
    @staticmethod    
    def startPosition() -> 'Board':
        """ return the start position """
        b = Board()
        b.setRank(8, "RNBQKBNR") # rank 8 = black pieces
        b.setRank(7, "PPPPPPPP") # rank 7 = black pawns
        b.setRank(2, "pppppppp") # rank 2 = white pawns
        b.setRank(1, "rnbqkbnr") # rank 1 = white pieces 
        return b
               
    def setRank(self, r: Rank, pieces: str):
        """ set all the pieces on a rank """
        for f in files:
            pc = pieces[f-1]
            self.sq[frix(f, r)] = pc
            
    def __str__(self) -> str:
        """ a string representation of a board, for printing """
        s = "    a b c d e f g h\n"
        s +="  +-----------------+\n"
        for r in ranks[::-1]:
            s += form("{} | ", r)
            for f in files:
                sv: Sqv = self.sq[frix(f, r)]
                if sv==" " and (f+r)%2==0: 
                    s += "# "
                else:
                    s += sv + " "
            #//for f
            s += "|\n"
        #//for r 
        s +="  +-----------------+\n"
        s += "    a b c d e f g h"
        return s

    def makeMove(self, m: Move) -> 'Board':
        pass

 
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
    if b.sq[sqix+10]==EMPTY:
        r += [(sqix, sqix+10)]
        
    # capture-left:
    if b.sq[sqix+9] in blackSet:
        r += [(sqix, sqix+9)]
        
    # capture-right:
    if b.sq[sqix+11] in blackSet:
        r += [(sqix, sqix+11)]
    
    # double first move
    rk = sqixFR(sqix)[1]
    if rk==2 and b.sq[sqix+10]==EMPTY and b.sq[sqix+20]==EMPTY:        
        r += [(sqix, sqix+20)]
    
    return r
    
def blackPawnMovs(b: Board, sqix: Sqix) -> List[Move]:
    """ moves for black pawn on (sqix) """
    r: List[Move] = []
    
    # 1 move ahead:
    if b.sq[sqix-10]==EMPTY:
        r += [(sqix, sqix-10)]
        
    # capture-left:
    if b.sq[sqix-11] in whiteSet:
        r += [(sqix, sqix-11)]
        
    # capture-right:
    if b.sq[sqix-9] in whiteSet:
        r += [(sqix, sqix-9)]
    
    # double first move
    rk = sqixFR(sqix)[1]
    if rk==7 and b.sq[sqix-10]==EMPTY and b.sq[sqix-20]==EMPTY:        
        r += [(sqix, sqix-20)]
    
    return r
    
def knightMovs(b: Board, p: Player, sqix: Sqix) -> List[Move]:
    """ moves for (p)'s knight on (sqix) """
    NDIR = [-21, -19, -12, -8, 8, 12, 19, 21]
    r: List[Move] = []
    for d in NDIR:
        if b.sq[sqix+d]==EMPTY or isOpponent(b.sq[sqix+d], p):
            r += [(sqix, sqix+d)]
    #//for d    
    return r
    
def brqMovs(b: Board, p: Player, sqix: Sqix, sv: Sqv) -> List[Move]:
    """ moves for (p)'s piece on (sqix), which is a B/R/Q """
    r: List[Move] = []
    
    if sv in bishopSet:
        ds = BDIR
    elif sv in rookSet: 
        ds = RDIR
    else:   
        # (sv) must be a queen
        ds = QDIR
    
    dpr("p={} sqix={} ({}) sv=%r", p, sqix, sqixAlge(sqix), sv)
    for d in ds:
        bound = 1
        
        while True:
            destSqix = sqix + bound*d
            dpr("d={} bound={} sqix={} ({}) destSqix={} ({})",
                d, bound, sqix, sqixAlge(sqix),
                destSqix, sqixAlge(destSqix))
            if b.sq[destSqix] == OFFBOARD: break
            if isPlayer(b.sq[destSqix], p): break
            if b.sq[destSqix] == EMPTY:
                r += [(sqix, destSqix)]
            if isOpponent(b.sq[destSqix], p):
                r += [(sqix, destSqix)]
                break
            bound += 1
    #//for d        
    return r
    
@printargs    
def kingMovs(b: Board, p: Player, sqix: Sqix) -> List[Move]:
    """ moves for (p)'s king on (sqix) """
    r: List[Move] = []
    for d in QDIR:
        destSqix = sqix+d
        if b.sq[destSqix] == EMPTY or isOpponent(b.sq[destSqix], p):
            r += [(sqix, destSqix)]
    #//for d
    return r
    


#---------------------------------------------------------------------

def main():
    b = Board()
    prn("board:\n{}", b)
    mvs = pmovs(b, 'W') # white's moves from starting position
    prn("white moves = {}", [movAlge(mv) for mv in mvs]) 

if __name__=='__main__':
    main()


#end
