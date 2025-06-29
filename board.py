# board.py = chess board

"""
Codes for a chess board. Allows all the moves from a board position
to be calculated.

Given a poard position, makes a move, returning a new board position.

## Limitations

Doesn't deal with castling, en passant or check.

Pawn promotion is always to Q
"""

from typing import List, Literal, Tuple, Union, cast, Optional

from ulib.butil import form, pr, prn, dpr, printargs
from ulib.termcolours import TermColours

from tpcheck import is_type

#---------------------------------------------------------------------
# exceptions

class ShouldntGetHere(Exception): pass

#---------------------------------------------------------------------
# types and definitions

Rank = int # chess rank 1..8
File = int # chess file a..h as 1..8
FileRank = Tuple[File,Rank]
ranks = [1,2,3,4,5,6,7,8]
reverseRanks = ranks[::-1]
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

WP='P'
WN='N'
WB='B'
WR='R'
WQ='Q'
WK='K'

BP='p'
BN='n'
BB='b'
BR='r'
BQ='q'
BK='k'

EMPTY=' '
OFFBOARD='-'

# a square-value is what can go in a Board.sq[] element
Sqv = Literal['P', 'N', 'B', 'R', 'Q', 'K',
              'p', 'n', 'b', 'r', 'q', 'k',
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

# directions of movement
WP_MOV = 1
WP_CAPTURE = [-9, 11]
BP_MOV = -1
BP_CAPTURE = [-11, 9]
N_MOV = [-21, -19, -12, -8, 8, 12, 19, 21]
B_DIR = [-11, -9, 9, 11]
R_DIR = [-10, -1, 1, 10]
Q_DIR = B_DIR + R_DIR

PIECE_TO_UNICODE = {
    " ": " ",
    "P": "\u2659",
    "N": "\u2658",
    "B": "\u2657",
    "R": "\u2656",
    "Q": "\u2655",
    "K": "\u2654",
    "p": "\u265F",
    "n": "\u265E",
    "b": "\u265D",
    "r": "\u265C",
    "q": "\u265B",
    "k": "\u265A"
}

def toChessUnicode(ch: str) -> str:
    return ch
    return PIECE_TO_UNICODE.get(ch, "?")

#---------------------------------------------------------------------
# players 

# a player is either White or Black
Player = Literal['W', 'B']

def opponent(p: Player) -> Player:
    """ (p)'s opponent """
    return "W" if p=="B" else "B"

OPP_PIECE = {}
for wp, bp in [[WP, BP], [WN, BN], [WB, BB], 
               [WR, BR], [WQ, BQ], [WK, BK]]:
    OPP_PIECE[wp] = bp
    OPP_PIECE[bp] = wp

def opponentPiece(pv: Sqv) -> Sqv:
    """ if (pv) is a piece, return the opponent's equivalent piece
    else return EMPTY.
    """
    return OPP_PIECE.get(pv, EMPTY)
    
def isPlayer(sv: Sqv, p: Player) -> bool:
    """ does (sv) belong to player (p)? """
    return ((p=='W' and sv in whiteSet)
            or (p=='B' and sv in blackSet))

def isOpponent(sv: Sqv, p: Player) -> bool:
    """ does (sv) belong to the opponent of player (p)? """
    return isPlayer(sv, opponent(p))

#---------------------------------------------------------------------
# functions for mirrors

def mirrorSq(sx: Sqix) -> Sqix:
    """ return the mirror of a square address """
    f, rk = sqixFR(sx)
    return toSqix((f, 9-rk))

def mirrorMove(mv: Move) -> Move:
    """ return the mirror of a move """
    src, dest = mv
    return (mirrorSq(src), mirrorSq(dest))

def mirrorMoves(mvs: List[Move]) -> List[Move]:
    """ return the mirror of a list of moves """
    return [mirrorMove(mv) for mv in mvs]

#---------------------------------------------------------------------

class Board:
    #----- game position:
    sq: List[Sqv] = []
    mover: Player = 'W'
    castleWK: bool = True 
    castleWQ: bool = True 
    castleBK: bool = True 
    castleBQ: bool = True 
    mspmc: int = 0 # moves since pawn move or capture
    ply: int = 0 # moves made by either player
    
    #----- history:
    movesMade: List[Move] = []
    
    #----- useful stuff for move generation, evaluation, etc
    mirror: Optional['Board'] = None
    wMovs: Optional[List[Move]] = None
    bMovs: Optional[List[Move]] = None
    
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
        b.setRank(8, "rnbqkbnr") # rank 8 = black pieces 
        b.setRank(7, "pppppppp") # rank 7 = black pawns
        b.setRank(2, "PPPPPPPP") # rank 2 = white pawns
        b.setRank(1, "RNBQKBNR") # rank 1 = white pieces
        return b
    
    @staticmethod    
    def fromFEN(fen: str) -> 'Board':
        """ create Board from FEN """
        b = Board()
        fen2 = fen.split()
        if len(fen2)!=6:
            raise ValueError(form("Bad FEN of %r", fen))
        fb = fen2[0]
        fbRanks = fb.split("/")
        if len(fbRanks)!=8:
            raise ValueError(form("Bad fen=%r, wrong number of files",
                fen))
        for rk in ranks:
            b.setRank(rk, fbRanks[8-rk])
            
        b.mover = "W" if fen2[1]=="w" else "B"
        b.castleWK = "K" in fen2[2]
        b.castleWQ = "Q" in fen2[2]
        b.castleBK = "k" in fen2[2]
        b.castleBQ = "q" in fen2[2]
        
        b.mspmc = int(fen2[4])
        moveToMake = int(fen2[5])
        b.ply = (moveToMake-1)*2 + int(b.mover=="B")
        return b
    
    def toFen(self) -> str:
        """ output position in FEN notation """
        s = ""
        for rk in ranks[::-1]:
            s += self._toFenRank(rk) + "/"
        #//for rk
        s = s[:-1] + " " + self.mover.lower()
        s += form(" {} ", self._toFenCastling()) # TODO: castling
        s += "- " # TODO: en passant
        s += form("{} ", self.mspmc)
        s += form("{}", int(self.ply/2) + 1)
        return s
    
    def _toFenRank(self, rk) -> str:
        """ return FEN-string for rank (rk) """
        s = ""
        numSpaces = 0
        for f in files:
            sv = self.sq[toSqix((f,rk))]
            if sv==" ": 
                numSpaces += 1
            else:
                if numSpaces >= 1:
                    s += form("{}", numSpaces)
                    numSpaces = 0
                s += sv
        #//for f       
        if numSpaces >= 1:
            s += form("{}", numSpaces)
        return s   
    
    def _toFenCastling(self) -> str:
        s = ""
        if self.castleWK: s+= "K"
        if self.castleWQ: s+= "Q"
        if self.castleBK: s+= "k"
        if self.castleBQ: s+= "q"
        if not s: s = ""
        return s
    
    def getSq(self, ad:SqLocation) -> Sqv:
        return self.sq[toSqix(ad)]
        
    def setSq(self, ad:SqLocation , sv: Sqv):  
        self.sq[toSqix(ad)] = sv
               
    def setRank(self, r: Rank, pieces: str):
        """ set all the pieces on a rank """
        pieces2 = expandRank(pieces)
        for f in files:
            pc = pieces2[f-1]
            self.sq[toSqix((f,r))] = pc
            
    def getMirror(self) -> 'Board':
        """ a mirror is the same position as the Board, but mirrored
        along the boundary of the 4th and 5th ranks, and with colours
        reversed.
        
        Using mirrors means you don't have to write separate code 
        for white and black in some instances. 
        """
        if not self.mirror:
            self.mirror = self.calcMirror()
        return self.mirror
    
    def calcMirror(self) -> 'Board':
        """ Return a Board that is the mirror of (self) """
        mir = Board()
        for sx in sqixs:
            mir.sq[mirrorSq(sx)] = opponentPiece(self.sq[sx])
        mir.mover = opponent(self.mover)  
        return mir
    
    def createMoves(self):
        """ create wMovs, bMovs etc if they are not already
        created. 
        """
        import movegen
        if self.wMovs is not None: return # don't create again
        self.wMovs = movegen.pmovs(self, 'W')
        self.bMovs = movegen.pmovs(self, 'B')
        
            
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
                    s += b + toChessUnicode(sv) + a + " "
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
        sqFrom, sqTo = mv
        b2 = self.copy()
        b2.mover = opponent(self.mover)
        b2.movesMade = self.movesMade + [m]
        b2.ply = self.ply + 1  
        
        #>>>>> is it a pawn move or capture?
        if (self.sq[sqFrom] in pawnSet
            or self.sq[sqTo] != EMPTY):
            b2.mspmc = 0
        else:
            b2.mspmc = self.mspmc + 1
            
        #>>>> do the move 
        b2.sq[sqTo] = b2.sq[sqFrom]
        b2.sq[sqFrom] = EMPTY
        b2._checkCanCastle()   
        
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
    
    def _checkCanCastle(self):
        """ if W or B can no longer castle, change the relevant
        castling flag. 
        """
        if self.getSq("h1")!="R": self.castleWK = False
        if self.getSq("a1")!="R": self.castleWQ = False
        if self.getSq("e1")!="K": 
            self.castleWK = False
            self.castleWQ = False
        if self.getSq("h8")!="r": self.castleBK = False
        if self.getSq("a8")!="r": self.castleBQ = False
        if self.getSq("e8")!="k": 
            self.castleBK = False
            self.castleBQ = False

def expandRank(p: str) -> str:
    """ (p) is a rank in FEN format. Returns the same rank but 
    with digits expanded to that number of spaces. 
    """
    r = ""
    for ch in p:
        if ch.isdigit():
            r += " " * int(ch)
        else:
            r += ch
    #//for ch
    r += " "*8
    r = r[:8]
    return r
 
 
#---------------------------------------------------------------------

def main():
    b = Board.startPosition()
    prn("board:\n{}", b)
    prn("Prettier board:\n{}", b.termStr())


if __name__=='__main__':
    main()

#end
