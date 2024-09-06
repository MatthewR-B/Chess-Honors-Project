class Move:
    """Represents the potential movement of a piece from one space to another, storing the coordinates of all spaces through which the piece must travel"""
    def __init__(self, spaces: list[tuple[int,int]]) -> None:
        self.spaces = spaces
    
    def endPos(self) -> tuple[int,int]:
        """Get final space in move"""
        return self.spaces[-1]

    def __str__(self) -> str:
        return f"{self.spaces[0]} to {self.endPos()}"

class Piece:
    """Parent class for all pieces, storing color, location, and whether the piece has moved yet"""
    def __init__(self, board, color: str, pos: tuple[int,int]) -> None:
        self.board = board
        self.color = color
        self.pos = pos
        self.hasMoved = False
    
    def filterMoves(self, moves: list[Move]) -> list[Move]:
        """Apply restrictions on moves that are common to all pieces, including not moving through or onto a blocked space and not moving into check"""
        filteredMoves = []
        for candidate in moves:
            if self.moveFree(candidate): # ADD CHECK DETECTION
                filteredMoves.append(candidate)
        return filteredMoves

    def inBounds(self, row: int, col: int) -> bool:
        """Return True if the coordinates are on the board"""
        return row >= 0 and row <= 7 and col >= 0 and col <= 7
    
    def moveFree(self, mv: Move) -> bool:
        """Return True if the last space in a move is empty or the opposite color, and all other spaces are empty"""
        for loc in mv.spaces[:-1]: # check if all except last space is empty
            if self.board.getSpace(loc) != None:
                return False
        lastSpaceContent = self.board.getSpace(mv.endPos())
        return lastSpaceContent == None or lastSpaceContent.color == ('black' if self.color == 'white' else 'white') # check if last space empty or free to be captured
        


class King(Piece):
    def getMoves(self) -> list[Move]:
        moves = []
        startRow = self.pos[0]
        startCol = self.pos[1]
        for row in range(startRow-1, startRow+2): # add moves for 8 spaces around piece
            for col in (startCol-1, startCol-2):
                if (row != startRow or col != startCol) and self.inBounds(row, col): # only add move if it end on a different space that is on the board
                    moves.append(Move([(startRow, startCol), (row, col)]))
        # ADD CASTLING
        return self.filterMoves(moves)

    def __str__(self) -> str:
        return 'K' if self.color == 'white' else 'k'
    
class Queen(Piece):
    def __str__(self) -> str:
        return 'Q' if self.color == 'white' else 'q'
    
class Bishop(Piece):
    def __str__(self) -> str:
        return 'B' if self.color == 'white' else 'b'
    
class Knight(Piece):
    def __str__(self) -> str:
        return 'N' if self.color == 'white' else 'n'
    
class Rook(Piece):
    def __str__(self) -> str:
        return 'R' if self.color == 'white' else 'r'
    
class Pawn(Piece):
    def __str__(self) -> str:
        return 'P' if self.color == 'white' else 'p'