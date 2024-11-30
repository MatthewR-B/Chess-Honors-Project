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
        self.path = [(0,0),(0,1),(0,2)]
        self.mv1 = p.Move(self.path)
        self.mv2 = p.Move(self.path, castle = "kingside", doublePawn = "black", enPassant=True)

    def testInit(self):
        """Test attributes assigned in __init__ method"""
        self.assertEqual("", self.mv1.castle) 
        self.assertEqual("", self.mv1.doublePawn)
        self.assertEqual(False, self.mv1.enPassant)
        self.assertEqual("kingside", self.mv2.castle)
        self.assertEqual("black", self.mv2.doublePawn)
        self.assertEqual(True, self.mv2.enPassant)
        self.assertEqual(self.path, self.mv1.spaces)
        self.assertEqual(self.path, self.mv2.spaces)
    
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
        """Place multiple pieces onto board [defaults to self.board] and set turn [defaults to white]"""
        if board is None:
            board = self.board
        for i in range(len(pieces)):
            board.setSpace(pieces[i], spaces[i])

    def assertMoves(self, piece: p.Piece, expectedMoveEnds: list[p.Coordinate]):
        """Assert that the end spaces of available moves of piece are the same as expected"""
        assert piece._board is not None
        piece._board.turn = piece.color
        moveEnds = [m.endPos() for m in piece.getMoves()]
        self.assertCountEqual(expectedMoveEnds, moveEnds) # type: ignore

    def move(self, spaces: list[p.Coordinate], board: Optional[g.Game] = None, castle: str = "", doublePawn: str = "", enPassant: bool = False):
        """Execute move through spaces on board [defaults to self.board]"""
        if board is None:
            board = self.board
        piece = board.getSpace(spaces[0])
        assert isinstance(piece, p.Piece)
        board.turn = piece.color
        mv = p.Move(spaces, castle=castle, doublePawn=doublePawn, enPassant=enPassant)
        board.move(mv)

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
        """Test getMoves with other pieces in the way"""
        p1 = p.Rook("white")
        p2 = p.Bishop("white")
        p3 = p.Pawn("black")
        self.placePieces([p1,p2,p3],[(5,5),(2,5),(5,3)])
        expected = [(5,3),(5,4),(5,6),(5,7),(4,5),(3,5),(6,5),(7,5)]
        self.assertMoves(p1, expected)
    
    def testGetMovesPinned(self):
        """Test getMoves when some moves result in check. This test not needed for all Pieces since check detection functions the same"""
        p1 = p.Rook("white")
        p2 = p.King("white")
        p3 = p.Queen("black")
        self.placePieces([p1,p2,p3],[(5,2),(6,2),(3,2)], self.checkBoard)
        expected = [(4,2),(3,2)]
        self.assertMoves(p1, expected)

    def testGetMovesCheck(self):
        """Test getMoves when only one move gets out of check. This test not needed for all Pieces since check detection functions the same"""
        p1 = p.Rook("white")
        p2 = p.King("white")
        p3 = p.Queen("black")
        self.placePieces([p1,p2,p3],[(3,4),(6,2),(3,2)], self.checkBoard)
        expected = [(3,2)]
        self.assertMoves(p1, expected)

class TestKnight(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Knight)

    def testGetMovesEmpty(self):
        """Test getMoves on empty board"""
        p1 = p.Knight("black")
        self.board.setSpace(p1, (4,4))
        expected = [(2,3),(3,2),(2,5),(3,6),(5,6),(6,5),(6,3),(5,2)]
        self.assertMoves(p1, expected)

    def testGetMovesEmptyEdge(self):
        """Test getMoves with knight near the edge of the board"""
        p1 = p.Knight("black")
        self.board.setSpace(p1, (1,1))
        expected = [(0,3),(2,3),(3,0),(3,2)]
        self.assertMoves(p1, expected)

    def testGetMovesObstacles(self):
        """Test getMoves with other pieces in the way"""
        p1 = p.Knight("black")
        p2 = p.Bishop("white")
        p3 = p.Pawn("black")
        p4 = p.Knight("black")
        p5 = p.Pawn("white")
        self.placePieces([p1,p2,p3,p4,p5],[(4,4),(2,3),(4,2),(5,6),(4,5)])
        expected = [(2,3),(3,2),(2,5),(3,6),(6,5),(6,3),(5,2)]
        self.assertMoves(p1, expected)

