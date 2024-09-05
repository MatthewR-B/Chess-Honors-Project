class Piece:
    def __init__(self, board, color: str, location: tuple[int]) -> None:
        self.board = board
        self.color = color
        self.location = location
        self.hasMoved = False

class King(Piece):
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