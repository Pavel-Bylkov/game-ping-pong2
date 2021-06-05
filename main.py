import pygame as pg
from time import time

WIN_X, WIN_Y = 600, 500
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

class Ball(pg.sprite.Sprite):
    def __init__(self, image, x, y, speed, wight, height):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image), (wight, height)) #вместе 55,55 - параметры
        self.speed_x = speed
        self.speed_y = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        #если мяч достигает границ экрана, меняем направление его движения
        if self.rect.y > WIN_Y - self.rect.height or self.rect.y < 0:
           self.speed_y *= -1
    
    def collide_rocket(self, rocket):
        if pg.sprite.collide_rect(self, rocket):
            self.speed_x *= -1
            if self.speed_x > 0:
                self.speed_x += 1
            else:
                self.speed_x -= 1

class Button(GameSprite):
    def __init__(self, text, x, y, wight, height, font_color=GREEN, bg_color=BLUE, fsize=40):
        super().__init__(bg_color, x, y, 0, wight, height)
        self.text = text
        self.fsize = fsize
        self.font = pg.font.Font(None, self.fsize)
        self.font_color = font_color
        self.visible = True
        self.render()
        
    def render(self):
        self.text_img = self.font.render(self.text, True, self.font_color)
        self.rect_text = self.text_img.get_rect()
        self.rect_text.centerx = self.rect.centerx
        self.rect_text.centery = self.rect.centery

    def reset(self, win):
        if self.visible:
            super().reset(win)  # Вызываем метод Родительского класса
            win.blit(self.text_img, (self.rect_text.x, self.rect_text.y))
    
    def is_clicked(self, x, y):
        return self.visible and self.rect.collidepoint(x, y)
    
    def show(self):
        if not self.visible:
            self.visible = True
    
    def hide(self):
        if self.visible:
            self.visible = False

win = pg.display.set_mode((WIN_X, WIN_Y))
pg.display.set_caption("Ping-pong")

#создания мяча и ракетки   
racket1 = Player1(RED, WIN_X - 40, 200, 4, 25, 150)
racket2 = Player2(BLUE, 15, 200, 4, 25, 150) 
ball = Ball('ball.png', 200, 200, 4, 40, 40)

# надписи
pg.font.init()
font = pg.font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

# Кнопки меню
btn_start = Button(text="START", x=WIN_X//2, y=WIN_Y//2, wight=150, height=50)

def start():
    global finish
    finish = False
    btn_start.hide()
    racket1.rect.x, racket1.rect.y = WIN_X - 40, 200
    racket2.rect.x, racket2.rect.y = 15, 200
    ball.rect.x, ball.rect.y = 200, 200
    ball.speed_x = 4
    ball.speed_y = 4

clock = pg.time.Clock()
run = True
finish = True
end_game = False
last_time = time()
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if btn_start.is_clicked(x, y):
                start()
    win.fill(GREEN)
    if not finish:
        racket1.update()
        racket2.update()
        racket1.reset(win)
        racket2.reset(win)
        ball.update()
        ball.reset(win)
        ball.collide_rocket(racket1)
        ball.collide_rocket(racket2)

        #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            finish = True
            end_game = True
            who_lose = lose1
            last_time = time()

        #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > WIN_X - ball.rect.width:
            finish = True
            who_lose = lose2
            end_game = True
            last_time = time()
    else:
        btn_start.reset(win)
        if time() - last_time > 3:
            end_game = False
            btn_start.show()
        if end_game:
            win.blit(who_lose, (200, 200))
    pg.display.update()
    clock.tick(FPS)