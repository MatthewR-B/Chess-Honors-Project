# mypy: disable-error-code="call-overload"
from pieces import *
class Game:
    def __init__(self) -> None:
        self.board = [[None]*8 for i in range(8)]
        pieceList = [Rook,Knight,Bishop,King,Queen,Bishop,Knight,Rook]
        col = 0
        for piece in pieceList:
            self.board[0][col] = piece(self,'black',(0,col))
            self.board[1][col] = Pawn(self,'black',(1,col))
            self.board[6][col] = Pawn(self,'white',(6,col))
            self.board[7][7-col] = piece(self,'white',(7,7-col))
            col += 1
    
    def __str__(self) -> str:
        boardStr = ""
        for row in self.board:
            for piece in row:
                boardStr += ('-' if piece == None else piece.__str__()) + ' '
            boardStr += "\n"
        return boardStr

    def move(self, pos1: tuple[int,int], pos2: tuple[int,int]) -> None: # CHANGE TO TAKE MOVE OBJECT AS INPUT
        piece = self.getSpace(pos1)
        piece.pos = pos2
        self.setSpace(piece,pos2)
        self.setSpace(None,pos1)
        # Add move logging here

    def getSpace(self, pos: tuple[int,int]) -> Piece | None:
        return self.board[pos[0]][pos[1]]

    def setSpace(self, content: Piece | None, pos: tuple[int,int]) -> None:
        self.board[pos[0]][pos[1]] = content

    
if __name__ == "__main__":
    g = Game()
    g.setSpace(None,(0,2))
    for mv in g.board[0][3].getMoves():
        print(mv)