class Move:
    """Represents the potential movement of a piece from one space to another, storing the coordinates of all spaces through which the piece must travel"""
    def __init__(self, spaces: list[tuple[int,int]], castle: bool = False) -> None:
        self.spaces = spaces
        self.castle = castle

    def startPos(self) -> tuple[int,int]:
        """Get first space in move"""
        return self.spaces[0]
    
    def endPos(self) -> tuple[int,int]:
        """Get final space in move"""
        return self.spaces[-1]

    def __str__(self) -> str:
        return f"{self.startPos()} to {self.endPos()}{" castle" if self.castle else ""}"

class Piece:
    """Parent class for all pieces, storing color, location, and whether the piece has moved yet"""
    def __init__(self, board, color: str, pos: tuple[int,int]) -> None:
        self.board = board
        self.color = color
        self.pos = pos
        self.hasMoved = False
    
    def isValid(self, mv: Move) -> bool:
        """Apply restrictions on moves that are common to all pieces, including staying on the board, not moving through or onto a blocked space, and not moving into check"""
        return self.inBounds(mv) and self.moveFree(mv)

    def inBounds(self, mv: Move) -> bool:
        """Return True if the last space in mv is on the board"""
        row = mv.endPos()[0]
        col = mv.endPos()[1]
        return row >= 0 and row <= 7 and col >= 0 and col <= 7
    
    def moveFree(self, mv: Move) -> bool:
        """Return True if the last space in a move is empty or the opposite color, and all other spaces are empty"""
        for loc in mv.spaces[1:-1]: # check if all except first and last space are empty
            if self.board.getSpace(loc) != None:
                return False
        lastSpaceContent = self.board.getSpace(mv.endPos())
        return lastSpaceContent == None or lastSpaceContent.color == ('black' if self.color == 'white' else 'white') # check if last space empty or free to be captured
        


class King(Piece):
    def getMoves(self) -> list[Move]:
        moves = []
        row = self.pos[0]
        col = self.pos[1]
        for dr in (-1,0,1): # add moves for 8 spaces around piece
            for dc in (-1,0,1):
                if (dr != 0 or dc != 0): # only add move if it ends on a different space that is on the board
                    candidate = Move([(row, col), (row+dr, col+dc)])
                    if self.isValid(candidate): 
                        moves.append(candidate)
        if not self.hasMoved: # add castling moves
            leftCorner = self.board.getSpace((row,0))
            rightCorner = self.board.getSpace((row,7))
            if isinstance(leftCorner,Rook) and not leftCorner.hasMoved: # queenside castle
                moves.append(Move([(row,4),(row,3),(row,1),(row,2)], castle = True)) # include (row,1) to ensure that all spaces between the rook and king are empty
            if isinstance(rightCorner,Rook) and not rightCorner.hasMoved: # kingside castle
                moves.append(Move([(row,4),(row,5),(row,6)], castle = True))
        return moves

    def __str__(self) -> str:
        return 'K' if self.color == 'white' else 'k'
    
class Queen(Piece):
    def getMoves(self) -> list[Move]:
        moves = []
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr != 0 or dc != 0:
                    row = self.pos[0]
                    col = self.pos[1]
                    currentMove = [(row,col)]
                    while True:
                        row += dr
                        col += dc
                        currentMove.append((row,col))
                        candidate = Move(currentMove.copy())
                        if (self.isValid(candidate)): 
                            moves.append(candidate)
                        else:
                            break
        return moves
            
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