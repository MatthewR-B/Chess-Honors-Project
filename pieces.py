from typing import Optional, TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

Coordinate: TypeAlias = tuple[int,int]

class Move:
    """Represents the potential movement of a piece from one space to another, storing the coordinates of all spaces through which the piece must travel"""
    def __init__(self, spaces: list[Coordinate], castle: str = "", doublePawn: str = "", enPassant: bool = False) -> None:
        self._spaces = spaces
        self.castle = castle # kingside, queenside, or empty
        self.doublePawn = doublePawn # white, black, or empty
        self.enPassant = enPassant # True or False

    def startPos(self) -> Coordinate:
        """Get first space in move"""
        return self._spaces[0]
    
    def endPos(self) -> Coordinate:
        """Get final space in move"""
        return self._spaces[-1]
    
    def partialCastle(self) -> "Move":
        """Return a new Move including the first two spaces of self for testing if castling moves through check"""
        return Move(self._spaces[0:2])

    def __repr__(self) -> str:
        """Return string representation of Move"""
        c = f', castle={self.castle}' if self.castle != '' else ''
        d = f', doublePawn={self.doublePawn}' if self.doublePawn != '' else ''
        e = f', enPassant=True' if self.enPassant else ''
        return f"Move({self.startPos()} to {self.endPos()}{c}{d}{e})"

class Piece:
    """Parent class for all pieces, storing color, location, and whether the piece has moved yet"""
    CARDINAL_DIRECTIONS = ((1,0),(0,-1),(-1,0),(0,1))
    DIAGONAL_DIRECTIONS = ((1,1),(1,-1),(-1,-1),(-1,1))
    ALL_DIRECTIONS = CARDINAL_DIRECTIONS + DIAGONAL_DIRECTIONS

    def __init__(self, color: str) -> None:
        """Initialize Piece with its color. _board and pos are set using the setSpace method of Game"""
        self._board: Optional[Game] = None
        self.pos: Optional[Coordinate] = None
        self.color = color
        self.hasMoved = False

    def setBoard(self, board) -> None:
        """Assign a board to this piece"""
        self._board = board

    def _hasPiece(self, pos: Coordinate) -> bool:
        """Return True if there is a piece at pos"""
        if self._board is None:
            raise RuntimeError("Piece not assigned to board")
        return self._inBounds(Move([pos])) and self._board.getSpace(pos) is not None
    
    def _oppositeColor(self):
        """Return the color that is not this piece's color"""
        return "black" if self.color == "white" else "white"

    def _addIfValid(self, mv: Move, moves: list[Move], allowCapture: bool = True) -> bool:
        """Add mv to moves if it is in bounds, there are no pieces in the way, and it does not cause check. Return True if the first two conditions are met."""
        if self._board is None:
            raise RuntimeError("Piece not assigned to board")
        if self._inBounds(mv) and self._moveFree(mv, allowCapture):
            if not self._board.checkEnabled:
                moves.append(mv)
            elif not self._board.causesCheck(mv):
                if not mv.castle:
                    moves.append(mv)
                elif not self._board.causesCheck(mv.partialCastle()) and not self._board.inCheck(): # only add a castle move if not starting in or moving through check 
                    moves.append(mv)
            return True # indicates that movesInLine should continue to check spaces
        return False

    def _inBounds(self, mv: Move) -> bool:
        """Return True if the last space in mv is on the board"""
        row = mv.endPos()[0]
        col = mv.endPos()[1]
        return row >= 0 and row <= 7 and col >= 0 and col <= 7
    
    def _moveFree(self, mv: Move, allowCapture: bool) -> bool:
        """Return True if the last space in a move is empty or has an piece available to capture, and all other spaces are empty"""
        if self._board is None:
            raise RuntimeError("Piece not assigned to board")
        for loc in mv._spaces[1:-1]: # check if all except first and last space are empty
            if self._hasPiece(loc):
                return False
        lastSpace = self._board.getSpace(mv.endPos())
        return lastSpace is None or (allowCapture and lastSpace.color == self._oppositeColor())
    
    def _movesInLine(self, directions: tuple[Coordinate, ...], limitLength: bool = False) -> list[Move]:
        """Return list of all moves available in directions given as a list of tuples of length 2 with values of -1, 0, or 1"""
        if self.pos is None:
            raise RuntimeError("Piece does not have position")
        moves: list[Move] = []
        for dr, dc in directions:
            row = self.pos[0]
            col = self.pos[1]
            currentMove = [self.pos]
            while True:
                row += dr
                col += dc
                currentMove.append((row,col))
                if self._addIfValid(Move(currentMove.copy()),moves) == False:
                    break
                if limitLength: # limit move to one space in every direction in case of King
                    break
        return moves
    
    def getMoves(self) -> list[Move]:
        """Call getMoves in Piece subclass instead"""
        raise NotImplementedError
    
    def copy(self, newBoard: "Game") -> "Piece":
        """Return a copy of self on newBoard"""
        new = type(self)(self.color)
        new._board = self._board
        new.pos = self.pos
        new.hasMoved = self.hasMoved
        return new
    
    def __repr__(self) -> str:
        """Return string representation of Piece for debugging"""
        return f"{type(self).__name__}({self.color},{self.pos})"

