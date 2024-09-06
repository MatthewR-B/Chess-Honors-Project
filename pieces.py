class Move:
    """Represents the potential movement of a piece from one space to another, storing the coordinates of all spaces through which the piece must travel"""
    def __init__(self, spaces: list[tuple[int,int]]) -> None:
        self.spaces = spaces
    
    def endPos(self) -> tuple[int,int]:
        return self.spaces[-1]

class Piece:
    def __init__(self, board, color: str, loc: tuple[int,int]) -> None:
        self.board = board
        self.color = color
        self.loc = loc
        self.hasMoved = False
    
    def filterMoves(self, moves: list[Move]) -> list[Move]:
        """Apply restrictions on moves that are common to all pieces, including staying on the board and not moving through or onto a blocked space"""
        filteredMoves = []
        for candidate in moves:
            if self.inBounds(candidate) and self.moveFree():
                filteredMoves.append(candidate)
        return filteredMoves

    def inBounds(self, mv: Move) -> bool:
        """Return True if the last space of a move is on the board"""
        pos = mv.endPos()
        return pos[0] >= 0 and pos[0] <= 7 and pos[1] >= 0 and pos[1] <= 7
    
    def locBlocked(self, loc: tuple[int]) -> bool:
        """Return true if loc is occupied by a piece of the same color"""


class King(Piece):
    def getMoves(self) -> list[Move]:
        moves = []
        for dy in range(-1,2):
            for dx in (-1,2):
                if dy != 0 or dx != 0:
                    moves.append(Move((self.loc[0] + dy, self.loc[1] + dx)))
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