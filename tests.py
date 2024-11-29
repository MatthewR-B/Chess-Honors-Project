import unittest
import game as g
import pieces as p
from typing import Optional, Any

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = g.Game()
        self.empty = g.Game(populate=False, checkEnabled=False)

    def assertPiece(self, piece: Optional[p.Piece], pieceType: type, color: str, pos: p.Coordinate, hasMoved: bool):
        """Assert that piece has correct type, color, pos, and hasMoved attributes"""
        assert piece is not None # for type checking
        self.assertIsInstance(piece,pieceType)
        self.assertEqual(color, piece.color)
        self.assertEqual(pos, piece.pos)
        self.assertEqual(hasMoved, piece.hasMoved)

    def testInit(self):
        """Test __init__ and getSpace method"""
        self.assertEqual(0, len(self.game.moveHistory))
        self.assertEqual(0, len(self.game.visibleMoves))
        self.assertEqual("white", self.game.turn)
        pieceList = [p.Rook, p.Knight, p.Bishop, p.Queen, p.King, p.Bishop, p.Knight, p.Rook]
        for col in range(8):
            self.assertPiece(self.game.getSpace((0,col)), pieceList[col], "black", (0,col), False)
            self.assertPiece(self.game.getSpace((1,col)), p.Pawn, "black", (1,col), False)
            self.assertPiece(self.game.getSpace((6,col)), p.Pawn, "white", (6,col), False)
            self.assertPiece(self.game.getSpace((7,col)), pieceList[col], "white", (7,col), False)    

    def testSetSpace(self):
        """Test setSpace method"""
        p1 = p.Rook("black")
        for r in range(8):
            for c in range(8):
                self.empty.setSpace(p1,(r,c))
                self.assertIs(p1, self.empty.getSpace((r,c)))
                self.empty.setSpace(None,(r,c))
                self.assertIs(None, self.empty.getSpace((r,c)))

    def testMoveNormal(self):
        """Test move method"""
        mv = p.Move([(0,0),(0,1)])
        with self.assertRaises(RuntimeError):
            self.empty.move(mv)
        
        rook = p.Rook("black",)
        self.empty.setSpace(rook, (0,0))
        self.empty.move(mv)
        self.assertIs(None, self.empty.getSpace((0,0)))
        self.assertIs(rook, self.empty.getSpace((0,1)))
        self.assertTrue(rook.hasMoved)
        self.assertEqual(1, len(self.empty.moveHistory))
        self.assertEqual((0,1), rook.pos)
        self.assertEqual("black", self.empty.turn)

    def testMoveCastleKingside(self):
        """Test kingside castle with move method"""
        king = p.King("white")
        rook = p.Rook("white")
        self.empty.setSpace(king,(7,4))
        self.empty.setSpace(rook, (7,7))
        mv = p.Move([(7,4),(7,5),(7,6)], castle="kingside")
        self.empty.move(mv)
        self.assertTrue(king.hasMoved)
        self.assertTrue(rook.hasMoved)
        self.assertIs(rook, self.empty.getSpace((7,5)))
        self.assertIs(king, self.empty.getSpace((7,6)))
        self.assertIs(None, self.empty.getSpace((7,7)))
        self.assertEqual((7,5), rook.pos)
        self.assertEqual((7,6), king.pos)
        self.assertEqual("black", self.empty.turn)

    def testMoveCastleQueenside(self):
        """Test queenside castle with move method"""
        king = p.King("white")
        rook = p.Rook("white")
        self.empty.setSpace(king,(7,4))
        self.empty.setSpace(rook, (7,0))
        mv = p.Move([(7,4),(7,3),(7,2)], castle="queenside")
        self.empty.move(mv)
        self.assertTrue(king.hasMoved)
        self.assertTrue(rook.hasMoved)
        self.assertIs(rook, self.empty.getSpace((7,3)))
        self.assertIs(king, self.empty.getSpace((7,2)))
        self.assertIs(None, self.empty.getSpace((7,0)))
        self.assertEqual((7,3), rook.pos)
        self.assertEqual((7,2), king.pos)
        self.assertEqual("black", self.empty.turn)

    def testMoveEnPassant(self):
        """Test en passant with move method"""
        pawn1 = p.Pawn("black")
        pawn2 = p.Pawn("white")
        self.empty.setSpace(pawn1, (1,0))
        self.empty.setSpace(pawn2, (3,1))
        mv1 = p.Move([(1,0),(2,0),(3,0)], doublePawn="")
        mv2 = p.Move([(3,1),(2,0)], enPassant=True)
        self.empty.move(mv1)
        self.empty.move(mv2)
        self.assertIs(pawn2, self.empty.getSpace((2,0)))
        self.assertIs(None, self.empty.getSpace((3,0)))
        self.assertEqual((2,0), pawn2.pos)
        self.assertEqual("white", self.empty.turn)

    def testMovePromotion(self):
        """Test pawn promotion with move method"""
        pawn = p.Pawn("white")
        self.empty.setSpace(pawn, (1,0))
        mv = p.Move([(1,0),(0,0)])
        self.empty.move(mv)
        self.assertIsInstance(self.empty.getSpace((0,0)), p.Queen)

    def testClick(self):
        """Test click method"""
        M = self.game.visibleMoves
        H = self.game.moveHistory
        click = self.game.click
        click((2,0)) # click on empty space
        self.assertEqual(0, len(M))
        self.assertEqual(0, len(H))
        click((0,0)) # click on piece with no moves
        self.assertEqual(0, len(M))
        self.assertEqual(0, len(H))
        click((6,0)) # click on pawn with two moves
        self.assertEqual(2, len(M))
        self.assertEqual(0, len(H))
        click((1,1)) # click away from pawn
        self.assertEqual(0, len(M))
        self.assertEqual(0, len(H))
        click((6,0)) # click on pawn with two moves
        click((5,0)) # click on available move
        self.assertEqual(0, len(M))
        self.assertEqual(1, len(H))
        click((6,0)) # click on pawn with moves but not on turn
        self.assertEqual(0, len(M))
        self.assertEqual(1, len(H))

