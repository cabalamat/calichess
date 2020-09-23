# board.py = cheaa board

"""
Codes for a chess board. Allows all the moves from a board position
to be calculated.

Given a poard position, makes a move, returning a new board position.

## Limitations

Doesn't deal with castling, en passant or check.

Pawn promotion is always to Q
"""

from typing import List, Literal, Tuple, Union, cast

from ulib.butil import form, pr, prn, dpr, printargs
from ulib.termcolours import TermColours

from tpcheck import is_type

#---------------------------------------------------------------------
# exceptions

class ShouldntGetHere(Exception): pass

#---------------------------------------------------------------------
# types

Rank = int # chess rank 1..8
File = int # chess file a..h as 1..8
FileRank = Tuple[File,Rank]
ranks = [1,2,3,4,5,6,7,8]
files = [1,2,3,4,5,6,7,8]

Sqix = int # address as index of Board.sq

def frix(f: File, r: Rank) -> Sqix:
    """ convert file and rank to index of sq[] """
    return 10 + 10*f + r

def sqixFR(sqix: Sqix) -> FileRank:
    """ convert a square index to  file and rank """
    f = int(sqix/10) - 1
    rk = sqix % 10
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
    
SqLocation = Union[FileRank, str, Sqix]

def toSqix(ad: SqLocation) -> Sqix:
    """ convert a location to a square index, from
    - a square indedx (do nothing)
    - a RankFile, e.g. (2,4)=>34
    - algebraic, e.g. b4 => 34
    """
    if is_type(ad, Sqix):
        return ad
    elif is_type(ad, FileRank):
        return frix(ad[0], ad[1])
    elif isinstance(ad, str):
        return algeSqix(ad)
    else:
        raise ShouldntGetHere

def toAlge(ad: SqLocation) -> str:
    """ convert a location to algebraic notation, from
    - a square index, e.g. 34 => 'b4'
    - a RankFile, e.g. (2,4)=>'b4'
    - algebraic, e.g. b4 => 'b4' (do nothing)
    """
    if is_type(ad, Sqix):
        return sqixAlge(ad)
    elif is_type(ad, FileRank):
        f, rk = ad
        return form("{}{}", "?abcdefghij"[f], rk)
    elif isinstance(ad, str):
        return ad # do nothing
    else:
        raise ShouldntGetHere

# a list of all the on-board square addresses
sqixs = [toSqix((f,r)) 
         for f in files 
         for r in ranks]

# a move is a 4-tuple of Sqix e.g. "e2e4" would be (62,64)
Move = Tuple[Sqix,Sqix]

# An Almov is a move in algebraic notation e.g. "e2e4"
Almov = str

# Different ways of describing a move:
MovAlmov = Union[Move, Almov]

def movAlmov(mv: Move) -> str:
    """ convert a move to algebraic notation  e.g. 'e2e4' """
    return toAlge(mv[0]) + toAlge(mv[1])

def almovMov(am: Almov) -> Move:
    """ convert an Almov (e.g. "a2a3") to a Move
    (e.g. (22,23) ).
    """
    mv = (toSqix(am[:2]), toSqix(am[2:]))
    return mv

def toAlmov(m: MovAlmov) -> Almov:
    """ convert a move (in Almov or Move form)
    to Almov form, i.e. like 'h7h5' """
    if isinstance(m, str):
        # it's already an Almov
        return m
    else:
        return movAlmov(m)
    

def toMov(m: MovAlmov) -> Move:
    """ convert a move-like to a Move """
    if isinstance(m, str):
        return almovMov(m)
    else:
        # it's already a Move
        return m
    
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

# a player is either White or Black
Player = Literal['W', 'B']

def opponent(p: Player) -> Player:
    """ (p)'s opponent """
    return "W" if p=="B" else "B"
    
def isPlayer(sv: Sqv, p: Player) -> bool:
    """ does (sv) belong to player (p)? """
    return ((p=='W' and sv in whiteSet)
            or (p=='B' and sv in blackSet))

def isOpponent(sv: Sqv, p: Player) -> bool:
    """ does (sv) belong to the opponent of player (p)? """
    return isPlayer(sv, opponent(p))

# directions of movement
WP_MOV = 1
WP_CAPTURE = [-9, 11]
BP_MOV = -1
BP_CAPTURE = [-11, 9]
N_MOV = [-21, -19, -12, -8, 8, 12, 19, 21]
B_DIR = [-11, -9, 9, 11]
R_DIR = [-10, -1, 1, 10]
Q_DIR = B_DIR + R_DIR

#---------------------------------------------------------------------

