# template from https://www.pg.org/docs/
import pygame as pg
from game import Game
from pieces import Move, Piece
from typing import Optional

SCREENWIDTH = 720
SCREENHEIGHT = 720
COLORLIGHT = (255,255,255)
COLORDARK = (0,170,255)
DARKERMODIFIER = 60

sideLength = int(SCREENHEIGHT/8)
tiles: list[list[pg.Rect]] = [[pg.Rect(col*sideLength, row*sideLength, sideLength, sideLength) for col in range(8)] for row in range(8)]

pg.init()
screen = pg.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
g = Game()
clock = pg.time.Clock()
running = True

visibleMoves: list[Move] = []

def click(pos: tuple[int,int]) -> None: # move to Game
    """If a piece is already selected, execute the move that ends in the clicked space or deselect if another space is clicked. If a piece is not selected, highlight the moves of the clicked piece if the color matches the turn."""
    global visibleMoves
    if len(visibleMoves) > 0:
        for mv in visibleMoves:
            if mv.endPos() == pos:
                g.move(mv)
        visibleMoves.clear()
    else:
        piece = g.getSpace((row,col))
        if piece is not None:
            visibleMoves = piece.getMoves()

def darker(color: tuple[int, ...]) -> tuple[int, ...]:
    """Return a tuple representing a color slightly darker than the argument"""
    newColor = []
    for val in color:
        newColor.append(val - DARKERMODIFIER if val >= DARKERMODIFIER else 0)
    return tuple(newColor)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT: # close window
            running = False
        if event.type == pg.MOUSEBUTTONUP: # click detection
            pos = pg.mouse.get_pos()
            for row in range(8):
                for col in range(8):
                    if tiles[row][col].collidepoint(pos):
                        click((row,col))
                        
    # render board
    for row in range(8):
        for col in range(8):
            color: tuple[int, ...] = COLORLIGHT if (row + col) % 2 == 0 else COLORDARK
            for mv in visibleMoves: # darken color to highlight
                if mv.endPos() == (row,col):
                    color = darker(color)
                    break
            pg.draw.rect(screen,color,tiles[row][col]) # draw tile
            piece = g.getSpace((row,col))
            if piece is not None: # draw piece on tile
                imagePath = f"images/{piece.color.capitalize()}{type(piece).__name__}.png"
                image = pg.transform.scale(pg.image.load(imagePath),(sideLength,sideLength))
                screen.blit(image,tiles[row][col])

    pg.display.flip()
    clock.tick(60)

pg.quit()