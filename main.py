import pygame as pg

WIN_X, WIN_Y = 800, 500
FPS = 40
GREEN = (50, 150, 50)
BLUE = (50, 50, 150)
RED = (150, 50, 50)


class GameSprite(pg.sprite.Sprite):
    def __init__(self, color, x, y, speed, wight, height):
        super().__init__()
        self.image = pg.Surface((wight, height)) #вместе 55,55 - параметры
        self.image.fill(color=color)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player1(GameSprite):
   def update(self):
       keys = pg.key.get_pressed()
       if keys[pg.K_UP] and self.rect.y > 0:
           self.rect.y -= self.speed
       if keys[pg.K_DOWN] and self.rect.y < WIN_Y - self.rect.height:
           self.rect.y += self.speed
class Player2(GameSprite):
   def update(self):
       keys = pg.key.get_pressed()
       if keys[pg.K_w] and self.rect.y > 0:
           self.rect.y -= self.speed
       if keys[pg.K_s] and self.rect.y < WIN_Y - self.rect.height:
           self.rect.y += self.speed

win = pg.display.set_mode((WIN_X, WIN_Y))
pg.display.set_caption("Ping-pong")

#создания мяча и ракетки   
racket2 = Player2(BLUE, 15, 200, 4, 25, 150) 
racket1 = Player1(RED, WIN_X - 40, 200, 4, 25, 150)

clock = pg.time.Clock()
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    win.fill(GREEN)
    racket1.update()
    racket2.update()
    racket1.reset(win)
    racket2.reset(win)
    pg.display.update()
    clock.tick(FPS)