import pygame,sys #import a library of functions called 'pygame'
from pygame.locals import *
#from init2 import *

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y,health,color,element,speed,name,data):
        pygame.sprite.Sprite.__init__(self)  
        self.name = name
        #set the pictures
        if self.name == 'Karak':
            self.image = pygame.transform.scale(data.monster1,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Lyote':
            self.image = pygame.transform.scale(data.monster2,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'SunBeam':
            self.image = pygame.transform.scale(data.monster3,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'StealthBomber':
            self.image = pygame.transform.scale(data.monster4,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'HellFyre':
            self.image = pygame.transform.scale(data.monster5,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'SeaGuardian':
            self.image = pygame.transform.scale(data.monster6,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'SunRay':
            self.image = pygame.transform.scale(data.monster7,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'DarkBat':
            self.image = pygame.transform.scale(data.monster8,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'SeaDemon':
            self.image = pygame.transform.scale(data.monster9,(30,30))
        elif self.name == 'Mermaid':
            self.image = pygame.transform.scale(data.monster10,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'RagingGod':
            self.image = pygame.transform.scale(data.monster11,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'InvisibleSlippery':
            self.image = pygame.transform.scale(data.monster12,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Boss1':
            self.image = pygame.transform.scale(data.boss1,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Boss2':
            self.image = pygame.transform.scale(data.boss2,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'FinalBoss':
            self.image = pygame.transform.scale(data.finalboss,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Water Elemental':
            self.image = pygame.transform.scale(data.water1,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Water Elemental 2':
            self.image = pygame.transform.scale(data.water2,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Water Elemental 3':
            self.image = pygame.transform.scale(data.water3,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Fire Elemental':
            self.image = pygame.transform.scale(data.fire1,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Fire Elemental 2':
            self.image = pygame.transform.scale(data.fire2,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Fire Elemental 3':
            self.image = pygame.transform.scale(data.fire3,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Darkness Elemental':
            self.image = pygame.transform.scale(data.dark1,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Darkness Elemental 2':
            self.image = pygame.transform.scale(data.dark2,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Darkness Elemental 3':
            self.image = pygame.transform.scale(data.dark3,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Light Elemental':
            self.image = pygame.transform.scale(data.light1,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Light Elemental 2':
            self.image = pygame.transform.scale(data.light2,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Light Elemental 3':
            self.image = pygame.transform.scale(data.light3,(30,30)).convert()
            self.image.set_colorkey((data.whiteColor))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.health = health
        self.element = element
        self.speed = speed
        self.data = data
  
    # Find a new position for the enemy
    def update(self,data):
        step=self.speed#from 1 to 10
        #hard coded to keep within the path set
        if 50<=self.rect.x<=100 and self.rect.y<210:
            self.rect.y+=step
        elif 200<=self.rect.y<=235 and 50<=self.rect.x<=407:
            self.rect.x+=step
        elif 407<=self.rect.x<=435 and 200<=self.rect.y<=407:
            self.rect.y+=step
        elif 407<=self.rect.y<=435 and 115<=self.rect.x<=435:
            self.rect.x-=step
        elif 100<=self.rect.x<=135 and 407<=self.rect.y<=455:
            self.rect.y+=step
        elif 455<=self.rect.y<=475 and 100<=self.rect.x<=607:
            self.rect.x+=step
        elif 607<=self.rect.x<=(635) and (1<=self.rect.y<=475):
            self.rect.y-=step


class Wave(pygame.sprite.Sprite):
    def __init__(self,list,data):
        pygame.sprite.Sprite.__init__(self)
        self.list = list #give a list of the monsters for each level in the subclass
        self.data=data

class Towers(pygame.sprite.Sprite):
    def __init__(self,name,range,cost,bulletdamage,timer,description,element,color,water,fire,light,darkness,data):
        pygame.sprite.Sprite.__init__(self)
        self.name = name #type of tower
        self.range = range #what is the range in radius of each kind of tower
        self.cost = cost #money needed to purchase tower
        self.bulletdamage = bulletdamage #damage done to enemy
        self.timer = timer #the time before next shot fired
        self.description = description #gives the decription on UI
        self.element = element #gives element of tower
        self.color = color
        self.water = water
        self.fire = fire
        self.light = light
        self.darkness = darkness
        self.data = data

class Enemy(pygame.sprite.Sprite):
    def __init__(self,name,health,vectorspeed,element,color,data):
        pygame.sprite.Sprite.__init__(self)
        self.name = name #name of enemy
        self.health = health #the number of hits taken before death
        self.vectorspeed = vectorspeed #the initial speed of the enemy
        self.element = element #this one of the 6 elements
        self.data = data
        self.color = color

class Turrets(pygame.sprite.Sprite):
    def __init__(self,x,y,color,damage,range,cost,rate,description,element,name,data):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([50,50])
        #self.image.fill(color) 
        self.damage = damage
        # Make our top-left corner the passed-in location.
        #self.rect = self.image.get_rect()
        #self.rect.x = x 
        #self.rect.y = y
        self.range = range
        self.cost = cost
        self.rate = rate
        self.description = description
        self.element = element
        self.name = name
        self.data = data
        if self.name == 'Fire':
            self.image = pygame.transform.scale(data.fireTower,(50,50)).convert()
            self.image.set_colorkey((data.blackColor))
        elif self.name == 'Focused Fire':
            self.image = pygame.transform.scale(data.focusedfireTower,(50,50)).convert()
            self.image.set_colorkey((data.blackColor))
        elif self.name == 'Water':
            self.image = pygame.transform.scale(data.waterTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Focused Water':
            self.image = pygame.transform.scale(data.focusedwaterTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Light':
            self.image = pygame.transform.scale(data.lightTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Focused Light':
            self.image = pygame.transform.scale(data.focusedlightTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Darkness':
            self.image = pygame.transform.scale(data.darknessTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Focused Darkness':
            self.image = pygame.transform.scale(data.focuseddarknessTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Steam':
            self.image = pygame.transform.scale(data.steamTower,(50,50)).convert()
            self.image.set_colorkey((data.blackColor))
        elif self.name == 'Magnify':
            self.image = pygame.transform.scale(data.magnifyTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Devil':
            self.image = pygame.transform.scale(data.devilTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Rainbow':
            self.image = pygame.transform.scale(data.rainbowTower,(50,50)).convert()
            self.image.set_colorkey((data.blackColor))
        elif self.name == 'Poison':
            self.image = pygame.transform.scale(data.poisonTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == 'Trickery':
            self.image = pygame.transform.scale(data.trickeryTower,(50,50)).convert()
            self.image.set_colorkey((117,117,117))
        elif self.name == "Laser":
            self.image = pygame.transform.scale(data.laserTower,(50,50)).convert()
            self.image.set_colorkey((data.whiteColor))
        elif self.name == "Hail":
            self.image = pygame.transform.scale(data.hailTower,(50,50)).convert()
            self.image.set_colorkey((data.blackColor))
        elif self.name == "FlameThrower":
            self.image = pygame.transform.scale(data.flamethrowerTower,(50,50)).convert()
            self.image.set_colorkey((data.blackColor))
        elif self.name == "Corrosion":
            self.image = pygame.transform.scale(data.corrosionTower,(50,50)).convert()
            self.image.set_colorkey((data.blackColor))
        else:
            self.image = pygame.Surface([50,50])
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,xcol,ycol,damage,range,ratecounter,element,data):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([5, 5])
        self.image.fill(data.blackColor)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xcol = xcol
        self.ycol =ycol
        self.damage = damage
        self.range = range
        self.ratecounter = ratecounter
        self.element = element

    def update(self,data):
        displacement = 5 #every new image of bullet at interval of 5
        range = 30 * (self.range/100.0) #bullet range
        if self.xcol==0 and abs(data.turretCounter*(self.ycol)*displacement)<(range+20):
            self.rect.x += self.xcol*displacement
            self.rect.y += self.ycol*displacement
            data.turretCounter+=1
        elif self.ycol==0 and abs(data.turretCounter*(self.xcol)*displacement)<(range+20):
            self.rect.x += self.xcol*displacement
            self.rect.y += self.ycol*displacement
            data.turretCounter+=1
        elif self.xcol!=0 and self.ycol!=0 and (((data.turretCounter*self.xcol*displacement)**2)+((data.turretCounter*self.ycol*displacement)**2))**0.5<(range):
            self.rect.x += self.xcol*displacement
            self.rect.y += self.ycol*displacement
            data.turretCounter+=1
        else:
            self.rect.x = 1300
            self.rect.y= 900
            data.turretCounter = 1