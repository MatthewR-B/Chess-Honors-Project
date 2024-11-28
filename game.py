from pieces import Move, Piece, King, Queen, Bishop, Knight, Rook, Pawn, Coordinate
from typing import Optional

class Game:
    def __init__(self, populate: bool = True, checkEnabled: bool = True) -> None:
        """Initialize board and populate with starting pieces"""
        self.board: list[list[Optional[Piece]]] = [[None]*8 for i in range(8)]
        self.moveHistory: list[Move] = []
        self.visibleMoves: list[Move] = []
        self.turn = "white"
        self.checkEnabled = checkEnabled # False for testing of boardstates without a king
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

    def move(self, mv: Move, checkTesting: bool = False) -> None:
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
        
        if mv.enPassant: # remove pawn if en passant
            self.setSpace(None, self.moveHistory[-1].endPos())

        oppRow = 0 if piece.color == "white" else 7
        if isinstance(piece,Pawn) and mv.endPos()[0] == oppRow: # pawn promotion GIVE OPTION FOR UNDERPROMOTION
            self.setSpace(Queen(self,piece.color,mv.endPos()), mv.endPos())

        self.turn = "black" if self.turn == "white" else "white"
        self.moveHistory.append(mv)

        if not checkTesting and self.checkmate():
            print("Checkmate")
    
    def click(self, pos: Coordinate) -> None:
        """If a piece is already selected, execute the move that ends in the clicked space or deselect if another space is clicked. If a piece is not selected, highlight the moves of the clicked piece if the color matches the turn."""
        if len(self.visibleMoves) > 0:
            for mv in self.visibleMoves:
                if mv.endPos() == pos:
                    self.move(mv)
            self.visibleMoves.clear()
        else:
            content = self.getSpace(pos)
            if isinstance(content, Piece) and content.color == self.turn:
                self.visibleMoves.extend(content.getMoves())

    def copy(self) -> "Game":
        """Return a copy of self"""
        newBoard = Game(populate=False, checkEnabled=self.checkEnabled)
        for r in range(8):
            for c in range(8):
                content = self.getSpace((r,c))
                if isinstance(content, Piece):
                    newBoard.setSpace(content.copy(newBoard),(r,c))
        return newBoard

    def causesCheck(self, mv: Move) -> bool: # CONSIDER CHANGING TO inCheck AND DO COPYING AND MOVE EXECUTION IN addIfValid
        """Return True if a move results in a player putting themself in check"""
        if not self.checkEnabled:
            return False
        newBoard = self.copy()
        for r in range(8): # find king of current player
            for c in range(8):
                content = newBoard.getSpace((r,c))
                if isinstance(content, King) and content.color == self.turn:
                    king = content
                    break
        newBoard.move(mv, checkTesting=True)
        # newBoard.printBoard()
        for r in range(8):
            for c in range(8):
                content = newBoard.getSpace((r,c))
                if isinstance(content, Piece) and content.color == ("black" if self.turn == "white" else "white"):
                    possibleMoves = content.getMoves(checkTesting=True)
                    for move in possibleMoves:
                        if move.endPos() == king.pos:
                            return True # There is a piece of the opposite color that could capture the king
        return False
    
    def checkmate(self) -> bool:
        """Return True if active player has no moves to get out of checkmate"""
        mate = True
        for r in range(8):
            for c in range(8):
                content = self.getSpace((r,c))
                if isinstance(content, Piece):
                    for move in content.getMoves():
                        if not self.causesCheck(move):
                            # print(move)
                            mate = False
                            break
        return mate
    
    def printBoard(self) -> None:
        """Print text representation of the board"""
        for row in self.board:
            for piece in row:
                print(str(piece) if piece else '-', end = " ")
            print()
        print()