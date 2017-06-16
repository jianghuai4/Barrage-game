import pygame,math
from BulletsClass import *
from Rqueue import *
from drop import *
from Angle import *

#---------------------------怪物类----------------------------------
class Foe():
    def __init__(self, HP, images, pos, drop):
        self.HP = HP
        self.images = images
        self.image = pygame.image.load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.drop = drop

    def reImage(self):
        return pygame.image.load(self.images[int(self.index / 4) % 4])

    def coll(self, atr, drops):
        self.HP -= atr
        if self.HP < 0:
            self.die(drops)
            return True
        else:
            return False

    def die(self, drops):
        self.drop.x = self.rect.centerx
        self.drop.y = self.rect.centery
        drops.append(self.drop)

class PinkFoe(Foe):
    def __init__(self, pos, drop):
        images = ['image/foe/foe2_1.png','image/foe/foe2_2.png','image/foe/foe2_3.png','image/foe/foe2_4.png']
        super(PinkFoe, self).__init__(10, images, pos, drop)

class BlueFoe(Foe):
    def __init__(self, pos, drop):
        images = ['image/foe/foe1_1.png','image/foe/foe1_2.png','image/foe/foe1_3.png','image/foe/foe1_4.png']
        super(BlueFoe, self).__init__(15, images, pos, drop)

class VioletFoe(Foe):
    def __init__(self, pos, drop):
        images = ['image/foe/foe3_1.png','image/foe/foe3_2.png','image/foe/foe3_3.png','image/foe/foe3_4.png']
        super(VioletFoe, self).__init__(25, images, pos, drop)

class RedFoe(Foe):
    def __init__(self, pos, drop):
        images = ['image/foe/foe4_1.png','image/foe/foe4_2.png','image/foe/foe4_3.png','image/foe/foe4_4.png']
        super(RedFoe, self).__init__(30, images, pos, drop)
    
class OrangeFoe(Foe):
    def __init__(self, pos, drop):
        images = ['image/foe/foe5_1.png','image/foe/foe5_2.png','image/foe/foe5_3.png','image/foe/foe5_4.png']
        super(OrangeFoe, self).__init__(35, images, pos, drop)

class ssBoss(Foe):
    def __init__(self, pos, drop):
        images = ['image/foe/ssBoss_1.png','image/foe/ssBoss_2.png']
        super(ssBoss, self).__init__(200, images, pos, drop)

class sBoss1(Foe):
    def __init__(self, pos, drop):
        images = ['image/foe/sBoss1_1.png','image/foe/sBoss1_2.png','image/foe/sBoss1_3.png','image/foe/sBoss1_4.png']
        super(sBoss1, self).__init__(500, images, pos, drop)

class sBoss2(Foe):
    def __init__(self, pos, drop):
        images = ['image/foe/sBoss2_1.png','image/foe/sBoss2_2.png','image/foe/sBoss2_3.png','image/foe/sBoss2_4.png']
        super(sBoss2, self).__init__(500, images, pos, drop)
        

def get_foe(index, pos, drop):
    if index == 0:
        foe = PinkFoe(pos, drop)
    elif index == 1:
        foe = BlueFoe(pos, drop)
    elif index == 2:
        foe = VioletFoe(pos, drop)
    elif index == 3:
        foe = RedFoe(pos, drop)
    elif index == 4:
        foe = OrangeFoe(pos, drop)
    elif index == 5:
        foe = ssBoss(pos, drop)
    elif index == 6:
        foe = sBoss1(pos, drop)
    elif index == 7:
        foe = sBoss2(pos, drop)
    return foe

#--------------------------------怪物的移动类----------------------------
class FoeMove():
    def __init__(self, foe):
        self.foe = foe
        self.index = 0
    def coll(self):
        self.foe.coll()

class FoeMove1(FoeMove):
    def move(self, own, bullets):
        self.index += 1
        if self.index < 45:
            self.foe.rect.centerx -= 5
        elif self.index >= 45 and self.index < 225:
            sp = Speed((360 - self.index * 2), 160)
            self.foe.rect.center = [sp[0] + 225, sp[1] + 210]
            if self.index % 10 == 0:
                self.shoot.shooting(self.foe.rect.center, own.rect.center, bullets)
        elif self.index >= 225:
            self.foe.rect.centerx -= 5
        self.foe.image = pygame.image.load(self.foe.images[int((self.index%4))])
        
class FoeMove2(FoeMove):
    def move(self, own, bullets):
        self.index += 1
        if self.index < 45:
            self.foe.rect.centerx += 5
        elif self.index >= 45 and self.index < 225:
            sp = Speed(self.index * 2+180, 160)
            self.foe.rect.center = [sp[0] + 225, sp[1] + 210]
            if self.index % 10 == 0:
                self.shoot.shooting(self.foe.rect.center, own.rect.center, bullets)
        elif self.index >= 225:
            self.foe.rect.centerx += 5
        self.foe.image = pygame.image.load(self.foe.images[int((self.index%4))])

class FoeMove3(FoeMove):
    def move(self, own, bullets):
        self.index += 1
        if self.index < 50:
            self.foe.rect.centery += 2
        if self.index >= 50 and self.index < 500:
            if self.index % 15 == 0:
                self.shoot.shooting(self.foe.rect.center, own.rect.center, bullets)
        if self.index > 500:
            self.foe.rect.centery += 3
            if self.index % 15 == 0:
                self.shoot.shooting(self.foe.rect.center, own.rect.center, bullets)

#----------未完成------------------
class FoeMove4(FoeMove):
    def move (self, own, bullets):
        self.index += 1
        if self.index < 50:
            self.foe.rect.centery += 2
        elif self.index == 50:
            self.cen = self.foe.rect.centerx
        elif self.index > 50 and self.index < 500:
            x = 80 * math.sin((self.index-50) * math.pi/180)
            self.foe.rect.centerx = self.cen + x
            self.shoot.shooting(self.foe.rect.center, own.rect.center, bullets, self.foe)
        elif self.index == 500:
            ang = Angle(self.foe.rect.center, own.rect.center)
            sp = Speed(ang)
            self.speed = sp
        elif self.index > 500:
            self.foe.rect.centery += self.speed[0]
            self.foe.rect.centerx += self.speed[1]

def get_foeMove(index, foe):
    if index == 0:
        foeMove = FoeMove1(foe)
    elif index == 1:
        foeMove = FoeMove2(foe)
    elif index == 2:
        foeMove = FoeMove3(foe)
    elif index == 3:
        foeMove = FoeMove4(foe)
    
    return foeMove
