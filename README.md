# CSE 2050 Honors Project - Matthew Reed-Brown

## Overview
The project fully implements a game of chess for two human players in Python. It knows for the movement of each piece, and only allows valid moves according to the rules of chess, accounting for situations like castling, en passant, pawn promotion, and check. Users play the game through a GUI made with the PyGame library.

### Deliverables/Milestones:
- 10/1 or earlier:
Have functioning GUI and move logic, excluding check and checkmate.
- 10/25 or earlier:
Submit prototype of game, functioning well enough to find playtesters and search for bugs.
- 11/29 or earlier:
Submit final project with documentation and reflection.

## Code Structure and Algorithms

The code is split between three files:
1. main.py - contains the main game loop for rendering with PyGame
2. pieces.py - contains Move and Piece classes which can return a list of possible moves of any given piece on the board
3. game.py - contains Game class which handles the board, piece movement, check detection, and game end conditions

When a user clicks on a space, there is a PyGame event which calls the click method in Game. If a piece is not already selected, it will call the getMoves method of the piece in the space the user clicked to find where that piece could move, then highlight all spaces represented by those moves by darkening the colors of those spaces. If the user clicks on a highlighted space, it will execute the move using the move method in Game, which moves the piece and handles any special cases like removing a pawn taken by en passant or moving a rook when castling. 

Piece has a subclass for each type of piece in chess. Each one has its own getMoves method that accounts for its unique movement. Bishop, Rook, and Queen all use a helper method inherited from Piece since their movement involves going in straight lines until they hit another piece or the edge of the board. King uses the same helper method with a parameter to limit its movement to one space in each direction, then adds on available castling moves. Pawns consider the space in front of them, the direction of which depends on the color of the piece, the space two in front of them if it has not yet moved, and the spaces diagonally in front of them if there is a piece of the opposing color present, or if the last move was a double move by an opposing pawn that can be taken by *en passant*.

Each potential move is represented by a Move object which stores the spaces through which it travels and whether it is a special case for the Game.move method to handle, including en passant, double pawn moves, and castling. getMoves passes each move candidate to another helper method that checks whether it remains within bounds of the board, is not blocked by any other pieces, is not a castle move that passes through a space threatened by an opposing piece, and does not cause an illegal boardstate by putting oneself in check. It returns the remaining list of moves for the player to select.


## Challenges and Lessons:

I had to alter a lot of aspects of my original outline of the code structure. For example, I changed the Move class to store the position of every space a piece would move through, rather than just the first and last. This was necessary to check if there are pieces in the way of the move, or if a King would move through a threatened space while castling. To account for a Knight's movement, I only record the first and last parts of the move so it does not check for collision in the middle, allowing for the piece's signature "jumping" move.

I also changed check detection to work by creating a copy of the current board so I could reuse the existing getMoves methods of each Piece, but ran into infinite recursion issues as those getMoves methods were also checking whether they themselves would result in check. I implemented a base case by creating an attribute of Game checkEnabled that toggles further check detection off.

Another challenge came with type checking. I wanted to include type annotations to make autocompletion and debugging easier. I learned a lot about how tuples are handled differently than other collections, and how annotating an attribute as Optional requires isinstance checks later when using the attribute in a situation where None would result in an error. I also had an issue with circular imports as I wanted to annotate using the Game and Piece types in both files. [A Stack Overflow post](https://stackoverflow.com/a/39757388) pointed me in the direction of using the TYPE_CHECKING constant from typing.

One of the largest tasks for me was the test cases. I coded a large part of the project in the beginning of the semester, before learning about unittest. As a result, I had to write a lot of test cases retroactively, which made spotting errors very difficult at times. I now understand the importance of test-driven development, and will definitely make use of it in my future projects.

---
### Assets Source: [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces)