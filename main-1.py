import pygame, sys, math, random
from Rqueue import *
from BulletsClass import *
from own import OwnClass
from foe import *

class OwnFly(pygame.sprite.Sprite):
    def __init__(self,image_file,location):
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.imagesum = 0
    def images(self):
        self.imagesum += 1
        if self.imagesum >12 :
            self.imagesum = 0
        self.image = pygame.image.load('image/own/own%s.png' % ((self.imagesum/4)+1))
        return self.image

class BulletClass(pygame.sprite.Sprite):
    def __init__(self,image_file,pos,epos, speed = [0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        '''x = random.randint(-4,4)
        y = random.randint(-4,4)
        self.speed = [x, y]'''
        s = math.sqrt(mox(abs(epos[0]-pos[0])) + mox(abs(epos[1]-pos[1])))/8
        self.speed = speed
        self.speed = [(epos[0]-pos[0]) / s, (epos[1]-pos[1]) / s]
    def move(self):
        self.rect = self.rect.move(self.speed)

def drawRq(rq):
    while rq.head:
        data = rq.remove()
        if data.bool:
            return
        screen.blit(data.image,data.pos)

def mox(x):
    return x * x

def anim(bullets, own,rq):
    global score
    for foe in foes:
        foe.move(own,bullets)
        rq.add(foe.reImage(), foe.rect)
        if foe.rect.centerx > 450 or foe.rect.centery >700 or foe.rect.centerx <0 or foe.rect.centery < 0 :
            foes.remove(foe)
        if math.sqrt(mox(abs(foe.rect.centerx-own.rect.centerx)) + mox(abs(foe.rect.centery-own.rect.centery))) < foe.rect.width/2 + 5 :
            score += 1
            foes.remove(foe)
        
    for bullet in bullets:
        bullet.move()
        rq.add(bullet.image, bullet.rect)
        if bullet.rect.centerx > 450 or bullet.rect.centery >700 or bullet.rect.centerx <0 or bullet.rect.centery < 0 :
            bullets.remove(bullet)
        if math.sqrt(mox(abs(bullet.rect.centerx-own.rect.centerx)) + mox(abs(bullet.rect.centery-own.rect.centery))) < bullet.rect.width/2 + 5 :
            score += 1
            bullets.remove(bullet)
    for bullet in ownBullets:
        bullet.move()
        rq.add(bullet.image, bullet.rect)
        if bullet.rect.centerx > 450 or bullet.rect.centery >700 or bullet.rect.centerx <0 or bullet.rect.centery < 0 :
            ownBullets.remove(bullet)
        
            


def fonts(text, size, x, y,rq):
    font = pygame.font.Font(None, size)
    content = font.render(text, 1,(0,0,0))
    textpos = [x, y]
    rq.add(content, textpos)
    return content

pygame.init()
screen = pygame.display.set_mode([450,700])
screen.fill([255,255,255])
own = OwnClass([250,550])
rq = Rqueue()
pygame.key.set_repeat(12,12)
bullets = []
foes = []
ownBullets = []
clock = pygame.time.Clock()
global score
score = 0
maxs = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and own.rect.centery-10>0:
                own.rect.centery -= 6
                own.imagees()
            if event.key == pygame.K_DOWN and own.rect.centery+10<700 :
                own.imagees()
                own.rect.centery += 6
            if event.key == pygame.K_LEFT and own.rect.centerx-10>0:
                own.rect.centerx -= 6
                own.left()
            if event.key == pygame.K_RIGHT and own.rect.centerx+10<450:
                own.rect.centerx += 6
                own.right()
            if event.key == pygame.K_z:
                ownBullet = OwnBullets(2,own.rect.center)
                ownBullets.append(ownBullet)
                

    clock.tick(50)
    screen.fill([255,255,255])
    b = random.randint(0,20)
    if b == 0 :
        '''angle = random.randint(0,360)
        intx = 100 * math.sin(angle*math.pi/180)+120
        inty = 100 * math.cos(angle*math.pi/180)+120
        maxs += 1
        bullet = BulletsClass(1,[intx,inty], own.rect.center)
        bullets.append(bullet)'''
        foe = BlueFoe([450, 60])
        foes.append(foe)

    rq.add(own.image, own.rect)
    anim(bullets, own,rq)
    fonts('on: %s/%s' % (score,maxs),16,30,30,rq)
    rq.add(None, None,True)
    drawRq(rq)
    pygame.display.flip()

