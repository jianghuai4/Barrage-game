import pygame
from Rqueue import *
from BulletsClass import *

class OwnClass():
    def __init__(self, pos, width, height, bullets):
        self.images = []
        self.left_images = []
        self.right_images = []
        self.angle = 0
        self.speed = [0,0]
        self.cwid = width
        self.chei = height
        for i in range(7):
            self.left_images.append('image/own/own_left%s.png' % (i+1))
            self.right_images.append('image/own/own_right%s.png' % (i+1))
            if i < 4:
                self.images.append('image/own/own%s.png' % (i+1))
        self.image = pygame.image.load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.imagesum = 0
        self.speed = [0, 0]
        self.barrage = Barrage()
        self.shooting= False
        self.bullets = bullets
        self.atr = 100

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]
        self.imagesum += 1
        self.image = pygame.image.load(self.images[int((self.imagesum%12))//3])
        if  self .imagesum > 12:
            self.imagesum = 0
        if abs(self.rect.centerx - self.cwid) > self.cwid:
            self.speed[0] = 0
        if abs(self.rect.centery - self.chei) > self.chei:
            self.speed[1] = 0
        if self.shooting and self.imagesum % 3 == 0:
            self.barrage.shooting(self.rect.center, self.bullets)

    def die(self):
        self.rect.center = [225,1000]
        #rq = Rqueue.creatRq()
        #images = []
        #pos = self.rect
        #rq.add(images,pos,len(images))
        pass

class OwnShadow():
    def __init__(self):
        self.images = ['image/own/own1.png', 'image/own/own2.png', 'image/own/own3.png', 'image/own/own4.png', ]
        self.image = pygame.image.load(self.images[0])
        self.rect = self.image.get_rect()
        self.index = 0

    def move(self):
        self.rect.centery -= 3

    def imgs(self):
        self.index += 1
        image = pygame.image.load(self.images[self.index/3 % 4])
