from pieces import Move, Piece, King, Queen, Bishop, Knight, Rook, Pawn, Coordinate
from typing import Optional

class Game:
    def __init__(self, populate: bool = True) -> None:
        """Initialize board and populate with starting pieces"""
        self.board: list[list[Optional[Piece]]] = [[None]*8 for i in range(8)]
        self.moveHistory: list[Move] = []
        if populate:
            pieceList = [Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]
            for col in range(8):
                self.setSpace(pieceList[col](self,'black',(0,col)), (0,col))
                self.setSpace(Pawn(self,'black',(1,col)), (1,col))
                self.setSpace(Pawn(self,'white',(6,col)), (6,col))
                self.setSpace(pieceList[col](self,'white',(7,col)), (7,col))

    def getSpace(self, pos: Coordinate) -> Optional[Piece]:
        """Return contents of space at pos"""
        return self.board[pos[0]][pos[1]]

    def setSpace(self, content: Optional[Piece], pos: Coordinate) -> None: # IF PIECE, DEFAULT TO POS OF PIECE?
        """Set contents of space at pos to content"""
        self.board[pos[0]][pos[1]] = content

        """Execute Move mv"""
        piece = self.getSpace(mv.startPos())
        if piece is None:
            raise RuntimeError("Tried to move from empty space")
        piece.hasMoved = True
        piece.pos = mv.endPos()
        self.setSpace(piece, mv.endPos())
        self.setSpace(None, mv.startPos())
        
        if mv.castle != "": # move rook if castle
            row = 7 if piece.color == "white" else 0
            oldCol,newCol = (7,5) if mv.castle == "kingside" else (0,3)
            rook = self.getSpace((row,oldCol))
            assert rook is not None # to make mypy happy. rook should never be None
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
    
    def printBoard(self) -> None:
        """Print text representation of the board"""
        for row in self.board:
            for piece in row:
                print('-' if piece == None else str(piece), end = " ")
            print()
        print()