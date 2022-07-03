from pygame import *

W = 700
H = 500
FPS = 60

window = display.set_mode((W, H))
back_image = image.load('back.webp')
background = transform.scale(back_image, (W, H))
clock = time.Clock()

class Sprite():
    def __init__(self, model, w, h, x, y):
        self.image = transform.scale(image.load(model), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


sprite = Sprite('player.png', 100, 130, 100, 100)

isRun = True
while isRun:
    for e in event.get():
        if e.type == QUIT:
            isRun = False
    display.update()
    window.blit(background, (0, 0))
    sprite.draw()
    clock.tick(FPS)





