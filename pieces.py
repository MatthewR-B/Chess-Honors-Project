class Piece:
    def __init__(self, board, color: str, loc: tuple[int,int]) -> None:
        self.board = board
        self.color = color
        self.loc = loc
        self.hasMoved = False
    
    def filterMoves(self, moves: list[tuple[int,int]]) -> list[tuple[int,int]]:
        """Apply restrictions on moves that are common to all pieces, including staying on the board and not moving through or onto a blocked space"""
        filteredMoves = []
        for move in moves:
            if self.inBounds(move):
                filteredMoves.append(move)
        return filteredMoves

    def inBounds(self, loc: tuple[int]) -> bool:
        return loc[0] >= 0 and loc[0] <= 7 and loc[1] >= 0 and loc[1] <= 7
    
    def locBlocked(self, loc: tuple[int]) -> bool:
        """Return true if loc is occupied by a piece of the same color"""


class King(Piece):
    def moves(self) -> list[tuple[int]]:
        moves = []
        for dy in range(-1,2):
            for dx in (-1,2):
                if dy != 0 or dx != 0:
                    moves.append((self.loc[0] + dy, self.loc[1] + dx))
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