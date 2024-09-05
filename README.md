Matthew Reed-Brown
CSE 2050 Honors Project Plan

Overview:
The project will fully implement a game of chess for two human players in Python. It will know the movement for each piece, and only allow valid moves according to the rules of chess, accounting for more-complex situations like castling, en passant, pawn promotion, and check. It will also have a GUI using the PyGame library.

Deliverables/Milestones:
10/1 or earlier:
Have functioning GUI and move logic, excluding check and checkmate.
10/25 or earlier:
Submit prototype of game, functioning well enough to find playtesters and search for bugs.
11/29 or earlier:
Submit final project with documentation and reflection.

Project Proposal/Plan:
1. Define a Piece class, with attributes including a string for color, a tuple of two integers for location, a boolean to determine if the piece has moved yet, and the board, passed in the constructor for access to the locations of other pieces.
2. Create a board class that uses a 2D list to keep track of pieces. Its constructor populates the list with all the pieces in their starting positions. Empty spaces are represented by the null object. Define a move() method which takes two coordinate pair tuples as parameters, moves a piece from the first location to the second, then updates the location and already-moved attributes of the piece. Record the move in a list of strings using standard chess notation.
3. Define subclasses for each type of piece, including Pawn, Rook, Knight, Bishop, King, and Queen that inherit from Piece, each with a moves() method that returns a list of potential moves in coordinate pairs. It will start with a list of all moves that would be possible according to the movement of that type of the piece, assuming the board is empty. Then, remove any moves that are made invalid by pieces being in the way or having already moved the piece in the case of castling, double pawn move, and en passant.
4. Create a loop that draws and updates the board using PyGame.
Define a check(color,board) method that iterates through the board, running the moves() method on each piece of the opposite of the passed color and returning true if one of those pieces would be able to capture the opposing king.
5. For the click event of each space on the board, if spaces are not already highlighted and the space contains a piece of the color of the current turn, call the moves() method for the piece and highlight the spaces represented by the moves in the list. If there are already highlighted spaces and the user clicks on one of the options, make a copy of the board and run the move() method. Run the check(board) function on the copy to determine if the move would result in an illegal move due to putting oneself in check. If false, assign the copy of the board to the original board.
6. After a move, check for pawn promotion. If a pawn moved to the opposite side of the board, open a selector window where the user can pick the piece with which the pawn will be replaced.
7. Define a checkmate(board) function, which will run at the beginning of a turn. First, run the check(board) method. If true, iterate through each possible move of each piece with color matching the turn. For each move, create a copy of the board, execute the move, and run check(board) on the copy. If no move is found that will remove the player from check, return true and end the game.