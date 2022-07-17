from pygame import *
from random import *

W = 700
H = 500
FPS = 60

ENEMY_COUNT = 0
#0.Заменить музыку
#1.Сделать возможность создавать противника, который не преследует игрока, а двигаеться в случайную сторону.
#2.Сделать возможность меня кол-во противников с помощью переменной ENEMY_COUNT (Вспоминаем списки).

window = display.set_mode((W, H))
timer = time.Clock()
backgroud = transform.scale(image.load('back.webp'), (W,H))
game_over = transform.scale(image.load('game_over.jpg'), (W,H))

randomEnemies = []

#mixer.init()
#mixer.music.load('background.mp3')
#mixer.music.play()

class Sprite():
    def __init__(self, model, w, h, x, y):
        self.model = transform.scale(image.load(model), (w, h))
        self.rect = self.model.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.degree = 0
        self.isFlip = False

    def set_rotate(self, degree):
        dif = degree - self.degree;
        self.degree = degree
        self.model = transform.rotate(self.model, dif)

    def set_flip(self, isFlip):
        if isFlip != self.isFlip:
            self.model = transform.flip(self.model, 180, 0)
            self.isFlip = isFlip

    def draw(self):
        window.blit(self.model, (self.rect.x, self.rect.y))

class Chatacter(Sprite):
    def __init__(self, model, w, h, x, y, speed):
        super().__init__(model, w, h, x, y)
        self.speed = speed
    def move(self, direction):
        if direction == 0 and self.rect.y > 0:
            for wall in wallList:
                if self.rect.y <= wall.rect.y + wall.rect.h  and self.rect.y >= wall.rect.y:
                    if (wall.rect.x + wall.rect.w >= self.rect.x >= wall.rect.x) or (wall.rect.x  >= self.rect.x + wall.rect.w  >= wall.rect.x + wall.rect.w ):
                       return
            self.rect.y -= self.speed
        if direction == 1 and self.rect.y < H - self.rect.h:
            for wall in wallList:
                if self.rect.y + self.rect.h  >= wall.rect.y and self.rect.y + self.rect.h  <= wall.rect.y + wall.rect.h :
                    if (wall.rect.x + wall.rect.w >= self.rect.x >= wall.rect.x) or (wall.rect.x  >= self.rect.x + wall.rect.w  >= wall.rect.x + wall.rect.w ):
                       return
            self.rect.y += self.speed
        if direction == 2 and self.rect.x > 0:
            for wall in wallList:
                if self.rect.x <= wall.rect.x + wall.rect.w  and self.rect.x >= wall.rect.x:
                    if (self.rect.y > wall.rect.y and self.rect.y < wall.rect.y + wall.rect.h) or (self.rect.y + self.rect.h > wall.rect.y and self.rect.y + self.rect.h < wall.rect.y + wall.rect.h):
                        return
            self.rect.x -= self.speed

        if direction == 3 and self.rect.x < W - self.rect.w:
            for wall in wallList:
                if self.rect.x + self.rect.w >= wall.rect.x and self.rect.x + self.rect.w <=  wall.rect.x + wall.rect.w:
                    if (self.rect.y > wall.rect.y and self.rect.y < wall.rect.y + wall.rect.h) or (self.rect.y + self.rect.h > wall.rect.y and self.rect.y + self.rect.h < wall.rect.y + wall.rect.h):
                        return
            self.rect.x += self.speed






class Player(Chatacter):
    def __init__(self, model, w, h, x, y, speed):
        super().__init__(model, w, h, x, y, speed)

    def move(self):
        najatie_knopki = key.get_pressed()

        if najatie_knopki[K_UP]:
            super().move(0)

        if najatie_knopki[K_DOWN]:
            super().move(1)

        if najatie_knopki[K_LEFT]:
            super().move(2)
            self.set_flip( True)

        if najatie_knopki[K_RIGHT]:
            super().move(3)
            self.set_flip( False)



    def checkCollison(self):
        if self.rect.colliderect(enemy.rect) == True:
            return True
        for e in randomEnemies:
            if self.rect.colliderect(e.rect) == True:
                return True
        return False


class Enemy(Chatacter):
    def __init__(self, model, w, h, x, y, speed):
        super().__init__(model, w, h, x, y, speed)


    def chase(self, target):
        if target.rect.x > self.rect.x:
            super().move(3)
        else:
            super().move(2)
        if target.rect.y > self.rect.y:
            super().move(1)
        else:
            super().move(0)

    def move(self):
        direction = randint(0,3)
        super().move(direction)

class Wall(Sprite):
    def __init__(self, model, w, h, x, y):
        super().__init__(model, w, h, x, y)

wallList = []
w1 = Wall('wall.png', 300, 10, 100, 300)
w2 = Wall('wall.png', 10, 300, 150, 0)
w3 = Wall('wall.png', 10, 300, 250, 0)
wallList.append(w1)
wallList.append(w2)
wallList.append(w3)


myPlayer = Player('player.png', 50, 60, 0, 0, 5)
enemy = Enemy('enemy.png', 50, 60, 400, 300, 2)

for i in range(ENEMY_COUNT):
    newEnemy = Enemy('fire.png', 50, 70, randint(0, W), randint(0, H), 3)
    randomEnemies.append(newEnemy)
isWin = True
isGame = True #Остановка движения
run = True #Остановка всей игры целиком!
while run:
    display.update()

    for e in event.get():
        if e.type == QUIT:
            run = False

    if isGame == True:
        myPlayer.move()
        if myPlayer.checkCollison() == True:
            isGame = False
            isWin = False

        enemy.chase(myPlayer)
        for e in randomEnemies:
            e.move()
    #--------------------------------------------------

        window.fill((0, 0, 0))
        window.blit(backgroud, (0, 0))
        myPlayer.draw()
        for wall in wallList:
            wall.draw()
        enemy.draw()
        for e in randomEnemies:
            e.draw()
    else:
        window.blit(game_over, (0, 0))

    timer.tick(FPS)