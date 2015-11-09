import pygame,sys #import a library of functions called 'pygame'
from pygame.locals import *
from classes import *

def init2(data):
    #all the hard coded data is here
    data.gameOverWinSound=pygame.mixer.Sound("music/JazzTip.wav")
    data.gameOverLoseSound=pygame.mixer.Sound("music/laugh.wav")

    #define some colors
    data.blackColor = (0,0,0)
    data.whiteColor = (255,255,255)
    data.greenColor = (0,255,0)
    data.redColor = (255,0,0)
    data.blueColor = (0,0,255)
    data.yellowColor = (255, 255, 0)
    data.pinkColor = (255,200,200)
    data.darkBlueColor = (0,0,128)
    data.darkRedColor = (128,0,0)
    data.darkYellowColor = (128,128,0)
    data.lightBlueColor = (20,20,175)
    data.lightYellowColor= (175,175,0)
    data.lightRedColor = (175,20,20)
    data.lightGreenColor = (20,175,20)
    data.grayColor = (185,185,185)
    data.redBlackColor = (242,73,101)
    data.rainbowColor = (0,242,255)
    data.trickeryColor = (235,235,143)
    data.transparentColor = (255,0,255)
    data.black2Color = (250,250,250)

    #different types of towers
    data.FireTowerOne=Towers('Fire',100,5,1,5,'range:100, cost:5, damage:1, fire rate:0.25s, elements: fire',['fire'],data.redColor,0,0,0,0,data)
    data.WaterTowerOne=Towers('Water',100,5,1,5,'range:100, cost:5, damage:1, fire rate:0.25s, elements: water',['water'],data.blueColor,0,0,0,0,data)
    data.LightTowerOne=Towers('Light',100,5,1,5,'range:100, cost:5, damage:1, fire rate:0.25s, elements: light',['light'],data.yellowColor,0,0,0,0,data)
    data.DarknessTowerOne=Towers('Darkness',100,5,1,5,'range:100, cost:5, damage:1, fire rate:0.25s, elements: darkness',['darkness'],data.blackColor,0,0,0,0,data)

    data.FireTowerTwo=Towers('Focused Fire',150,30,8,4,'range:150, cost:30, damage:8, fire rate:0.2s, elements: fire',['fire'],data.darkRedColor,0,2,0,0,data)
    data.WaterTowerTwo=Towers('Focused Water',150,30,8,4,'range:150, cost:30, damage:8, fire rate:0.2s, elements: water',['water'],data.darkBlueColor,2,0,0,0,data)
    data.LightTowerTwo=Towers('Focused Light',150,30,8,4,'range:150, cost:30, damage:8, fire rate:0.2s, elements: light',['light'],data.darkYellowColor,0,0,2,0,data)
    data.DarknessTowerTwo=Towers('Focused Darkness',150,30,8,4,'range:150, cost:30, damage:8, fire rate:0.2s, elements: darkness',['darkness'],data.blackColor,0,0,0,2,data)
                
    data.SteamTower=Towers('Steam',150,30,7,3,'range:150, cost:30, damage:7, fire rate:0.15s, elements: fire & water',['fire','water'],data.lightBlueColor,1,1,0,0,data)
    data.MagnifyTower=Towers('Magnify',150,30,7,3,'range:150, cost:30, damage:7, fire rate:0.15s, elements: fire & light',['fire','light'],data.lightRedColor,0,1,1,0,data)
    data.DevilTower=Towers('Devil',150,30,7,3,'range:150, cost:30, damage:7, fire rate:0.15s, elements: fire & darkness',['fire','darkness'],data.redBlackColor,0,1,0,1,data)
    data.RainbowTower=Towers('Rainbow',150,30,7,3,'range:150, cost:30, damage:7, fire rate:0.15s, elements: water & light',['water','light'],data.rainbowColor,1,0,1,0,data)
    data.PoisonTower=Towers('Poison',150,30,7,3,'range:150, cost:30, damage:7, fire rate:0.15s, elements: darkness & water',['water','darkness'],data.grayColor,1,0,0,1,data)
    data.TrickeryTower=Towers('Trickery',150,30,7,3,'range:150, cost:30, damage:7, fire rate:0.15s, elements: light & darkness',['light','darkness'],data.trickeryColor,0,0,1,1,data)

    data.LaserTower=Towers('Laser',200,60,9,2,'range:200, cost:60, damage:9, fire rate:0.1s, elements: fire & water & light',['water','light','fire'],data.grayColor,1,1,1,0,data)
    data.HailTower=Towers('Hail',200,60,9,2,'range:200, cost:60, damage:9, fire rate:0.1s, elements: fire & water & darkness',['water','darkness','fire'],data.lightBlueColor,1,1,0,1,data)
    data.FlameThrowerTower=Towers('FlameThrower',200,60,9,2,'range:200, cost:60, damage:9, fire rate:0.1s, elements: fire & darkness & light',['darkness','light','fire'],data.yellowColor,0,1,1,1,data)
    data.CorrosionTower=Towers('Corrosion',200,60,9,2,'range:200, cost:60, damage:9, fire rate:0.1s, elements: darkness & water & light',['water','light','darkness'],data.redBlackColor,1,0,1,1,data)



    #types of monsters
    data.Karak=Enemy('Karak',4,2,['fire'],data.redColor,data)
    data.Lyote=Enemy('Lyote',4,2,['water'],data.blueColor,data)
    data.SunBeam=Enemy('SunBeam',4,2,['light'],data.yellowColor,data)
    data.StealthBomber=Enemy('StealthBomber',4,2,['darkness'],data.blackColor,data)

    data.HellFyre=Enemy('HellFyre',20,5,['fire'],data.redColor,data)
    data.SeaGuardian=Enemy('SeaGuardian',20,5,['water'],data.blueColor,data)
    data.SunRay=Enemy('SunRay',20,5,['light'],data.yellowColor,data)
    data.DarkBat=Enemy('DarkBat',10,5,['darkness'],data.blackColor,data)

    data.SeaDemon=Enemy('SeaDemon',40,6,['fire','water'],data.lightBlueColor,data)
    data.Mermaid=Enemy('Mermaid',40,6,['water','light'],data.lightYellowColor,data)
    data.RagingGod=Enemy('RagingGod',40,6,['light','fire'],data.lightRedColor,data)
    data.InvisibleSlippery=Enemy('InvisibleSlippery',40,6,['darkness','water'],data.grayColor,data)

    #for last three levels
    data.Boss1=Enemy('Boss1',280,7,['neutral'],data.whiteColor,data)
    data.Boss2=Enemy('Boss2',390,7,['neutral'],data.greenColor,data)
    data.FinalBoss=Enemy('FinalBoss',500,7,['neutral'],data.blackColor,data)

    #elementals
    #for increasing level; can choose which one to summon
    data.WaterElemental1=Enemy('Water Elemental',33,4,['WATER','water'],data.blueColor,data)
    data.FireElemental1=Enemy('Fire Elemental',33,4,['FIRE','fire'],data.redColor,data)
    data.LightElemental1=Enemy('Light Elemental',33,4,['LIGHT','light'],data.yellowColor,data)
    data.DarknessElemental1=Enemy('Darkness Elemental',33,4,['DARKNESS','darkness'],data.blackColor,data)

    data.WaterElemental2=Enemy('Water Elemental 2',63,6,['WATER','water'],data.darkBlueColor,data)
    data.FireElemental2=Enemy('Fire Elemental 2',63,6,['FIRE','fire'],data.darkRedColor,data)
    data.LightElemental2=Enemy('Light Elemental 2',63,6,['LIGHT','light'],data.darkYellowColor,data)
    data.DarknessElemental2=Enemy('Darkness Elemental 2',63,6,['DARKNESS','darkness'],data.blackColor,data)

    data.WaterElemental3=Enemy('Water Elemental 3',83,7,['WATER','water'],data.redBlackColor,data)
    data.FireElemental3=Enemy('Fire Elemental 3',83,7,['FIRE','fire'],data.trickeryColor,data)
    data.LightElemental3=Enemy('Light Elemental 3',83,7,['LIGHT','light'],data.rainbowColor,data)
    data.DarknessElemental3=Enemy('Darkness Elemental 3',83,7,['DARKNESS','darkness'],data.grayColor,data)

    data.listOfNameOfMonsters=['Karak','Lyote','SunBeam','StealthBomber','HellFyre','SeaGuardian',\
    'Mermaid','RagingGod','InvisibleSlippery','Boss1','Boss2','FinalBoss']

    #waves of monsters
    data.Wave1=Wave([data.Karak,data.Lyote,data.SunBeam,data.StealthBomber],data)
    data.Wave2=Wave([data.Karak,data.Lyote,data.Lyote,data.StealthBomber,data.StealthBomber],data)
    data.Wave3=Wave([data.Karak,data.Karak,data.Lyote,data.Lyote,data.Lyote,data.StealthBomber,data.SunBeam,data.StealthBomber,data.StealthBomber],data)
    data.Wave4=Wave([data.Karak,data.Karak,data.Lyote,data.Lyote,data.Lyote,data.StealthBomber,data.Karak,data.SunBeam,data.StealthBomber,data.StealthBomber],data)
    data.Wave5=Wave([data.Karak,data.Karak,data.Lyote,data.Lyote,data.Lyote,data.StealthBomber,data.SunBeam,data.StealthBomber,data.StealthBomber,data.Karak,data.Lyote],data)
    data.Wave6=Wave([data.Karak,data.Karak,data.Lyote,data.Lyote,data.Lyote,data.StealthBomber,data.SunBeam,data.StealthBomber,data.StealthBomber,data.Karak,data.Lyote,data.Karak],data)
    data.Wave7=Wave([data.HellFyre,data.SeaGuardian,data.SunRay,data.DarkBat],data)
    data.Wave8=Wave([data.HellFyre,data.SeaGuardian,data.SunRay,data.DarkBat,data.SeaGuardian],data)
    data.Wave9=Wave([data.DarkBat,data.HellFyre,data.SeaGuardian,data.SunRay,data.DarkBat,data.HellFyre,data.SunRay],data)
    data.Wave10=Wave([data.DarkBat,data.HellFyre,data.SeaGuardian,data.SunRay,data.DarkBat,data.HellFyre,data.SunRay,data.DarkBat,data.HellFyre],data)
    data.Wave11=Wave([data.SeaDemon,data.DarkBat,data.HellFyre,data.SeaGuardian,data.SunRay,data.DarkBat,data.HellFyre,data.SunRay],data)
    data.Wave12=Wave([data.SeaDemon,data.DarkBat,data.HellFyre,data.SeaGuardian,data.DarkBat,data.SunRay,data.DarkBat,data.HellFyre,data.SunRay],data)
    data.Wave13=Wave([data.SeaDemon,data.DarkBat,data.HellFyre,data.SeaGuardian,data.DarkBat,data.SunRay,data.InvisibleSlippery],data)
    data.Wave14=Wave([data.SeaDemon,data.InvisibleSlippery,data.Mermaid,data.SeaDemon,data.RagingGod,data.RagingGod,data.InvisibleSlippery],data)
    data.Wave15=Wave([data.SeaDemon,data.InvisibleSlippery,data.Mermaid,data.SeaDemon,data.RagingGod,data.RagingGod,data.InvisibleSlippery,data.SeaDemon],data)
    data.Wave16=Wave([data.Boss1],data)
    data.Wave17=Wave([data.Boss2],data)
    data.Wave18=Wave([data.Boss1,data.Boss2],data)
    data.Wave19=Wave([data.Boss2,data.Boss2,data.Boss2],data)
    data.Wave20=Wave([data.FinalBoss,data.FinalBoss],data)


    

    #LOAD ALL IMAGES HERE FOR MAIN GAME
    #images for monsters
    data.monster1 = pygame.image.load('monsterpictures/monster1.jpg')
    data.monster2 = pygame.image.load('monsterpictures/monster2.jpg')
    data.monster3 = pygame.image.load('monsterpictures/monster3.jpg')
    data.monster4 = pygame.image.load('monsterpictures/monster4.jpg')
    data.monster5 = pygame.image.load('monsterpictures/monster5.gif')
    data.monster6 = pygame.image.load('monsterpictures/monster6.jpg')
    data.monster7 = pygame.image.load('monsterpictures/monster7.gif')
    data.monster8 = pygame.image.load('monsterpictures/monster8.png')
    data.monster9 = pygame.image.load('monsterpictures/monster9.png')
    data.monster10 = pygame.image.load('monsterpictures/monster10.jpg')
    data.monster11 = pygame.image.load('monsterpictures/monster11.jpg')
    data.monster12 = pygame.image.load('monsterpictures/monster12.jpg')
    data.boss1 = pygame.image.load('monsterpictures/boss1.jpg')
    data.boss2 = pygame.image.load('monsterpictures/boss2.gif')
    data.finalboss = pygame.image.load('monsterpictures/finalboss.png')
    #images of elementals
    data.water1 = pygame.image.load('monsterpictures/water1.jpg')
    data.water2 = pygame.image.load('monsterpictures/water2.jpg')
    data.water3 = pygame.image.load('monsterpictures/water3.jpg')
    data.fire1 = pygame.image.load('monsterpictures/fire1.jpg')
    data.fire2 = pygame.image.load('monsterpictures/fire2.jpg')
    data.fire3 = pygame.image.load('monsterpictures/fire3.png')
    data.dark1 = pygame.image.load('monsterpictures/dark1.jpg')
    data.dark2 = pygame.image.load('monsterpictures/dark2.jpg')
    data.dark3 = pygame.image.load('monsterpictures/dark3.jpg')
    data.light1 = pygame.image.load('monsterpictures/light1.jpg')
    data.light2 = pygame.image.load('monsterpictures/light2.jpg')
    data.light3 = pygame.image.load('monsterpictures/light3.gif')
    #images of towers
    data.fireTower = pygame.image.load('towers/firetower1.png')
    data.focusedfireTower = pygame.image.load('towers/firetower2.jpg')
    data.waterTower = pygame.image.load('towers/watertower1.jpg')
    data.focusedwaterTower = pygame.image.load('towers/watertower2.jpg')
    data.lightTower = pygame.image.load('towers/lighttower1.jpg')
    data.focusedlightTower = pygame.image.load('towers/lighttower2.jpg')
    data.darknessTower = pygame.image.load('towers/darknesstower1.jpg')
    data.focuseddarknessTower = pygame.image.load('towers/darknesstower2.jpg')
    data.steamTower = pygame.image.load('towers/steamtower.jpg')
    data.magnifyTower = pygame.image.load('towers/magnifytower.png')
    data.devilTower = pygame.image.load('towers/devil.png')
    data.rainbowTower = pygame.image.load('towers/rainbowtower.jpg')
    data.poisonTower = pygame.image.load('towers/poisontower.png')
    data.trickeryTower = pygame.image.load('towers/trickerytower.jpg')
    data.laserTower = pygame.image.load('towers/lasertower.png')
    data.hailTower = pygame.image.load('towers/hailtower.jpg')
    data.flamethrowerTower = pygame.image.load('towers/flamethrowertower.jpg')
    data.corrosionTower = pygame.image.load('towers/corrosivetower.jpg')



    data.tileUp = pygame.image.load('tiles/tileup.png')
    data.tileDown = pygame.image.load('tiles/tiledown.png')
    data.tileLeft = pygame.image.load('tiles/tileleft.png')
    data.tileRight = pygame.image.load('tiles/tileright.png')
    data.tileStart = pygame.image.load('tiles/tilestart.png')
    data.tileExit = pygame.image.load('tiles/tileexit.png')
    data.tile = pygame.image.load('tiles/tile.jpg')


    data.LIGHT = pygame.image.load('images/LIGHT.png')
    data.DARKNESS = pygame.image.load('images/DARKNESS.png')
    data.WATER = pygame.image.load('images/WATER.png')
    data.FIRE = pygame.image.load('images/FIRE.png')

    data.lightBarImage = pygame.image.load('images/lightbarimage.png')
    data.darknessBarImage = pygame.image.load('images/darknessbarimage.png')
    data.fireBarImage = pygame.image.load('images/firebarimage.png')
    data.waterBarImage = pygame.image.load('images/waterbarimage.png')
    data.dragon1 = pygame.image.load('images/dragon1.png')
    data.dragon2 = pygame.image.load('images/dragon2.png')
    data.dragon3 = pygame.image.load('images/dragon3.png')

    #for easier refence in etd file
    data.dictionaryForBlittingMonster = {'Karak':(data.monster1,data.whiteColor),'Lyote':(data.monster2,data.whiteColor),'Sunbeam':(data.monster3,data.whiteColor),\
    'StealthBomber':(data.monster4,data.whiteColor),'HellFyre':(data.monster5,data.whiteColor),'SeaGuardian':(data.monster6,data.whiteColor),\
    'SunRay':(data.monster7,data.whiteColor),'DarkBat':(data.monster8,data.whiteColor),'SeaDemon':(data.monster9,data.whiteColor),\
    'Mermaid':(data.monster10,data.whiteColor),'RagingGod':(data.monster11,data.whiteColor),'InvisibleSlippery':(data.monster12,data.whiteColor),\
    'Boss1':(data.boss1,data.whiteColor),'Boss2':(data.boss2,data.whiteColor),'FinalBoss':(data.finalboss,data.whiteColor),\
    'Water Elemental':(data.water1,data.whiteColor),'Water Elemental 2':(data.water2,data.whiteColor),'Water Elemental 3':(data.water3,data.whiteColor),\
    'Fire Elemental':(data.fire1,data.whiteColor),'Fire Elemental 2':(data.fire2,data.whiteColor),'Fire Elemental 3':(data.fire3,data.whiteColor),\
    'Light Elemental':(data.light1,data.whiteColor),'Light Elemental 2':(data.light2,data.whiteColor),'Light Elemental 3':(data.light3,data.whiteColor),\
    'Darkness Elemental':(data.dark1,data.whiteColor),'Darkness Elemental 2':(data.dark2,data.whiteColor),'Darkness Elemental 3':(data.dark3,data.whiteColor)}

    #for easier refence in etd file
    data.dictionaryForBlittingTowers = {'Fire':(data.fireTower,data.blackColor),'Focused Fire':(data.focusedfireTower,data.blackColor),\
        'Water':(data.waterTower,data.whiteColor),'Focused Water':(data.focusedwaterTower,data.whiteColor),\
        'Light':(data.lightTower,data.whiteColor),'Focused Light':(data.focusedlightTower,data.whiteColor),\
        'Darkness':(data.darknessTower,data.whiteColor),'Focused Darkness':(data.focuseddarknessTower,data.whiteColor),\
        'Steam':(data.steamTower,data.blackColor),'Magnify':(data.magnifyTower,data.whiteColor),\
        'Devil':(data.devilTower,data.whiteColor),'Rainbow':(data.rainbowTower,data.blackColor),\
        'Poison':(data.poisonTower,data.whiteColor),'Trickery':(data.trickeryTower,(117,117,117)),\
        'Laser':(data.laserTower,data.whiteColor),'Hail':(data.hailTower,data.blackColor),\
        'FlameThrower':(data.flamethrowerTower,data.blackColor),'Corrosion':(data.corrosionTower,data.blackColor)}