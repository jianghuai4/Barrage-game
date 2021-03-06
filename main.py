import pygame, sys, math, random
from multiprocessing import Process
import os
from Rqueue import *
from BulletsClass import *
from own import *
from foe import *
from collision import *
from drop import *
import copy

def plot_read(chapter):
    with open('plot/plot%s.txt' % chapter) as plot_file:
        plots = plot_file.readlines()
    return plots
    
def plot_process(plots, foes):
    global proc
    global plotIndex
    if len(bossFoe) == 0:
        proc += 1
    print(proc)
    print(len(plots),plotIndex)
    while(plotIndex < len(plots)):
        param = plots[plotIndex].split(',')
        if proc == int(param[0]):
            print(param)
            foe = creatFoe(param)
            if int(param[2]) > 10:
                bossFoe.append(foe)
            else:
                foes.append(foe)
            plotIndex += 1
        else:
            return

def creatFoe(param):
    shoot = ShootMode.get_shoot(int(param[1]))
    pos = [int(param[4]), int(param[5])]
    drop = get_drop(int(param[3]))
    foe = get_foe(int(param[2]), pos, drop)
    foeMove = get_foeMove(int(param[6]), foe)
    foeMove.shoot = shoot
    return foeMove

#---------------------------物体移动--------------------------------
def moveAll(own, foes, bossFoe, bullets, ownBullets, drops):
    own.move()
    for foe in foes:
        foe.move(own, bullets)
        #敌机超出屏幕外50px后，消除敌机
        if abs(foe.foe.rect.centerx - width/2) > width/2+50 or abs(foe.foe.rect.centery - height/2) > height/2+50:
            foes.remove(foe)
    for foe in bossFoe:
        foe.move(own, bullets)
    for bullet in bullets:
        bullet.move()
        #弹幕超出屏幕外100px后，消除弹幕
        if abs(bullet.rect.centerx - width/2) > width/2+100 or abs(bullet.rect.centery - height/2) > height/2+100:
            bullets.remove(bullet)
    for obullet in ownBullets:
        obullet.move()
        #自机弹幕超出屏幕10px后，消除弹幕
        if abs(obullet.rect.centerx - width/2) > width/2+10 or abs(obullet.rect.centery - height/2) > height/2+10:
            ownBullets.remove(obullet)
    for drop in drops:
        drop.move()
        #掉落物超出屏幕外12px后，消除掉落物
        if abs(drop.rect.centerx - width/2) > width/2+10 or abs(drop.rect.centery - height/2) > height/2+10:
            drops.remove(drop)
    colli1(own, foes, bossFoe, bullets, drops)
    colli2(foes, bossFoe, ownBullets)

#---------------------------物体碰撞------------------------------------
def colli1(own, foes, bossFoe, bullets, drops):
    global ownDie
    global dieTime
    for foe in foes:
        if collision(own, foe.foe, -10):
            foe.coll(own.atr, drops, foes)
            own.die()
    for foe in bossFoe:
        if collision(own, foe.foe, -10):
            foe.coll(0, drops, bossFoe)
            own.die()
    for bullet in bullets:
        if collision(own, bullet, -10):
            bullets.remove(bullet)
            own.die()
    for drop in drops:
        if collision(own, drop, 30):
            #drops.remove(drop)
            #own.barrage.barUp()
            drop.coll(drops, own)

def colli2(foes, bossFoe, ownBullets):
    for foe in foes:
        for bullet in ownBullets:
            if collision(foe.foe, bullet):
                replace = foe.coll(bullet.atr, drops, foes)
                if replace:
                    foe = foe.replaceMove()
                bullet.die(ownBullets)
    for foe in bossFoe:
        for bullet in ownBullets:
            if collision(foe.foe, bullet):
                replace = foe.coll(bullet.atr, drops, bossFoe)
                if replace:
                    foe = foe.replaceMove()
                bullet.die(ownBullets)

def draw(own, foes, bossFoe, bullets, ownBullets, drop):
    screen.blit(own.image, own.rect)
    for foe in foes:
        screen.blit(foe.foe.image, foe.foe.rect)
    for foe in bossFoe:
        screen.blit(foe.foe.image, foe.foe.rect)
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)
    for ownBullet in ownBullets:
        screen.blit(ownBullet.image, ownBullet.rect)
    for drop in drops:
        screen.blit(drop.image, drop.rect)

def rqueueDraw(rq):
    rq.add(None,None,True,0)
    draw = rq.head
    while draw:
        screen.blit(draw.image[draw.number-1], draw.pos)
        draw.loop()
        draw = draw.next
        if draw.bool:
            break

