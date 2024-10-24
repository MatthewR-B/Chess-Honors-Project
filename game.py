from pieces import *
from typing import Optional

class Game:
        """Initialize board and populate with starting pieces"""
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
        
        if (mv.castle != ""): # move rook if castle
            row = 7 if piece.color == "white" else 0
            oldCol,newCol = (7,5) if mv.castle == "kingside" else (0,3)
            rook = self.getSpace((row,oldCol))
            rook.hasMoved = True
            rook.pos = (row,newCol)
            self.setSpace(rook,(row,newCol))
            self.setSpace(None,(row,oldCol))
        
        oppRow = 0 if piece.color == "white" else 7
        if isinstance(piece,Pawn) and mv.endPos()[0] == oppRow: # pawn promotion GIVE OPTION FOR UNDERPROMOTION
            self.setSpace(Queen(self,piece.color,mv.endPos()), mv.endPos())

        self.moveHistory.append(mv)
        # ADD MOVE LOGGING

    def getSpace(self, pos: Coordinate) -> Optional[Piece]:
        """Return contents of space at pos"""
        return self.board[pos[0]][pos[1]]

    def setSpace(self, content: Optional[Piece], pos: Coordinate) -> None:
        """Set contents of space at pos to content"""
        self.board[pos[0]][pos[1]] = content