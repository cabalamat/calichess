# game.py = play a game of chess

from ulib.butil import form, pr, prn, dpr, printargs

from board import *
from movegen import pmovs
import evalpos

#---------------------------------------------------------------------

def getBestMove(b: Board) -> Move:
    """ get the computer's best move in this position """
    computerIsPlaying = b.mover
    
    allMoves = pmovs(b, computerIsPlaying)
    movesValues:List[Tuple[Move,int]] = []
    for mv in allMoves:
        b2 = b.makeMove(mv)
        value = evalpos.staticEval(b2)
        movesValues.append((mv,value))
    ##/for
    
    bestMoves = sorted(movesValues, key=lambda mv: mv[1])[::-1]
    if computerIsPlaying=="B":
        # we want best for black, so reverse order:
        bestMoves = bestMoves[::-1]
        
    bestMove, bestScore = bestMoves[0]    
    prn("Computer's best move is {} scoring {}", 
        toAlmov(bestMove), bestScore)
    return bestMove
    

#---------------------------------------------------------------------

def main():
    b = Board.startPosition()
    while 1:
        prn("Position: {}\n", b.termStr())
        possibleMoves = pmovs(b, "W")
        possMovesStr = [toAlmov(mv) for mv in possibleMoves]
        while 1:
            yourMove = input("Enter your move: ")
            if yourMove in possMovesStr:
                break
            else:    
                prn("Error, legal moves are {}", possMovesStr)
        #//while
        b = b.makeMove(yourMove)
        
        bestMove = getBestMove(b)
        prn("Computer move is {}", toAlmov(bestMove))
        b = b.makeMove(bestMove)
    #//while    
    
#---------------------------------------------------------------------

if __name__=='__main__':
    main()

#end