def game_interface(clock):
    interface = pygame.image.load('image/interface/game_start.jpg')
    title = pygame.image.load('image/interface/title.png')
    start = pygame.image.load('image/interface/start.png')
    setting = pygame.image.load('image/interface/setting.png')
    over = pygame.image.load('image/interface/over.png')
    interface_rect = interface.get_rect()
    interface_rect.left, interface_rect.top = [0,0]
    title_rect = title.get_rect()
    title_rect.left, title_rect.top = [58,40]
    start_rect = start.get_rect()
    start_rect.left, start_rect.top = [35,565]
    setting_rect = setting.get_rect()
    setting_rect.left, setting_rect.top = [158,605]
    over_rect = over.get_rect()
    over_rect.left, over_rect.top = [285,646]
    
    trans_interface = pygame.Surface([450,700])
    trans_interface.blit(interface,[0,0])
    
    times = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if times > 175:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] > start_rect.left and event.pos[0] < start_rect.right:
                        if event.pos[1] > start_rect.top and event.pos[1] < start_rect.bottom:
                            return
                    if event.pos[0] > setting_rect.left and event.pos[0] < setting_rect.right:
                        if event.pos[1] > setting_rect.top and event.pos[1] < setting_rect.bottom:
                            pass
                    if event.pos[0] > over_rect.left and event.pos[0] < over_rect.right:
                        if event.pos[1] > over_rect.top and event.pos[1] < over_rect.bottom:
                            sys.exit()
                
        clock.tick(50)
        times += 1
        if times < 50:
        #screen.blit(interface, [0,0])
            screen.fill([255,255,255])
            trans_interface.set_alpha(times*5+10)
            screen.blit(trans_interface, interface_rect)
        #screen.blit(title, [58,40])
        #screen.blit(start, [35,565])
        #screen.blit(setting, [158,605])
        #screen.blit(over, [285,646])
        else:
            screen.blit(interface, interface_rect)
        if times > 150 and times <= 175:
            screen.blit(over, [over_rect.left+12-(times-150)/2,over_rect.top])
            trans_interface.set_alpha(255-(times-150)*10)
            screen.blit(trans_interface, interface_rect)
        elif times > 175:
            screen.blit(over, over_rect)
        if times > 125 and times <= 150:
            screen.blit(setting,[setting_rect.left+12-(times-125)/2,setting_rect.top])
            trans_interface.set_alpha(255-(times-125)*10)
            screen.blit(trans_interface, interface_rect)
        elif times > 150:
            screen.blit(setting, setting_rect)
        if times > 100 and times <= 125:
            screen.blit(start,[start_rect.left+12-(times-100)/2,start_rect.top])
            trans_interface.set_alpha(255-(times-100)*10)
            screen.blit(trans_interface, interface_rect)
        elif times > 125:
            screen.blit(start, start_rect)
        if times > 50 and times <= 100:
            screen.blit(title, title_rect)
            trans_interface.set_alpha(255-(times-50)*5)
            screen.blit(trans_interface, interface_rect)
        elif times > 100:
            screen.blit(title,title_rect)

        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    global width
    global height
    width, height = (450,700)
    screen = pygame.display.set_mode([width,height])
    screen.fill([255,255,255])
    global plotIndex
    global score
    global ownDie
    ownDie = False
    global dieTime
    global proc
    background = pygame.image.load('image/interface/background.jpg')
    background_rect = background.get_rect()
    background_rect.left, background_rect.top = (0, -1300)
    score = 0
    proc = 0
    plotIndex = 1
    bullets = []
    foes = []
    ownBullets = []
    drops = []
    bossFoe = []
    own = OwnClass([250,730], width/2, height/2, ownBullets)
    ownShadow = OwnShadow()
    rq = Rqueue.creatRq()
    pygame.key.set_repeat(12,12)
    clock = pygame.time.Clock()
    plots = plot_read(1)
    maxs = 0
    proc = 0
    #-------------------以下为测试内容------------------------
    #-----------------掉落物drop--------------------
    #drop = FractionDrop()
    #-----------------弹幕类型-----------------------
    #shoot = 7
    #------------------怪物移动方式FoeMove,怪物外观BlueFoe-------------------
    #foe = FoeMove3(BlueFoe([150,-10],drop), shoot)
    #------------------怪物组foes-------------------------
    #foes.append(foe)
    game_interface(clock)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and own.rect.centery-10>0:
                    own.speed[1] = -6
                if event.key == pygame.K_DOWN and own.rect.centery+10<700 :
                    own.speed[1] = 6
                if event.key == pygame.K_LEFT and own.rect.centerx-10>0:
                    own.speed[0] = -6
                    own.state = 4
                if event.key == pygame.K_RIGHT and own.rect.centerx+10<450:
                    own.speed[0] = 6
                    own.state = 8
                if event.key == pygame.K_z:
                    own.shooting = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and own.rect.centery-10>0:
                    own.speed[1] = 0
                if event.key == pygame.K_DOWN and own.rect.centery+10<700 :
                    own.speed[1] = 0
                if event.key == pygame.K_LEFT and own.rect.centerx-10>0:
                    own.speed[0] = 0
                    own.state = 0
                if event.key == pygame.K_RIGHT and own.rect.centerx+10<450:
                    own.speed[0] = 0
                    own.state = 0
                if event.key == pygame.K_z:
                    own.shooting = False
                        


        clock.tick(50)
        plot_process(plots, foes)
        background_rect.centery += 1
        screen.blit(background,background_rect)
        if background_rect.top > 0:
            background_rect.top = -2000
        if background_rect.top < -1300:
            screen.blit(background, [0,background_rect.top+2000])
        moveAll(own, foes, bossFoe, bullets, ownBullets,drops)
        draw(own,foes, bossFoe,bullets,ownBullets,drops)
        if own.dieTime <= 100:
            own.dieTime += 1
            if own.dieTime < 30:
                own.rect.centery -= 3
        pygame.display.flip()
        

