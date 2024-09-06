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
    cardinalDirections = ((1,0),(0,-1),(-1,0),(0,1))
    diagonalDirections = ((1,1),(1,-1),(-1,-1),(-1,1))
    allDirecitons = cardinalDirections + diagonalDirections

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
    
    def movesInLine(self, directions: list[tuple[int,int]], limitLength: bool = False) -> list[Move]:
        """Return list of all moves available in directions given as a list of tuples of length 2 with values of -1, 0, or 1"""
        moves = []
        for dr, dc in directions:
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
                    if limitLength: # limit move to one space in every direction in case of King
                        break
        return moves
        


class King(Piece):
    def getMoves(self) -> list[Move]:
        moves = self.movesInLine(self.allDirecitons,limitLength=True)
        if not self.hasMoved: # add castling moves
            row = self.pos[0]
            leftCorner = self.board.getSpace((row,0))
            rightCorner = self.board.getSpace((row,7))
            if isinstance(leftCorner,Rook) and not leftCorner.hasMoved: # queenside castle
                queenside = Move([(row,4),(row,3),(row,1),(row,2)], castle = True) # include (row,1) to ensure that all spaces between the rook and king are empty, even if not passed through by King
                if self.isValid(queenside): moves.append(queenside) 
            if isinstance(rightCorner,Rook) and not rightCorner.hasMoved: # kingside castle
                kingside = Move([(row,4),(row,5),(row,6)], castle = True)
                if self.isValid(kingside): moves.append(kingside) 
        return moves

    def __str__(self) -> str:
        return 'K' if self.color == 'white' else 'k'
    
class Queen(Piece):
    def getMoves(self) -> list[Move]:
        return self.movesInLine(self.allDirecitons)
            
    def __str__(self) -> str:
        return 'Q' if self.color == 'white' else 'q'
    
class Bishop(Piece):
    def getMoves(self) -> list[Move]:
        return self.movesInLine(self.diagonalDirections)
    
    def __str__(self) -> str:
        return 'B' if self.color == 'white' else 'b'
    
class Knight(Piece):
    def getMoves(self) -> list[Move]:
        moves = []
        row = self.pos[0]
        col = self.pos[1]
        for dr in (-2,-1,1,2):
            for dc in (-2,-1,1,2):
                candidate = Move((row,col),(row+dr,col+dc))
                if self.isValid(candidate): moves.append(candidate)
        return moves
    
    def __str__(self) -> str:
        return 'N' if self.color == 'white' else 'n'
    
class Rook(Piece):
    def getMoves(self) -> list[Move]:
        return self.movesInLine(self.cardinalDirections)
    
    def __str__(self) -> str:
        return 'R' if self.color == 'white' else 'r'
    
class Pawn(Piece):
    def __str__(self) -> str:
        return 'P' if self.color == 'white' else 'p'