class TestBishop(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Bishop)

    def testGetMovesEmpty(self):
        """Test getMoves on empty board"""
        p1 = p.Bishop("white")
        self.board.setSpace(p1, (1,5))
        expected = [(0,4),(0,6),(2,4),(3,3),(4,2),(5,1),(6,0),(2,6),(3,7)]
        self.assertMoves(p1, expected)

    def testGetMovesObstacles(self):
        """Test getMoves with other pieces in the way"""
        p1 = p.Bishop("white")
        p2 = p.Knight("black")
        p3 = p.Pawn("white")
        p4 = p.Queen("black")
        self.placePieces([p1,p2,p3,p4],[(2,2),(1,3),(4,4),(0,0)])
        expected = [(0,0),(1,1),(1,3),(3,1),(4,0),(3,3)]
        self.assertMoves(p1, expected)

class TestQueen(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Queen)

    def testGetMovesEmpty(self):
        """Test getMoves on empty board"""
        p1 = p.Queen("black")
        self.board.setSpace(p1, (1,5))
        expected = [(0,4),(0,6),(2,4),(3,3),(4,2),(5,1),(6,0),(2,6),(3,7),(0,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(1,0),(1,1),(1,2),(1,3),(1,4),(1,6),(1,7)]
        self.assertMoves(p1, expected)

    def testGetMovesObstacles(self):
        """Test getMoves with other pieces in the way"""
        p1 = p.Bishop("white")
        p2 = p.Knight("black")
        p3 = p.Pawn("white")
        p4 = p.Queen("black")
        self.placePieces([p1,p2,p3,p4],[(2,2),(1,3),(4,4),(0,0)])
        expected = [(0,0),(1,1),(1,3),(3,1),(4,0),(3,3)]
        self.assertMoves(p1, expected)

class TestKing(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.King)

    def testGetMovesEmpty(self):
        """Test getMoves on empty board"""
        p1 = p.King("white")
        self.board.setSpace(p1, (4,6))
        expected = [(4,7),(5,7),(5,6),(5,5),(4,5),(3,5),(3,6),(3,7)]
        self.assertMoves(p1, expected)

    def testGetMovesObstacles(self):
        """Test getMoves with other pieces in the way"""
        p1 = p.King("black")
        p2 = p.Rook("black")
        p3 = p.Bishop("black")
        p4 = p.Knight("white")
        self.placePieces([p1,p2,p3,p4],[(6,2),(7,3),(5,3),(6,1)])
        expected = [(6,3),(7,2),(7,1),(6,1),(5,1),(5,2)]
        self.assertMoves(p1, expected)

    def testGetMovesCheck(self):
        """Test getMoves when some moves result in check"""
        p1 = p.King("black")
        p2 = p.Pawn("white")
        p3 = p.Queen("white")
        self.placePieces([p1,p2,p3],[(4,4),(4,3),(6,5)], self.checkBoard)
        expected = [(3,3),(5,3)]
        self.assertMoves(p1, expected)

    def testGetMovesCastle(self):
        """Test getMoves when castle available"""
        p1 = p.King("white")
        p2 = p.Rook("white")
        p3 = p.Rook("white")
        self.placePieces([p1,p2,p3],[(7,4),(7,7),(7,0)])
        expected = [(7,3),(6,3),(6,4),(6,5),(7,5),(7,6),(7,2)]
        self.assertMoves(p1, expected)
        # displace rook
        self.move([(7,7),(6,7)])
        self.move([(6,7),(7,7)])
        expected.remove((7,6))
        self.assertMoves(p1, expected)
        # displace king
        self.move([(7,0),(6,0)])
        self.move([(6,0),(7,0)])
        expected.remove((7,2))
        self.assertMoves(p1, expected)
    
    def testGetMovesCastleObstacles(self):
        """Test getMoves when castle blocked by other pieces"""
        p1 = p.King("black")
        p2 = p.Rook("black")
        p3 = p.Rook("black")
        p4 = p.Queen("black")
        self.placePieces([p1,p2,p3,p4],[(0,4),(0,7),(0,0),(0,5)])
        expected = [(0,3),(1,3),(1,4),(1,5),(0,2)]
        self.assertMoves(p1, expected)
        # move queen but still blocking kingside
        self.move([(0,5),(0,6)])
        expected.append((0,5))
        self.assertMoves(p1, expected)
        # move queen out of the way
        self.move([(0,6),(1,6)])
        expected.append((0,6))
        self.assertMoves(p1, expected)
        # move queen in the way of queenside
        self.move([(1,6),(0,3)])
        expected.remove((0,3))
        expected.remove((0,2))
        self.assertMoves(p1,expected)
        # move queen but still blocking queenside
        self.move([(0,3),(0,2)])
        expected.append((0,3))
        self.assertMoves(p1, expected)
        # move queen but still blocking queenside
        self.move([(0,2),(0,1)])
        self.assertMoves(p1, expected)
    
    def testGetMovesCastleCheck(self):
        """Test getMoves when castle blocked by check"""
        p1 = p.King("black")
        p2 = p.Rook("black")
        p3 = p.Rook("black")
        p4 = p.Rook("white")
        self.placePieces([p1,p2,p3,p4],[(0,4),(0,7),(0,0),(7,6)], board=self.checkBoard)
        expected = [(0,3),(1,3),(1,4),(1,5),(0,5),(0,2)]
        self.assertMoves(p1, expected)
        # move rook but still threaten kingside
        self.move([(7,6),(7,5)], self.checkBoard)
        expected.remove((0,5))
        expected.remove((1,5))
        self.assertMoves(p1, expected)
        # move rook to threaten king
        self.move([(7,5),(7,4)], self.checkBoard)
        expected.append((0,5))
        expected.append((1,5))
        expected.remove((1,4))
        expected.remove((0,2))
        self.assertMoves(p1, expected)
        # move rook out of the way of kingside and threaten queenside
        self.move([(7,4),(7,3)], self.checkBoard)
        expected.append((1,4))
        expected.append((0,6))
        expected.remove((0,3))
        expected.remove((1,3))
        self.assertMoves(p1, expected)
        # move rook but still threatening queenside
        self.move([(7,3),(7,2)], self.checkBoard)
        expected.append((0,3))
        expected.append((1,3))
        self.assertMoves(p1, expected)
        # move rook out of the way to second column
        self.move([(7,2),(7,1)], self.checkBoard)
        expected.append((0,2))
        self.assertMoves(p1, expected)

class TestPawn(TestPieceFactory, unittest.TestCase):
    def setUp(self):
        super().setUp(p.Pawn)
    
    def testGetMovesEmpty(self):
        """Test getMoves on a pawn of each color on an otherwise empty board"""
        p1 = p.Pawn("white")
        p2 = p.Pawn("black")
        self.placePieces([p1,p2],[(6,5),(1,2)])
        expected1 = [(5,5),(4,5)]
        expected2 = [(2,2),(3,2)]
        self.assertMoves(p1, expected1)
        self.assertMoves(p2, expected2)
        # move pawns away from starting positions
        self.move([(6,5),(5,5)])
        self.move([(1,2),(2,2)])
        expected1.remove((5,5))
        expected2.remove((2,2))
        self.assertMoves(p1, expected1)
        self.assertMoves(p2, expected2)
    
    def testGetMovesObstacles(self):
        """Test getMoves with other pieces in the way"""
        p1 = p.Pawn("white")
        p2 = p.Pawn("black")
        p3 = p.Knight("black")
        self.placePieces([p1,p2,p3],[(6,4),(4,5),(5,4)])
        expected1 = []
        self.assertMoves(p1, expected1)
        self.move([(4,5),(5,5)])
        expected1 = [(5,5)]
        expected2 = [(6,4),(6,5)]
        self.assertMoves(p1, expected1)
        self.assertMoves(p2, expected2)

    def testGetMovesEnPassant(self):
        """Test getMoves when en passant available"""
        p1 = p.Pawn("white")
        p2 = p.Pawn("black")
        self.placePieces([p1,p2],[(4,0),(1,1)])
        self.move([(4,0),(3,0)])
        expected = [(2,0)]
        self.assertMoves(p1, expected)
        self.move([(1,1),(2,1),(3,1)], doublePawn="black")
        expected.append((2,1))
        self.assertMoves(p1, expected)

if __name__ == "__main__":
    unittest.main()