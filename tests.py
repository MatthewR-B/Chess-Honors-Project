import unittest
import game as g
import pieces as p

class TestGame(unittest.TestCase):

    def assertPiece(self, piece: p.Piece, pieceType: type, color: str, pos: p.Coordinate, hasMoved: bool) -> None:
        """Assert that piece has correct type, color, pos, and hasMoved attributes"""
        isinstance(piece,pieceType)
        self.assertEqual(color, piece.color)
        self.assertEqual(pos, piece.pos)
        self.assertEqual(hasMoved, piece.hasMoved)

    def testInit(self) -> None:
        """Test __init__ method"""
        game = g.Game()
        self.assertEqual(8, len(game.board))
        self.assertEqual(8, len(game.board[0]))
        pieceList = [p.Rook, p.Knight, p.Bishop, p.Queen, p.King, p.Bishop, p.Knight, p.Rook]
        for col in range(8):
            self.assertPiece(game.getSpace((0,col)), pieceList[col], "black", (0,col), False)
            self.assertPiece(game.getSpace((1,col)), p.Pawn, "black", (1,col), False)
            self.assertPiece(game.getSpace((6,col)), p.Pawn, "white", (6,col), False)
            self.assertPiece(game.getSpace((7,col)), pieceList[col], "white", (7,col), False)
    
    def testMove(self) -> None:
        pass
# class TestPieceFactory(unittest.TestCase):
#     def setUp(self, pieceType):
#         self.pieceType = pieceType
    
#     def 

if __name__ == "__main__":
    unittest.main()