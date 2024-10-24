from typing import TypeAlias, TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game

Coordinate: TypeAlias = tuple[int,int]

class Move:
    """Represents the potential movement of a piece from one space to another, storing the coordinates of all spaces through which the piece must travel"""
    def __init__(self, spaces: list[Coordinate], castle: str = "", doublePawn: str = "") -> None:
        self.spaces = spaces
        self.castle = castle
        self.doublePawn = doublePawn

    def startPos(self) -> Coordinate:
        """Get first space in move"""
        return self.spaces[0]
    
    def endPos(self) -> Coordinate:
        """Get final space in move"""
        return self.spaces[-1]

    def __repr__(self) -> str:
        """Return string representation of Move"""
        return f"{self.startPos()} to {self.endPos()} {self.castle}"

class Piece:
    """Parent class for all pieces, storing color, location, and whether the piece has moved yet"""
    cardinalDirections = ((1,0),(0,-1),(-1,0),(0,1))
    diagonalDirections = ((1,1),(1,-1),(-1,-1),(-1,1))
    allDirecitons = cardinalDirections + diagonalDirections

    def __init__(self, board: "Game", color: str, pos: Coordinate) -> None:
        """Initialize Piece with the board, color, and position"""
        self.board = board
        self.color = color
        self.pos = pos
        self.hasMoved = False

    def hasPiece(self, pos: Coordinate) -> bool:
        """Return True if there is a piece at pos"""
        return self.inBounds(Move([pos])) and isinstance(self.board.getSpace(pos),Piece)
    
    def isOppositeColor(self, pos: Coordinate) -> bool:
        """Return True if there is a piece of the opposite color at pos"""
        return self.hasPiece(pos) and self.board.getSpace(pos).color == self.oppositeColor()
    
    def oppositeColor(self):
        """Return the color that is not this piece's color"""
        return "black" if self.color == "white" else "white"

    def addIfValid(self, mv: Move, moves: list[Move], allowCapture: bool = True) -> bool:
        """Apply restrictions on moves that are common to all pieces, including staying on the board, not moving through or onto a blocked space, and not moving into check""" # NEEDS UPDATING
        if self.inBounds(mv) and self.moveFree(mv, allowCapture): # and not self.inCheck(mv)
            moves.append(mv)
            return True
        return False

    def inBounds(self, mv: Move) -> bool:
        """Return True if the last space in mv is on the board"""
        row = mv.endPos()[0]
        col = mv.endPos()[1]
        return row >= 0 and row <= 7 and col >= 0 and col <= 7
    
    def moveFree(self, mv: Move, allowCapture: bool) -> bool: # MOVE TO MOVE CLASS?
        """Return True if the last space in a move is empty or has an piece available to capture, and all other spaces are empty"""
        for loc in mv.spaces[1:-1]: # check if all except first and last space are empty
            if self.hasPiece(loc):
                return False
        lastSpace = mv.endPos()
        captureAvailable = allowCapture and self.isOppositeColor(lastSpace)
        return (not self.hasPiece(lastSpace)) or captureAvailable # check if last space empty or free to be captured
    
    def movesInLine(self, directions: tuple[Coordinate], limitLength: bool = False) -> list[Move]:
        """Return list of all moves available in directions given as a list of tuples of length 2 with values of -1, 0, or 1"""
        moves: list[Move] = []
        for dr, dc in directions:
            row = self.pos[0]
            col = self.pos[1]
            currentMove = [self.pos]
            while True:
                row += dr
                col += dc
                currentMove.append((row,col))
                if self.addIfValid(Move(currentMove.copy()),moves) == False:
                    break
                if limitLength: # limit move to one space in every direction in case of King
                    break
        return moves
    
    def __repr__(self) -> str:
        """Return string representation of Piece for debugging"""
        return f"{type(self).__name__}({self.color}, {self.pos}, {self.hasMoved})"
        
class King(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        moves = self.movesInLine(self.allDirecitons,limitLength=True)
        if not self.hasMoved: # add castling moves
            row = self.pos[0]
            leftCorner = self.board.getSpace((row,0))
            rightCorner = self.board.getSpace((row,7))
            if isinstance(leftCorner,Rook) and not leftCorner.hasMoved: # queenside castle
                queenside = Move([(row,4),(row,3),(row,1),(row,2)], castle = "queenside") # include (row,1) to ensure that all spaces between the rook and king are empty, even if not passed through by King
                self.addIfValid(queenside,moves)
            if isinstance(rightCorner,Rook) and not rightCorner.hasMoved: # kingside castle
                kingside = Move([(row,4),(row,5),(row,6)], castle = "kingside")
                self.addIfValid(kingside,moves)
        return moves

    def __str__(self) -> str:
        return 'K' if self.color == 'white' else 'k'
    
class Queen(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        return self.movesInLine(self.allDirecitons)
            
    def __str__(self) -> str:
        """Return string representation of Queen for text board"""
        return 'Q' if self.color == 'white' else 'q'
    
class Bishop(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        return self.movesInLine(self.diagonalDirections)
    
    def __str__(self) -> str:
        """Return string representation of Bishop for text board"""
        return 'B' if self.color == 'white' else 'b'
    
class Knight(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        moves = []
        row = self.pos[0]
        col = self.pos[1]
        for dr, dc in ((-2,1),(-2,-1),(2,1),(2,-1),(-1,2),(-1,-2),(1,2),(1,-2)):
            candidate = Move([self.pos,(row+dr,col+dc)])
            self.addIfValid(candidate,moves)
        return moves
    
    def __str__(self) -> str:
        """Return string representation of King for text board"""
        return 'N' if self.color == 'white' else 'n'
    
class Rook(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        return self.movesInLine(self.cardinalDirections)
    
    def __str__(self) -> str:
        """Return string representation of Rook for text board"""
        return 'R' if self.color == 'white' else 'r'
    
class Pawn(Piece):
    def getMoves(self) -> list[Move]:
        """Return list of available Moves"""
        moves: list[Move] = []
        row = self.pos[0]
        col = self.pos[1]
        dr = -1 if self.color == 'white' else 1

        candidate = Move([self.pos, (row + dr, col)]) # single move
        self.addIfValid(candidate, moves, allowCapture = False)

        if not self.hasMoved: # double move
            candidate = Move([self.pos, (row + dr, col), (row + 2 * dr, col)], doublePawn = self.color)
            self.addIfValid(candidate, moves, allowCapture = False)

        endPos = (row + dr, col + 1)
        if self.hasPiece(endPos) or self.enPassant(endPos): # capture to right diagonal
            candidate = Move([self.pos, endPos])
            self.addIfValid(candidate,moves)

        endPos = (row + dr, col - 1)
        if self.hasPiece(endPos) or self.enPassant(endPos): # capture to left diagonal
            candidate = Move([self.pos, endPos])
            self.addIfValid(candidate, moves)
        
        return moves
    
    def enPassant(self, pos: Coordinate) -> bool:
        """Return True if moving to pos is a valid move by en passant"""
        history = self.board.moveHistory
        if len(history) == 0:
            return False
        lastMove = history[-1]
        return lastMove.doublePawn == self.oppositeColor() and lastMove.spaces[1] == pos

    def __str__(self) -> str:
        """Return string representation of Pawn for text board"""
        return 'P' if self.color == 'white' else 'p'