class King(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        if self._board is None:
            raise RuntimeError("Piece not assigned to board")
        if self.pos is None:
            raise RuntimeError("Piece does not have position")
        moves = self._movesInLine(self.ALL_DIRECTIONS,limitLength=True)
        if not self.hasMoved: # add castling moves
            row = self.pos[0]
            leftCorner = self._board.getSpace((row,0))
            rightCorner = self._board.getSpace((row,7))
            if isinstance(leftCorner,Rook) and not leftCorner.hasMoved: # queenside castle
                queenside = Move([(row,4),(row,3),(row,1),(row,2)], castle = "queenside") # include (row,1) to ensure that all spaces between the rook and king are empty, even if not passed through by King
                self._addIfValid(queenside,moves)
            if isinstance(rightCorner,Rook) and not rightCorner.hasMoved: # kingside castle
                kingside = Move([(row,4),(row,5),(row,6)], castle = "kingside")
                self._addIfValid(kingside,moves)
        return moves

    def __str__(self) -> str:
        return 'K' if self.color == 'white' else 'k'
    
class Queen(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        return self._movesInLine(self.ALL_DIRECTIONS)
            
    def __str__(self) -> str:
        """Return string representation of Queen for text board"""
        return 'Q' if self.color == 'white' else 'q'
    
class Bishop(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        return self._movesInLine(self.DIAGONAL_DIRECTIONS)
    
    def __str__(self) -> str:
        """Return string representation of Bishop for text board"""
        return 'B' if self.color == 'white' else 'b'
    
class Knight(Piece):

    L_DIRECTIONS = ((-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(-1,-2),(1,2),(1,-2))

    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        if self.pos is None:
            raise RuntimeError("Piece does not have position")
        moves: list[Move] = []
        row = self.pos[0]
        col = self.pos[1]
        for dr, dc in self.L_DIRECTIONS:
            candidate = Move([self.pos,(row+dr,col+dc)])
            self._addIfValid(candidate,moves)
        return moves
    
    def __str__(self) -> str:
        """Return string representation of King for text board"""
        return 'N' if self.color == 'white' else 'n'
    
class Rook(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        return self._movesInLine(self.CARDINAL_DIRECTIONS)
    
    def __str__(self) -> str:
        """Return string representation of Rook for text board"""
        return 'R' if self.color == 'white' else 'r'
    
class Pawn(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        if self.pos is None:
            raise RuntimeError("Piece does not have position")
        moves: list[Move] = []
        row = self.pos[0]
        col = self.pos[1]
        dr = -1 if self.color == 'white' else 1

        candidate = Move([self.pos, (row + dr, col)]) # single move
        self._addIfValid(candidate, moves, allowCapture = False)

        if not self.hasMoved: # double move
            candidate = Move([self.pos, (row + dr, col), (row + 2 * dr, col)], doublePawn = self.color)
            self._addIfValid(candidate, moves, allowCapture = False)

        endPos = (row + dr, col + 1)
        enPassant = self._enPassant(endPos)
        if self._hasPiece(endPos) or enPassant: # capture to right diagonal
            candidate = Move([self.pos, endPos], enPassant=enPassant)
            self._addIfValid(candidate, moves)

        endPos = (row + dr, col - 1)
        enPassant = self._enPassant(endPos)
        if self._hasPiece(endPos) or enPassant: # capture to left diagonal
            candidate = Move([self.pos, endPos], enPassant=enPassant)
            self._addIfValid(candidate, moves)
        
        return moves
    
    def _enPassant(self, pos: Coordinate) -> bool:
        """Return True if moving to pos is a valid move by en passant"""
        if self._board is None:
            raise RuntimeError("Piece not assigned to board")
        history = self._board.moveHistory
        if len(history) == 0:
            return False
        lastMove = history[-1]
        return lastMove.doublePawn == self._oppositeColor() and lastMove._spaces[1] == pos

    def __str__(self) -> str:
        """Return string representation of Pawn for text board"""
        return 'P' if self.color == 'white' else 'p'