class Board:
    sq: List[Sqv] = []
    mover: Player = 'W'
    movesMade: List[Move] = []
    
    def __init__(self):
        """ create an empty board """
        self.sq = [OFFBOARD]*121
        for sqix in sqixs:
            self.sq[sqix] = EMPTY
            
    def copy(self) -> 'Board':
        b2 = Board()
        b2.sq = self.sq[:]
        b2.mover = self.mover
        b2.movesMade = self.movesMade[:]
        return b2
        
    @staticmethod    
    def startPosition() -> 'Board':
        """ return the start position """
        b = Board()
        b.setRank(8, "RNBQKBNR") # rank 8 = black pieces
        b.setRank(7, "PPPPPPPP") # rank 7 = black pawns
        b.setRank(2, "pppppppp") # rank 2 = white pawns
        b.setRank(1, "rnbqkbnr") # rank 1 = white pieces 
        return b
    
    def getSq(self, ad:SqLocation) -> Sqv:
        return self.sq[toSqix(ad)]
        
    def setSq(self, ad:SqLocation , sv: Sqv):  
        self.sq[toSqix(ad)] = sv
               
    def setRank(self, r: Rank, pieces: str):
        """ set all the pieces on a rank """
        for f in files:
            pc = pieces[f-1]
            self.sq[toSqix((f,r))] = pc
            
    def __str__(self) -> str:
        """ a string representation of a board, for printing """
        s = self.headerStr() + self.midAsciiStr() + self.footerStr()
        return s
    
    def termStr(self) -> str:
        """ output the board to a xterm output device """
        s = self.headerStr() + self.midTermStr() + self.footerStr()
        return s
    
    def headerStr(self) -> str:
        """ string for header of board output """
        s = form("{} to move; Previous: {}\n", 
                 self.mover, self.prevMovesStr())
        s += "    a b c d e f g h\n"
        return s
    
    def midAsciiStr(self) -> str:
        """ middle of board output as ascii string """
        s = "  +-----------------+\n"
        for r in ranks[::-1]:
            s += form("{} | ", r)
            for f in files:
                sv: Sqv = self.sq[toSqix((f,r))]
                if sv==" " and (f+r)%2==0: 
                    s += "# "
                else:
                    s += sv + " "
            #//for f
            s += "|\n"
        #//for r 
        s += "  +-----------------+\n"
        return s
    
    def midTermStr(self) -> str:
        """ middle of board output as xterm string """
        W_BEFORE = (TermColours.BOLD + chr(27) + "[38;2;128;0;0m"
            + chr(27) + "[48;2;255;220;220m")
        W_AFTER = TermColours.NORMAL
        B_BEFORE = (TermColours.BOLD + chr(27) + "[38;2;0;0;128m" 
            + chr(27) + "[48;2;220;220;255m")
        B_AFTER = TermColours.NORMAL
        s = "  \u2554" + "\u2550"*17 + "\u2557\n"
        for r in ranks[::-1]:
            s += form("{} \u2551 ", r)
            for f in files:
                sv: Sqv = self.sq[toSqix((f,r))]
                bg = "\u2591" if (f+r)%2==0 else " "
                if sv==" " and (f+r)%2==0: 
                    s += bg + " "
                else:
                    b = ""; a = ""
                    if sv in whiteSet:
                        b = W_BEFORE; a = W_AFTER    
                    elif sv in blackSet:
                        b = B_BEFORE; a = B_AFTER
                    s += b + sv + a + " "
            #//for f
            s += "\u2551\n"
        #//for r 
        s += "  \u255A" + "\u2550"*17 + "\u255D\n"
        return s
    
    def footerStr(self) -> str:
        """ string for header of board output """
        s = "    a b c d e f g h"
        return s
    
    def prevMovesStr(self) -> str:
        """ a string containing the previous moves """
        s = ""
        for mv in self.movesMade:
            s += toAlmov(mv) + " "
        #//for    
        return s

    def makeMove(self, m: Move) -> 'Board':
        mv = toMov(m)
        b2 = self.copy()
        b2.mover = opponent(self.mover)
        b2.movesMade = self.movesMade + [m]
        sqFrom, sqTo = mv
        b2.sq[sqTo] = b2.sq[sqFrom]
        b2.sq[sqFrom] = EMPTY
        
        #>>>>> check for promoting pawns
        _, rankTo = sqixFR(sqTo)
        if self.mover=='W':
            # W promotes on 8th rank
            if rankTo==8 and b2.sq[sqTo]==WP:
                b2.sq[sqTo] = WQ
        else: 
            # B promotes on 1st rank
            if rankTo==1 and b2.sq[sqTo]==BP:
                b2.sq[sqTo] = BQ       
        
        return b2

 
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
