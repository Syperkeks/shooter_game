#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
life  = 3
score = 0 # сбито кораблей
goal = 10 # столько кораблей нужно сбить для победы
lost  = 0 # пропущено кораблей
max_lost = 3 # проиграли, если пропустили столько

# окно игры
win_height = 500
win_width = 700
window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
background = transform.scale(image.load('cosmos.jpg'),(700,500))
window.blit(background,(0,0))
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,size_x,size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys  = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 20, 20)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #исчезает если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()
# фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
# FPS
clock = time.Clock()
FPS = 60
clock.tick(FPS)
ship = Player('rocket.png', 5, win_height - 100,80,100,100)
finish = False
# шрифты и надписи
font.init()
font1 = font.SysFont('Arial',80)
win  = font1.render('YOU WIN!',True,(255,255,255))
lose = font1.render('YOU LOSE!',True,(180,0,0))
font2 = font.SysFont('Arial',36)
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
#класс спрайта врага
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost  = lost + 1
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80,win_width - 80), 40,randint(1,5), 50,50)
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy("asteroid.png",randint(80,win_width - 80), 40,randint(1,5), 50,50)
    asteroids.add(asteroid)
rel_time = False
num_fire  = 0
game  = True
font.init()
font2 = font.SysFont('Arial',36)
score  = 0
lost = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1 
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        # пишем текст на экране
        text = font2.render('Счёт:'+ str(score), 1,(255, 255, 255))
        window.blit(text,(10,20))
        text_lose = font2.render('Пропущено:'+ str(lost), 1,(255,255,255))
        window.blit(text_lose,(10,50))

        # производим движения спрайтов
        asteroids.update()
        ship.update()
        monsters.update()
        bullets.update()
        # обновляем их в новом местоположении
        ship.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        # проверка столкновения пули и монстра
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait,reload...', 1, (150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            # этот цикл повторится столько раз сколько монстров подбито
            score  = score + 1
            monster = Enemy('ufo.png', randint(80,win_width - 80), 40,randint(1,5), 50,50)
            monsters.add(monster)
        # возможный проигрыш
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True # проиграли 
            window.blit(lose,(200,200))
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life = life -1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        # проверка выигрыша
        if score >= goal:
            finish = True
            window.blit(win,(200,200))
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        text_life = font1.render(str(life),1,life_color)
        window.blit(text_life,(650,10))
        display.update()
        #цикл срабатывает каждые 0.05 секунд
    time.delay(50)