class TestMove(unittest.TestCase):

    def setUp(self):
        """Set up a move that is a castle and double pawn (not possible in a real game) and a Move that is neither"""
        path = [(0,0),(0,1),(0,2)]
        self.mv1 = p.Move(path)
        self.mv2 = p.Move(path, castle = "kingside", doublePawn = "black", enPassant=True)

    def testInit(self):
        """Test attributes assigned in __init__ method"""
        self.assertEqual("", self.mv1.castle) 
        self.assertEqual("", self.mv1.doublePawn)
        self.assertEqual(False, self.mv1.enPassant)
        self.assertEqual("kingside", self.mv2.castle)
        self.assertEqual("black", self.mv2.doublePawn)
        self.assertEqual(True, self.mv2.enPassant)
    
    def testGetters(self):
        """Test startPos and endPos methods"""
        self.assertEqual((0,0), self.mv1.startPos())
        self.assertEqual((0,2), self.mv1.endPos())
    
    def testRepr(self):
        """Test __repr__ method"""
        self.assertEqual("Move((0, 0) to (0, 2))", repr(self.mv1))
        self.assertEqual("Move((0, 0) to (0, 2), castle=kingside, doublePawn=black, enPassant=True)", repr(self.mv2))

class TestPieceFactory:

    def setUp(self, pieceType: type[p.Piece]):
        """Set up tests with empty boards and store the type of piece"""
        self.pieceType = pieceType
        self.board = g.Game(populate=False, checkEnabled=False)
        self.checkBoard = g.Game(populate=False, checkEnabled=True)

    def placePieces(self, pieces: list[p.Piece], spaces: list[p.Coordinate], board: Optional[g.Game] = None):
        """Place multiple pieces onto the board"""
        if board is None:
            board = self.board
        for i in range(len(pieces)):
            board.setSpace(pieces[i], spaces[i])

    def assertMoves(self, piece: p.Piece, expectedMoveEnds: list[p.Coordinate]):
        """Assert that the end spaces of available moves of piece are the same as expected"""
        moveEnds = [m.endPos() for m in piece.getMoves()]
        self.assertCountEqual(expectedMoveEnds, moveEnds) # type: ignore

    def testCopy(self):
        """Test copy method"""
        p1 = self.pieceType("black")
        self.board.setSpace(p1, (0,0))
        copy = p1.copy(g.Game(populate=False))
        self.assertIsNot(p1, copy)
        self.assertEqual(p1.pos, copy.pos)
        self.assertEqual(p1.color, copy.color)
        self.assertEqual(p1.hasMoved, copy.hasMoved)

    def testRepr(self):
        """Test __repr__ method"""
        piece = self.pieceType("white")
        self.board.setSpace(piece,(0,0))
        self.assertEqual(f"{self.pieceType.__name__}(white,(0, 0))", repr(piece))

class TestRook(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Rook)

    def testGetMovesEmpty(self):
        """Test getMoves on empty board"""
        p1 = p.Rook("white")
        self.board.setSpace(p1, (2,3))
        expected = [(0,3),(1,3),(3,3),(4,3),(5,3),(6,3),(7,3),(2,0),(2,1),(2,2),(2,4),(2,5),(2,6),(2,7)]
        self.assertMoves(p1, expected)

    def testGetMovesObstacles(self):
        """Test getMoves with other pieces"""
        p1 = p.Rook("white")
        p2 = p.Bishop("white")
        p3 = p.Pawn("black")
        self.placePieces([p1,p2,p3],[(5,5),(2,5),(5,3)])
        expected = [(5,3),(5,4),(5,6),(5,7),(4,5),(3,5),(6,5),(7,5)]
        self.assertMoves(p1, expected)
    
    def testGetMovesPinned(self):
        """Test getMoves when some moves result in check"""
        p1 = p.Rook("white")
        p2 = p.King("white")
        p3 = p.Queen("black")
        self.placePieces([p1,p2,p3],[(5,2),(6,2),(3,2)], self.checkBoard)
        expected = [(4,2),(3,2)]
        self.assertMoves(p1, expected)

class TestKnight(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Knight)

    

class TestBishop(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Bishop)

class TestQueen(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Queen)

class TestKing(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.King)

class TestPawn(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Pawn)

if __name__ == "__main__":
    unittest.main()