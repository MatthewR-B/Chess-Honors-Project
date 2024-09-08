# mypy: disable-error-code="call-overload"
from pieces import *
class Game:
    def __init__(self) -> None:
        self.board = [[None]*8 for i in range(8)]
        self.moveHistory = []
        pieceList = [Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]
        col = 0
        for piece in pieceList:
            self.board[0][col] = piece(self,'black',(0,col))
            self.board[1][col] = Pawn(self,'black',(1,col))
            self.board[6][col] = Pawn(self,'white',(6,col))
            self.board[7][col] = piece(self,'white',(7,col))
            col += 1
    
    def __str__(self) -> str:
        boardStr = ""
        for row in self.board:
            for piece in row:
                boardStr += ('-' if piece == None else piece.__str__()) + ' '
            boardStr += "\n"
        return boardStr

    def move(self, mv: Move) -> None:
        piece = self.getSpace(mv.startPos())
        piece.hasMoved = True
        piece.pos = mv.endPos()
        self.setSpace(piece, mv.endPos())
        self.setSpace(None, mv.startPos())
        self.moveHistory.append(mv)
        # CHECK FOR CASTLE TO MOVE ROOK
        # ADD MOVE LOGGING

    def getSpace(self, pos: tuple[int,int]) -> Piece | None:
        return self.board[pos[0]][pos[1]]

    def setSpace(self, content: Piece | None, pos: tuple[int,int]) -> None:
        self.board[pos[0]][pos[1]] = content