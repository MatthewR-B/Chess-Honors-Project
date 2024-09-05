# mypy: disable-error-code="call-overload"
from pieces import *
class Game:
    def __init__(self) -> None:
        self.board = [[None]*8 for i in range(8)]
        pieceList = [Rook,Knight,Bishop,King,Queen,Bishop,Knight,Rook]
        col = 0
        for piece in pieceList:
            self.board[0][col] = piece(self.board,'black',(0,col))
            self.board[1][col] = Pawn(self.board,'black',(1,col))
            self.board[6][col] = Pawn(self.board,'white',(6,col))
            self.board[7][7-col] = piece(self.board,'white',(7,7-col))
            col += 1
    
    def __str__(self) -> str:
        boardStr = ""
        for row in self.board:
            for piece in row:
                boardStr += ('-' if piece == None else piece.__str__()) + ' '
            boardStr += "\n"
        return boardStr

    def move(self, pos1: tuple[int,int], pos2: tuple[int,int]) -> None:
        piece = self.board[pos1[0]][pos1[1]]
        piece.location = pos2
        self.board[pos2[0]][pos2[1]] = piece
        self.board[pos1[0]][pos1[1]] = None
        # Add move logging here
    
if __name__ == "__main__":
    g = Game()
    print(g.board[0][3].moves())