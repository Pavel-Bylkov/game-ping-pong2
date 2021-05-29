import pygame as pg

WIN_X, WIN_Y = 800, 500
FPS = 40
GREEN = (50, 150, 50)

win = pg.display.set_mode((WIN_X, WIN_Y))
pg.display.set_caption("Ping-pong")

clock = pg.time.Clock()
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    win.fill(GREEN)
    pg.display.update()
    clock.tick(FPS)