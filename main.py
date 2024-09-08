# template from https://www.pg.org/docs/
import pygame as pg
from game import *

SCREENWIDTH = 720
SCREENHEIGHT = 720
COLORLIGHT = (255,255,255)
COLORDARK = (0,170,255)

pg.init()
screen = pg.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
g = Game()
clock = pg.time.Clock()
running = True
tiles = [[None]*8 for i in range(8)]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    # render board
    sideLength = int(SCREENHEIGHT/8)
    for row in range(8):
        for col in range(8):
            color = COLORLIGHT if (row + col) % 2 == 0 else COLORDARK
            tiles[row][col] = pg.Rect(col*sideLength,row*sideLength,sideLength,sideLength)
            pg.draw.rect(screen,color,tiles[row][col]) # draw tile
            piece = g.getSpace((row,col))
            if piece != None: # draw piece on tile
                imagePath = f"images/{piece.color.capitalize()}{type(piece).__name__}.png"
                image = pg.transform.scale(pg.image.load(imagePath),(sideLength,sideLength))
                screen.blit(image,tiles[row][col])

    pg.display.flip()
    clock.tick(60)

pg.quit()