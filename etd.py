import pygame,sys #import a library of functions called 'pygame'
from pygame.locals import *
import random

from classes import *
from init2 import *


#####################################################################
#barebones which includes mouse&key pressed,timerfired,redrawAll
#####################################################################


def mousePressed(event, data):
    #gets the position of the mouse clicked in the screen
    if event.type == MOUSEBUTTONDOWN:
        data.mouseClickX,data.mouseClickY = event.pos
    if data.mode == "Running":
        redrawAll(data)

def keyPressed(event, data):
    if event.key == K_ESCAPE:#quits by pressing escape
        pygame.event.post(pygame.event.Event(QUIT))
    if event.key == K_m: #to mute music
        data.musicCounter+=1
        if data.musicCounter%2!=0:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
    if event.key == K_p:#to pause game
        if data.mode == 'Running':
            if data.pause == False:
                data.pause = True
                data.backgroundMusic.stop()
                data.introMusic=pygame.mixer.Sound("music/dream.wav")#play background song
                data.introMusic.play(-1)
                if data.musicCounter%2!=0:
                    pygame.mixer.pause()
        if data.mode == 'Paused':
            if data.pause == True:
                data.pause = False
                data.introMusic.stop()
                data.backgroundMusic.play(-1)
                if data.musicCounter%2!=0:
                    pygame.mixer.pause()
    if event.key == K_r:#restarts game
        if data.gameOverLose==True:
            data.gameOverLose = False
            data.gameOverLoseSound.stop()
            data.backgroundMusic.play(-1)
            if data.musicCounter%2!=0:
                pygame.mixer.pause()
        elif data.gameOverWin==True:
            data.gameOverWin = False
            data.gameOverWinSound.stop()
            data.backgroundMusic.play(-1)
            if data.musicCounter%2!=0:
                pygame.mixer.pause()
        if data.musicCounter%2!=0:
            pygame.mixer.pause()
        data.mode = 'Running'
        initInitial(data)
        init(data)   
    if data.mode=='Running':
        if event.key == K_SPACE:#resets if tower chosen wrongly
            data.placePureTower=False
            data.selectedPureTowerToDraw=False
            data.placeDualTower=False
            data.selectedDualTowerToDraw=False
            data.placeTripleTower=False
            data.selectedTripleTowerToDraw=False
        if event.key == K_w: #shortcut to win
            data.mode = 'Done'
            data.gameOverWin = True
        if event.key == K_l:#shortcut to lose
            data.mode = 'Done'
            data.gameOverLose = True
        if event.key == K_BACKSLASH:#cheat
            data.playerMoney=10000
            data.waterLevel = 2
            data.fireLevel = 2
            data.lightLevel = 2
            data.darknessLevel = 2
        if event.key == K_s:#sell towers mode
            if data.sellMode==False:
                data.sellMode = True
                data.mouseClickXUP=None
                data.mouseClickYUP=None
            else:
                data.sellMode=False
    if data.mode == "Running":
        redrawAll(data)

def timerFired(data):#different redrawAll called based on game mode
    data.clock.tick(50)
    if data.mode=='Intro':
        redrawAll2(data)
        data.introCounter+=1
    elif data.mode=='Running':
        redrawAll(data)
        data.timerCounter+=1#counter for updating the monsters
        data.timerCounter2+=0.1#counter for drawing the dragon
        if data.timerCounter%10==0:
            data.imageCounter+=1
        data.monstersList.update(data)#calls update on monster
        data.turretsList.update(data)#calls update on the turrets
        for bullet in data.bulletsList:
            if data.timerCounter%bullet.ratecounter==0:   
                data.bulletsList.update(data)#updates bullet movement 
        data.spritesList.update(data)#update all the sprites as well
    elif data.mode =='Paused':
        redrawAll3(data)
    elif data.mode == 'Done':
        data.endCounter +=1
        gameOver(data)
    elif data.mode == 'Exit':
        exit(data)
        data.endCounter +=1
        if data.x2==600:#if the image has closed back
            pygame.event.post(pygame.event.Event(QUIT))
        pygame.display.flip()
    data.mouseX,data.mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            data.mode = "Done"
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousePressed(event, data)
        elif (event.type == pygame.MOUSEBUTTONUP):
            data.mouseClickXUP,data.mouseClickYUP = event.pos
        elif (event.type == pygame.KEYDOWN):
            keyPressed(event,data)

def redrawAll(data):
    data.spritesList.draw(data.screen)#draw all sprites everytime with this
    flyingDragon(data)#redraw dragon
    pygame.display.flip()#updates data.screen


#####################################################################
#prints path and grid onto screen
#####################################################################

def printGrid(data):#uses tile image of grass and blits it onto screen
    counter=0
    for row in xrange(16):
        for col in xrange(24):
            image = pygame.transform.scale(data.tile,(50,50)).convert()
            data.screen.blit(image,(col*50,row*50))
            counter+=1

def printPath(data):
    #uses hard coded [row][col] values based on the 2d list which is initialised
    #to find which directional tile is needed
    for row in xrange(len(data.monsterPath)):
        for col in xrange(len(data.monsterPath[0])):
            (x,y) = (col*50,row*50)
            (xcord,ycord) = (((x/50)*50),((y/50)*50))
            if data.monsterPath[row][col]!=0:
                pygame.draw.rect(data.screen,data.grayColor,(xcord,ycord,50,50))
            if data.monsterPath[row][col]==1:
                image = pygame.transform.scale(data.tileStart,(50,50)).convert()
                image.set_colorkey((data.blackColor))
                data.screen.blit(image,(xcord,ycord))
            elif data.monsterPath[row][col]==42:
                image = pygame.transform.scale(data.tileExit,(50,50)).convert()
                data.screen.blit(image,(xcord,ycord))
            elif 2<=data.monsterPath[row][col]<=4 or 12<=data.monsterPath[row][col]<=15 or data.monsterPath[row][col]==22:
                image = pygame.transform.scale(data.tileDown,(50,50)).convert()
                data.screen.blit(image,(xcord,ycord))
            elif 33<=data.monsterPath[row][col]<=41: 
                image = pygame.transform.scale(data.tileUp,(50,50)).convert()
                data.screen.blit(image,(xcord,ycord))
            elif 5<=data.monsterPath[row][col]<=11 or 23<=data.monsterPath[row][col]<=32: 
                image = pygame.transform.scale(data.tileRight,(50,50)).convert()
                data.screen.blit(image,(xcord,ycord))
            elif 16<=data.monsterPath[row][col]<=21: 
                image = pygame.transform.scale(data.tileLeft,(50,50)).convert()
                data.screen.blit(image,(xcord,ycord))
    #in between each tile is a gray colored line running through           
    for col in xrange(24):
        pygame.draw.line(data.screen,data.grayColor,(col*50,0),(col*50,8*100),4)    
    for row in xrange(16):
        pygame.draw.line(data.screen,data.grayColor,(0,row*50),(12*100,row*50),4)


#####################################################################
#monsters and wave
#####################################################################


def hardMode(data):
    #if player selects hard mode, the wave comes after 25 seconds, thus the magic number
    if data.time==0:
        if data.wave%3==0:#depending on wave number, give a elemental charge(per 3 waves)
            data.ELEMENTAL+=1
        addMonsters(data)
        data.mouseClickX=None
        data.mouseClickY=None
        data.wave+=1
        data.time=25

def callWave(data): 
    #if it is on easy mode, player manually calls the wave by clicking on the word 'wave'
    #the word is clicked by being the range of the following magic numbers
    #click to sumon next wave
    #20 is total number of waves
    if (710<=data.mouseClickX<=810) and (110<=data.mouseClickY<=150) and data.wave<20 and len(data.monstersList)==0:
        if data.wave%3==0:#depending on wave number, give a elemental charge(per 3 waves)
            data.ELEMENTAL+=1
        addMonsters(data)
        data.mouseClickX=None
        data.mouseClickY=None
        data.wave+=1

def viewWaveMonsters(data):
    #enables player to view the health and elements of the monsters
    #in the next wave when cursor is over the word wave
    #20 is total number of waves
    if (710<=data.mouseX<=810) and (110<=data.mouseY<=150) and data.wave<20:
        currentWaveList = (data.Waves[data.wave]).list
        (xcord,ycord)=(10,740)
        for x in currentWaveList:
            elements=''
            newelements=''
            hp=''
            #format the strings 
            hp+=str(x.health)
            elements+=str(tuple(x.element)).rstrip(',)') + ')'
            newelements=elements.replace("'","")
            for monster in data.dictionaryForBlittingMonster:#get the monster picture
                if x.name==monster: #blits the monster image at the bottom
                    image = pygame.transform.scale(data.dictionaryForBlittingMonster[monster][0],(50,50)).convert()
                    image.set_colorkey((data.dictionaryForBlittingMonster[monster][1]))
            data.screen.blit(image,(xcord,ycord))
            font2 = pygame.font.SysFont('arialnarow', 30)
            health = font2.render('%s'%hp,True,data.blackColor)
            data.screen.blit(health,(xcord+15,720))
            font5 = pygame.font.SysFont('arialnarow', 20)
            description = font5.render('%s'%newelements,True,data.blackColor)
            data.screen.blit(description,(xcord,700))
            xcord+=100#evenly spaced out monsters since at most there are 10 monsters
        data.mouseX = None
        data.mouseY = None


def addMonsters(data):
    #when a wave is called either way, this adds it to the sprite group 
    #to be updated
    counter=0
    #get all the info to be added to the monster sprite
    for x in xrange(len((data.Waves[data.wave]).list)):
        health = ((data.Waves[data.wave]).list)[counter].health
        color = ((data.Waves[data.wave]).list)[counter].color
        element = ((data.Waves[data.wave]).list)[counter].element
        speed = ((data.Waves[data.wave]).list)[counter].vectorspeed
        name = ((data.Waves[data.wave]).list)[counter].name
        monster = Monster(60,x*-100,health,color,element,speed,name,data)
        data.spritesList.add(monster)
        data.monstersList.add(monster)
        counter+=1

def monstersReachBase(data): #if monster ends to other side, decrease 1 life
    for monster in data.monstersList:
        if 607<=monster.rect.x<=635 and monster.rect.y<1:
            data.playerLife-=1
            data.spritesList.remove(monster)
            data.monstersList.remove(monster)

#####################################################################
#shooting monsters
#####################################################################

def shootMonsters(data):
    #this checks if monsters are in range
    #if they are within turret.range, the turret create bullet sprites in that direction
    if len(data.monstersList)!=0 and len(data.turretsList)!=0:
        for monster in data.monstersList:
            for turret in data.turretsList:
                if (0<=monster.rect.x<700) and (0<=monster.rect.y<550):
                    if ((monster.rect.x - turret.rect.x)**2 + (monster.rect.y - turret.rect.y)**2)**0.5<=turret.range:
                        x=max((abs(monster.rect.x - turret.rect.x)),(abs(monster.rect.y - turret.rect.y)))
                        xcol=round(((monster.rect.x - turret.rect.x)/float(x)),2)
                        ycol=round(((monster.rect.y - turret.rect.y)/float(x)),2)
                        bullet = Bullet(turret.rect.x+25.0,turret.rect.y+25.0,xcol,ycol,turret.damage,turret.range,turret.rate,turret.element,data)
                        sound=pygame.mixer.Sound("music/laser.wav")
                        if data.musicCounter%2==0:
                            sound.play()
                        data.bulletsList.add(bullet)
                        data.spritesList.add(bullet)

def ifMonsterHitOrBulletOB(data):
    #this function checks if:
    #1)bullet goes out of bounds of 
    #2)if it hits, whether they are of different elements
    #3)if monster has 0 hp, it dies and disappears
        for bullet in data.bulletsList: 
            monsterHitList = pygame.sprite.spritecollide(bullet, data.monstersList, False)
            for element in bullet.element:
                for monster in monsterHitList:
                    if element in monster.element:
                        monster.health+=bullet.damage#if of same element, makes monster stronger
                    monster.health-=bullet.damage
            for monster in monsterHitList:
                if monster.health<=0:
                    if data.musicCounter%2==0:
                        sound2=pygame.mixer.Sound("music/fart.wav")
                        sound2.play()
                    data.bulletsList.remove(bullet)
                    data.spritesList.remove(bullet)
                    data.monstersList.remove(monster)
                    data.spritesList.remove(monster)
                    data.playerMoney+=data.wave
                    #this checks if an elemental is killed, adds the element level for the player
                    if 'FIRE' in monster.element: #if a elemental, add to level if monster defeated
                        data.fireLevel+=1
                    elif 'WATER' in monster.element:  
                        data.waterLevel+=1
                    elif 'LIGHT' in monster.element: 
                        data.lightLevel+=1
                    elif 'DARKNESS' in monster.element: 
                        data.darknessLevel+=1
            # Remove the bullet if it flies up off the screen
            if bullet.rect.x > 700 or bullet.rect.y>550:
                data.bulletsList.remove(bullet)
                data.spritesList.remove(bullet)


#####################################################################
#player UI at the right and bottom
#####################################################################

def drawBar1(data):
    #draws bar at the right and updates it accordingly
    pygame.draw.rect(data.screen,data.black2Color,(700,0,500,550))
    font = pygame.font.SysFont('calibri', 40)
    playerLife = font.render('Life: %s'%data.playerLife,True,data.blackColor)
    data.screen.blit(playerLife,(710,10))
    playerMoney = font.render('Gold: %s'%data.playerMoney,True,data.blackColor)
    data.screen.blit(playerMoney,(710,60))
    wave = font.render('Wave: %s'%data.wave,True,data.blackColor)
    data.screen.blit(wave,(710,110))
    font3 = pygame.font.SysFont('silom', 40)
    towers = font3.render('TOWERS',True,data.blackColor)
    data.screen.blit(towers,(850,300))
    font4 = pygame.font.SysFont('silom', 30)
    pureTowers = font4.render('Pures',True,data.blackColor)
    data.screen.blit(pureTowers,(710,350))
    dualTowers = font4.render('Duals',True,data.blackColor)
    data.screen.blit(dualTowers,(870,350))
    tripleTowers = font4.render('Triples',True,data.blackColor)
    data.screen.blit(tripleTowers,(1030,350))
    font5 = pygame.font.SysFont('trebuchetms', 50)
    elementals = font5.render('CHARGE: %s'%data.ELEMENTAL,True,data.blackColor)
    data.screen.blit(elementals,(800,420))
    if data.timerCounter%20==0:
        if data.time>0 and len(data.monstersList)==0:
            data.time-=1
    if data.playHardMode ==  True: 
        if data.time>0:
            time = font5.render('Time: %d'%data.time,True,data.blackColor)
            data.screen.blit(time,(820,480))
        else:
            time = font5.render('Time: %d'%data.time,True,data.redColor)
            data.screen.blit(time,(820,480))
    #elemental box images
    image = pygame.transform.scale(data.FIRE,(100,100)).convert()
    data.screen.blit(image,(900,10))
    image2 = pygame.transform.scale(data.LIGHT,(100,100)).convert()
    data.screen.blit(image2,(1050,10))
    image3 = pygame.transform.scale(data.DARKNESS,(100,100)).convert()
    data.screen.blit(image3,(900,160))
    image4 = pygame.transform.scale(data.WATER,(100,100)).convert()
    data.screen.blit(image4,(1050,160))
    #elemental level blitting onto image
    font2 = pygame.font.SysFont('arialbold', 60)
    firenumber = font2.render('%s'%(data.fireLevel),True,data.whiteColor)
    data.screen.blit(firenumber,(939,45))
    waternumber = font2.render('%s'%(data.waterLevel),True,data.whiteColor)
    data.screen.blit(waternumber,(1090,195))
    darknessnumber = font2.render('%s'%(data.darknessLevel),True,data.whiteColor)
    data.screen.blit(darknessnumber,(939,195))
    lightnumber = font2.render('%s'%(data.lightLevel),True,data.whiteColor)
    data.screen.blit(lightnumber,(1090,45))
    #blits the charge onto screen
    #it flashes if more than 0
    if data.ELEMENTAL>0:
        if data.imageCounter%2==0:
            font5 = pygame.font.SysFont('trebuchetms', 50)
            elementals = font5.render('CHARGE: %s'%data.ELEMENTAL,True,data.blackColor)
        else:
            elementals = font5.render('CHARGE: %s'%data.ELEMENTAL,True,data.redColor)
        data.screen.blit(elementals,(800,420))



def drawBar2(data):
    #the different selections for the 
    #diferrent kind of towers
    pygame.draw.rect(data.screen,data.whiteColor,(0,550,1200,250))
    pygame.draw.line(data.screen,data.grayColor,(0,690),(1200,690),4)
    #if pure tower is clicked
    if (710<=data.mouseClickX<=800) and (350<=data.mouseClickY<=380):
        data.pureTowersBar = True
        data.dualTowersBar = False
        data.tripleTowersBar = False
        data.mouseClickX=None#resets the mouse event
        data.mouseClickY=None
        data.waterBar = False
        data.fireBar = False
        data.lightBar = False
        data.darknessBar = False
    #if duals clicked
    elif (870<=data.mouseClickX<=956) and (350<=data.mouseClickY<=380):
        data.pureTowersBar = False
        data.dualTowersBar = True
        data.tripleTowersBar = False
        data.elementalBar = False
        data.mouseClickX=None
        data.mouseClickY=None
        data.waterBar = False
        data.fireBar = False
        data.lightBar = False
        data.darknessBar = False
    elif (1030<=data.mouseClickX<=1135) and (350<=data.mouseClickY<=380):
        data.pureTowersBar = False
        data.dualTowersBar = False
        data.tripleTowersBar = True
        data.elementalBar = False
        data.mouseClickX=None
        data.mouseClickY=None
        data.waterBar = False
        data.fireBar = False
        data.lightBar = False
        data.darknessBar = False
       



#####################################################################
#towers PURE
#####################################################################

def drawPureTowersBar(data):
    listOfTowers=[]#stores coordinates of towers
    if data.pureTowersBar == True:
        xcord=10#preset coordinates for bar 2
        ycord=560
        for tower in data.pureTowers:#from list of pure towers in init
            #check which tower to blit
            for towers in data.dictionaryForBlittingTowers:
                if tower.name ==towers:
                    image = pygame.transform.scale(data.dictionaryForBlittingTowers[towers][0],(100,100)).convert()
                    image.set_colorkey((data.dictionaryForBlittingTowers[towers][1]))
            data.screen.blit(image,(xcord,ycord))
            listOfTowers+=[(xcord,xcord+100,ycord,ycord+100)]
            xcord+=150#spread them out, 1200 divided by number of towers
        data.towerCounterForDrawing = 0
        for coord in xrange(len(listOfTowers)):
            (y,y1,x,x1) = listOfTowers[coord]
            if (y<=data.mouseX<=y1) and (x<=data.mouseY<=x1):#when moving mouse over it gives description
                font = pygame.font.SysFont('arialnarow', 40)
                description = font.render('%s: %s'%(data.pureTowers[data.towerCounterForDrawing].name,data.pureTowers[data.towerCounterForDrawing].description),True,data.blueColor)
                data.screen.blit(description,(10,700))#shows at bottom of screen
                if data.pureTowers[data.towerCounterForDrawing].water>data.waterLevel or data.pureTowers[data.towerCounterForDrawing].fire>data.fireLevel or data.pureTowers[data.towerCounterForDrawing].darkness>data.darknessLevel or data.pureTowers[data.towerCounterForDrawing].light>data.lightLevel:
                    color = data.redColor#check if player elements' level is enough to purchase tower, if no, red color font
                else:
                    color = data.grayColor
                description2 = font.render('Elemental Level needed: Fire: %d, Water: %d, Light: %d, Darkness: %d\
                '%(data.pureTowers[data.towerCounterForDrawing].fire,data.pureTowers[data.towerCounterForDrawing].water,\
                data.pureTowers[data.towerCounterForDrawing].light,data.pureTowers[data.towerCounterForDrawing].darkness),True,color)
                data.screen.blit(description2,(10,750))#shows at bottom of screen
            data.cost = data.pureTowers[data.towerCounterForDrawing].cost
            water = data.pureTowers[data.towerCounterForDrawing].water
            fire = data.pureTowers[data.towerCounterForDrawing].fire
            light = data.pureTowers[data.towerCounterForDrawing].light
            darkness = data.pureTowers[data.towerCounterForDrawing].darkness
            if (y<=data.mouseClickX<=y1) and (x<=data.mouseClickY<=x1) and data.cost<=data.playerMoney:#if selected conditions
                if data.waterLevel>=water and data.fireLevel>=fire and data.lightLevel>=light and data.darknessLevel>=darkness:
                    data.selectedPureTowerToDraw = True#value set to true
                    data.mouseClickX = None
                    data.mouseClickY = None
                    data.selectedTowerCounter = data.towerCounterForDrawing
            data.towerCounterForDrawing+=1#goes through every tower based on index in the list

def drawTowerOnMouse(data):
    #for selected tower(if conditions met), draw it at mouse position center with its range 
    if data.selectedPureTowerToDraw == True:
        tower = data.pureTowers[data.selectedTowerCounter]
        for towers in data.dictionaryForBlittingTowers:
                if tower.name ==towers:
                    image = pygame.transform.scale(data.dictionaryForBlittingTowers[towers][0],(50,50)).convert()
                    image.set_colorkey((data.dictionaryForBlittingTowers[towers][1]))
        data.screen.blit(image,(data.mouseX-25,data.mouseY-25))
        pygame.draw.circle(data.screen,data.redColor,(data.mouseX,data.mouseY),data.pureTowers[data.selectedTowerCounter].range,1)
        if (0<=data.mouseClickX<700) and (0<=data.mouseClickY<550):#checks if it is going to be placed in path
            if not ((50<=data.mouseClickX<=100) and (0<=data.mouseClickY<=250)):
                if not ((100<=data.mouseClickX<=450) and (200<=data.mouseClickY<=250)):
                     if not ((400<=data.mouseClickX<=450) and (250<=data.mouseClickY<=450)):
                        if not ((100<=data.mouseClickX<=400) and (400<=data.mouseClickY<=450)):
                            if not ((100<=data.mouseClickX<=650) and (450<=data.mouseClickY<=500)):
                                if not ((600<=data.mouseClickX<=650) and (0<=data.mouseClickY<=500)):
                                    (xcord,ycord) = (((data.mouseClickX/50)*50),((data.mouseClickY/50)*50))
                                    if (xcord,ycord) not in data.coordListOfTurrets:
                                        if (data.waterLevel + data.fireLevel + data.lightLevel + data.darknessLevel)<5:
                                            if not (xcord==350 and ycord==300):   
                                                data.placePureTower = True#ready to place it
                                        else:
                                            data.placePureTower = True

def placeTower(data):
    #adds tower to location selected on map
    #uses info to add to sprite class
    if data.placePureTower==True:
        (xcord,ycord) = (((data.mouseClickX/50)*50),((data.mouseClickY/50)*50))#finds the grid for it
        data.towercoord+=[(xcord,ycord,data.pureTowers[data.selectedTowerCounter].color,\
            data.pureTowers[data.selectedTowerCounter].bulletdamage,\
            data.pureTowers[data.selectedTowerCounter].range,\
            data.pureTowers[data.selectedTowerCounter].cost,\
            data.pureTowers[data.selectedTowerCounter].timer,\
            data.pureTowers[data.selectedTowerCounter].description,\
            data.pureTowers[data.selectedTowerCounter].element,\
            data.pureTowers[data.selectedTowerCounter].name)]
        data.placePureTower=False
        data.selectedPureTowerToDraw=False
        data.playerMoney-= data.pureTowers[data.selectedTowerCounter].cost
        data.cost=0



#for all three kinds of towers
def drawTowersOnMap(data):
    for tower in xrange(len(data.towercoord)):
        (xcord,ycord,color,damage,range,cost,rate,description,element,name)=data.towercoord[tower]
        data.coordListOfTurrets += [(xcord,ycord)]
        turret = Turrets(xcord,ycord,color,damage,range,cost,rate,description,element,name,data)
        data.spritesList.add(turret)#add to sprite list
        data.turretsList.add(turret)#add to sprite list
    data.towercoord = []#resets after talking in data


#####################################################################
#towers DUAL similar to PURES
#####################################################################

def drawDualTowersBar(data):
    listOfTowers=[]
    if data.dualTowersBar == True:
        xcord=10
        ycord=560
        for tower in data.dualTowers:#from list of pure towers in init
            #check which tower to blit
            for towers in data.dictionaryForBlittingTowers:
                if tower.name ==towers:
                    image = pygame.transform.scale(data.dictionaryForBlittingTowers[towers][0],(100,100)).convert()
                    image.set_colorkey((data.dictionaryForBlittingTowers[towers][1]))
            data.screen.blit(image,(xcord,ycord))
            listOfTowers+=[(xcord,xcord+100,ycord,ycord+100)]
            xcord+=200#1200 divided by number of towers
        data.towerCounterForDrawing = 0
        for coord in xrange(len(listOfTowers)):
            (y,y1,x,x1) = listOfTowers[coord]
            if (y<=data.mouseX<=y1) and (x<=data.mouseY<=x1):
                font = pygame.font.SysFont('arialnarow', 40)
                description = font.render('%s: %s'%(data.dualTowers[data.towerCounterForDrawing].name,data.dualTowers[data.towerCounterForDrawing].description),True,data.blueColor)
                data.screen.blit(description,(10,700))
                if data.dualTowers[data.towerCounterForDrawing].water>data.waterLevel or data.dualTowers[data.towerCounterForDrawing].fire>data.fireLevel or data.dualTowers[data.towerCounterForDrawing].darkness>data.darknessLevel or data.dualTowers[data.towerCounterForDrawing].light>data.lightLevel:
                    color = data.redColor
                else:
                    color = data.grayColor
                description2 = font.render('Elemental Level needed: Fire: %d, Water: %d, Light: %d, Darkness: %d\
                '%(data.dualTowers[data.towerCounterForDrawing].fire,data.dualTowers[data.towerCounterForDrawing].water,\
                data.dualTowers[data.towerCounterForDrawing].light,data.dualTowers[data.towerCounterForDrawing].darkness),True,color)
                data.screen.blit(description2,(10,750))#shows at bottom of screen
            data.cost = data.dualTowers[data.towerCounterForDrawing].cost
            water = data.dualTowers[data.towerCounterForDrawing].water
            fire = data.dualTowers[data.towerCounterForDrawing].fire
            light = data.dualTowers[data.towerCounterForDrawing].light
            darkness = data.dualTowers[data.towerCounterForDrawing].darkness
            if (y<=data.mouseClickX<=y1) and (x<=data.mouseClickY<=x1) and data.cost<=data.playerMoney:
                if data.waterLevel>=water and data.fireLevel>=fire and data.lightLevel>=light and data.darknessLevel>=darkness:
                    data.selectedDualTowerToDraw = True
                    data.mouseClickX = None
                    data.mouseClickY = None
                    data.selectedTowerCounter = data.towerCounterForDrawing
            data.towerCounterForDrawing+=1

def drawTowerOnMouseDual(data):
    if data.selectedDualTowerToDraw == True:
        tower = data.dualTowers[data.selectedTowerCounter]
        for towers in data.dictionaryForBlittingTowers:
                if tower.name ==towers:
                    image = pygame.transform.scale(data.dictionaryForBlittingTowers[towers][0],(50,50)).convert()
                    image.set_colorkey((data.dictionaryForBlittingTowers[towers][1]))
        data.screen.blit(image,(data.mouseX-25,data.mouseY-25))#causes tower to be at centre of mouse
        pygame.draw.circle(data.screen,data.redColor,(data.mouseX,data.mouseY),data.dualTowers[data.selectedTowerCounter].range,1)
        if (0<=data.mouseClickX<700) and (0<=data.mouseClickY<550):#checks if it is going to be placed in path
            if not ((50<=data.mouseClickX<=100) and (0<=data.mouseClickY<=250)):
                if not ((100<=data.mouseClickX<=450) and (200<=data.mouseClickY<=250)):
                     if not ((400<=data.mouseClickX<=450) and (250<=data.mouseClickY<=450)):
                        if not ((100<=data.mouseClickX<=400) and (400<=data.mouseClickY<=450)):
                            if not ((100<=data.mouseClickX<=650) and (450<=data.mouseClickY<=500)):
                                if not ((600<=data.mouseClickX<=650) and (0<=data.mouseClickY<=500)):
                                    (xcord,ycord) = (((data.mouseClickX/50)*50),((data.mouseClickY/50)*50))
                                    if (xcord,ycord) not in data.coordListOfTurrets:   
                                        if (data.waterLevel + data.fireLevel + data.lightLevel + data.darknessLevel)<5:
                                            #checks for the dragon box
                                            if not (xcord==350 and ycord==300):   
                                                data.placeDualTower = True#ready to place it
                                        else:
                                            data.placeDualTower = True


def placeTowerDual(data):
    if data.placeDualTower==True:
        (xcord,ycord) = (((data.mouseClickX/50)*50),((data.mouseClickY/50)*50))#finds the grid for it
        data.towercoord+=[(xcord,ycord,data.dualTowers[data.selectedTowerCounter].color,\
            data.dualTowers[data.selectedTowerCounter].bulletdamage,\
            data.dualTowers[data.selectedTowerCounter].range,\
            data.dualTowers[data.selectedTowerCounter].cost,\
            data.dualTowers[data.selectedTowerCounter].timer,\
            data.dualTowers[data.selectedTowerCounter].description,\
            data.dualTowers[data.selectedTowerCounter].element,\
            data.dualTowers[data.selectedTowerCounter].name)]
        data.placeDualTower=False
        data.selectedDualTowerToDraw=False
        data.playerMoney-= data.dualTowers[data.selectedTowerCounter].cost
        data.cost=0

#####################################################################
#towers TRIPLE similarly...
#####################################################################

def drawTripleTowersBar(data):
    listOfTowers=[]
    if data.tripleTowersBar == True:
        xcord=10
        ycord=560
        for tower in data.tripleTowers:#from list of pure towers in init
            #check which tower to blit
            for towers in data.dictionaryForBlittingTowers:
                if tower.name ==towers:
                    image = pygame.transform.scale(data.dictionaryForBlittingTowers[towers][0],(100,100)).convert()
                    image.set_colorkey((data.dictionaryForBlittingTowers[towers][1]))
            data.screen.blit(image,(xcord,ycord))
            listOfTowers+=[(xcord,xcord+100,ycord,ycord+100)]
            xcord+=300
        data.towerCounterForDrawing = 0
        for coord in xrange(len(listOfTowers)):
            (y,y1,x,x1) = listOfTowers[coord]
            if (y<=data.mouseX<=y1) and (x<=data.mouseY<=x1):
                font = pygame.font.SysFont('arialnarow', 38)
                description = font.render('%s: %s'%(data.tripleTowers[data.towerCounterForDrawing].name,data.tripleTowers[data.towerCounterForDrawing].description),True,data.blueColor)
                data.screen.blit(description,(10,700))
                if data.tripleTowers[data.towerCounterForDrawing].water>data.waterLevel or data.tripleTowers[data.towerCounterForDrawing].fire>data.fireLevel or data.tripleTowers[data.towerCounterForDrawing].darkness>data.darknessLevel or data.tripleTowers[data.towerCounterForDrawing].light>data.lightLevel:
                    color = data.redColor
                else:
                    color = data.grayColor
                description2 = font.render('Elemental Level needed: Fire: %d, Water: %d, Light: %d, Darkness: %d\
                '%(data.tripleTowers[data.towerCounterForDrawing].fire,data.tripleTowers[data.towerCounterForDrawing].water,\
                data.tripleTowers[data.towerCounterForDrawing].light,data.tripleTowers[data.towerCounterForDrawing].darkness),True,color)
                data.screen.blit(description2,(10,750))#shows at bottom of screen
            data.cost = data.tripleTowers[data.towerCounterForDrawing].cost
            water = data.tripleTowers[data.towerCounterForDrawing].water
            fire = data.tripleTowers[data.towerCounterForDrawing].fire
            light = data.tripleTowers[data.towerCounterForDrawing].light
            darkness = data.tripleTowers[data.towerCounterForDrawing].darkness
            if (y<=data.mouseClickX<=y1) and (x<=data.mouseClickY<=x1) and data.cost<=data.playerMoney:
                if data.waterLevel>=water and data.fireLevel>=fire and data.lightLevel>=light and data.darknessLevel>=darkness:
                    data.selectedTripleTowerToDraw = True
                    data.mouseClickX = None
                    data.mouseClickY = None
                    data.selectedTowerCounter = data.towerCounterForDrawing
            data.towerCounterForDrawing+=1

def drawTowerOnMouseTriple(data):
    if data.selectedTripleTowerToDraw == True:
        tower = data.tripleTowers[data.selectedTowerCounter]
        for towers in data.dictionaryForBlittingTowers:
                if tower.name ==towers:
                    image = pygame.transform.scale(data.dictionaryForBlittingTowers[towers][0],(50,50)).convert()
                    image.set_colorkey((data.dictionaryForBlittingTowers[towers][1]))
        data.screen.blit(image,(data.mouseX-25,data.mouseY-25))
        #pygame.draw.rect(data.screen,data.tripleTowers[data.selectedTowerCounter].color,(data.mouseX-25,data.mouseY-25,50,50))
        pygame.draw.circle(data.screen,data.redColor,(data.mouseX,data.mouseY),data.tripleTowers[data.selectedTowerCounter].range,1)
        if (0<=data.mouseClickX<700) and (0<=data.mouseClickY<550):#checks if it is going to be placed in path
            if not ((50<=data.mouseClickX<=100) and (0<=data.mouseClickY<=250)):
                if not ((100<=data.mouseClickX<=450) and (200<=data.mouseClickY<=250)):
                     if not ((400<=data.mouseClickX<=450) and (250<=data.mouseClickY<=450)):
                        if not ((100<=data.mouseClickX<=400) and (400<=data.mouseClickY<=450)):
                            if not ((100<=data.mouseClickX<=650) and (450<=data.mouseClickY<=500)):
                                if not ((600<=data.mouseClickX<=650) and (0<=data.mouseClickY<=500)):
                                    (xcord,ycord) = (((data.mouseClickX/50)*50),((data.mouseClickY/50)*50))
                                    if (xcord,ycord) not in data.coordListOfTurrets:   
                                        if (data.waterLevel + data.fireLevel + data.lightLevel + data.darknessLevel)<5:
                                            if not (xcord==350 and ycord==300):   
                                                data.placeTripleTower = True#ready to place it
                                        else:
                                            data.placeTripleTower = True


def placeTowerTriple(data):
    if data.placeTripleTower==True:
        (xcord,ycord) = (((data.mouseClickX/50)*50),((data.mouseClickY/50)*50))#finds the grid for it
        data.towercoord+=[(xcord,ycord,data.tripleTowers[data.selectedTowerCounter].color,\
            data.tripleTowers[data.selectedTowerCounter].bulletdamage,\
            data.tripleTowers[data.selectedTowerCounter].range,\
            data.tripleTowers[data.selectedTowerCounter].cost,\
            data.tripleTowers[data.selectedTowerCounter].timer,\
            data.tripleTowers[data.selectedTowerCounter].description,\
            data.tripleTowers[data.selectedTowerCounter].element,\
            data.tripleTowers[data.selectedTowerCounter].name)]
        data.placeTripleTower=False
        data.selectedTripleTowerToDraw=False
        data.playerMoney-= data.tripleTowers[data.selectedTowerCounter].cost
        data.cost=0

#####################################################################
#selling towers and tower info on map
#####################################################################

def turretInfo(data):#prints kind of tower on bar 2 with its range
    if (0<=data.mouseX<700) and (0<=data.mouseY<550):
        if data.placePureTower==False and data.selectedPureTowerToDraw==False and data.placeDualTower==False and\
            data.selectedDualTowerToDraw==False and data.placeTripleTower==False and data.selectedTripleTowerToDraw==False:
            mouseOnTurrets = [s for s in data.turretsList if s.rect.collidepoint(data.mouseX,data.mouseY)]
            for s in mouseOnTurrets:
                font = pygame.font.Font(None, 38)
                description = font.render('%s: %s'%(s.name,s.description),True,data.blackColor)
                data.screen.blit(description,(10,700))
                pygame.draw.circle(data.screen,data.redColor,(s.rect.x+25,s.rect.y+25),s.range,1)


def sellTower(data):
    #if in sell mode, 
    #can sell selected tower which is on map for half its cost price
    if data.sellMode==True:
        pygame.draw.circle(data.screen,data.transparentColor,(data.mouseX,data.mouseY),30,5)
        if data.selectedPureTowerToDraw == False and data.placePureTower == False and data.selectedDualTowerToDraw == False and\
            data.placeDualTower == False and data.selectedTripleTowerToDraw == False and data.placeTripleTower == False:
            if data.mouseClickXUP!=None and data.mouseClickYUP!=None:
                clickedTurrets = [s for s in data.turretsList if s.rect.collidepoint(data.mouseClickXUP,data.mouseClickYUP)]
                for s in clickedTurrets:
                    data.playerMoney+=(s.cost/2)
                    data.turretsList.remove(s)
                    data.spritesList.remove(s)
                    data.coordListOfTurrets.remove((s.rect.x,s.rect.y))
            data.mouseClickXUP=None
            data.mouseClickYUP=None

#####################################################################
#summon elementals
#####################################################################

def summonElementals(data):
    #checks which box is clicked to summon which elemental
    if (1080<=data.mouseClickX<=1180) and (160<=data.mouseClickY<=260):#water
        data.pureTowersBar = False
        data.dualTowersBar = False
        data.tripleTowersBar = False
        data.waterBar = True
        data.fireBar = False
        data.lightBar = False
        data.darknessBar = False
        data.mouseClickX=None
        data.mouseClickY=None 
    if (900<=data.mouseClickX<=1000) and (160<=data.mouseClickY<=260):#darkness
        data.pureTowersBar = False
        data.dualTowersBar = False
        data.tripleTowersBar = False
        data.waterBar = False
        data.fireBar = False
        data.lightBar = False
        data.darknessBar = True
        data.mouseClickX=None
        data.mouseClickY=None 
    if (900<=data.mouseClickX<=1000) and (10<=data.mouseClickY<=110):#fire
        data.pureTowersBar = False
        data.dualTowersBar = False
        data.tripleTowersBar = False
        data.waterBar = False
        data.fireBar = True
        data.lightBar = False
        data.darknessBar = False
        data.mouseClickX=None
        data.mouseClickY=None
    if (1080<=data.mouseClickX<=1180) and (10<=data.mouseClickY<=110):#light
        data.pureTowersBar = False
        data.dualTowersBar = False
        data.tripleTowersBar = False
        data.waterBar = False
        data.fireBar = False
        data.lightBar = True
        data.darknessBar = False
        data.mouseClickX=None
        data.mouseClickY=None


#####################################################################
#summon elementals for each element, same code, just repititve
#####################################################################


def drawWaterElementals(data):
    #draws that specific elemental at bar 2
    #with its name appearing when mouse is brought over it
    listOfElementals=[]#stores coordinates of towers/elementals
    if data.waterBar == True:
        xcord=500#preset coordinates for bar 2
        ycord=560
        if data.waterLevel<3:
            elemental = data.waterElementals[data.waterLevel]
            if elemental.name == 'Water Elemental':
                image = pygame.transform.scale(data.water1,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            elif elemental.name == 'Water Elemental 2':
                image = pygame.transform.scale(data.water2,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            elif elemental.name == 'Water Elemental 3':
                image = pygame.transform.scale(data.water3,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            image2 = pygame.transform.rotate((pygame.transform.scale(data.waterBarImage,(1200,150)).convert()),180)
            data.screen.blit(image2,(0,550))
            #pygame.draw.rect(data.screen,data.darkBlueColor,(0,550,1200,150))
            data.screen.blit(image,(xcord,ycord))
            listOfElementals+=[(xcord,xcord+150,ycord,ycord+100)]
        for coord in xrange(len(listOfElementals)):
            (y,y1,x,x1) = listOfElementals[coord]
            if (y<=data.mouseX<=y1) and (x<=data.mouseY<=x1):#when moving mouse over it gives description
                font = pygame.font.SysFont('arialroundedmtbold', 40)
                description = font.render('%s'%(data.waterElementals[data.waterLevel].name),True,data.darkBlueColor)
                data.screen.blit(description,(400,730))#shows at bottom of screen


def callWaterElemental(data):
    #if there is a charge and there are no monsters
    #player may summon elemental
    if (500<=data.mouseClickX<=650) and (560<=data.mouseClickY<=660) and data.waterBar==True and len(data.monstersList)==0\
        and data.ELEMENTAL>0:
        addWaterElemental(data)
        data.mouseClickX=None
        data.mouseClickY=None

def addWaterElemental(data):
    #an elemental is also added to the monster sprite class
    elemental = (data.waterElementals[data.waterLevel])
    health = elemental.health
    color = elemental.color
    element = elemental.element
    speed = elemental.vectorspeed
    name = elemental.name
    monster = Monster(60,0,health,color,element,speed,name,data)
    data.spritesList.add(monster)
    data.monstersList.add(monster)
    data.ELEMENTAL-=1


def drawDarknessElementals(data):
    listOfElementals=[]#stores coordinates of towers/elementals
    if data.darknessBar == True:
        xcord=500#preset coordinates for bar 2
        ycord=560
        if data.darknessLevel<3:
            elemental =  data.darknessElementals[data.darknessLevel]#from list of water elementals
            if elemental.name == 'Darkness Elemental':
                image = pygame.transform.scale(data.dark1,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            elif elemental.name == 'Darkness Elemental 2':
                image = pygame.transform.scale(data.dark2,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            elif elemental.name == 'Darkness Elemental 3':
                image = pygame.transform.scale(data.dark3,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            image2 = pygame.transform.rotate((pygame.transform.scale(data.darknessBarImage,(1200,150)).convert()),180)
            data.screen.blit(image2,(0,550))
            #pygame.draw.rect(data.screen,data.grayColor,(0,550,1200,150))
            data.screen.blit(image,(xcord,ycord))
            listOfElementals+=[(xcord,xcord+150,ycord,ycord+100)]
        for coord in xrange(len(listOfElementals)):
            (y,y1,x,x1) = listOfElementals[coord]
            if (y<=data.mouseX<=y1) and (x<=data.mouseY<=x1):#when moving mouse over it gives description
                font = pygame.font.SysFont('arialroundedmtbold', 40)
                description = font.render('%s'%(data.darknessElementals[data.darknessLevel].name),True,data.blackColor)
                data.screen.blit(description,(400,730))#shows at bottom of screen

def callDarknessElemental(data):
    if (500<=data.mouseClickX<=650) and (560<=data.mouseClickY<=660) and data.darknessBar==True and len(data.monstersList)==0\
        and data.ELEMENTAL>0:
        addDarknessElemental(data)
        data.mouseClickX=None
        data.mouseClickY=None

def addDarknessElemental(data):
    elemental = (data.darknessElementals[data.darknessLevel])
    health = elemental.health
    color = elemental.color
    element = elemental.element
    speed = elemental.vectorspeed
    name = elemental.name
    monster = Monster(60,0,health,color,element,speed,name,data)
    data.spritesList.add(monster)
    data.monstersList.add(monster)
    data.ELEMENTAL-=1




def drawFireElementals(data):
    listOfElementals=[]#stores coordinates of towers/elementals
    if data.fireBar == True:
        xcord=500#preset coordinates for bar 2
        ycord=560
        if data.fireLevel<3:
            elemental = data.fireElementals[data.fireLevel]#from list of water elementals
            if elemental.name == 'Fire Elemental':
                image = pygame.transform.scale(data.fire1,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            elif elemental.name == 'Fire Elemental 2':
                image = pygame.transform.scale(data.fire2,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            elif elemental.name == 'Fire Elemental 3':
                image = pygame.transform.scale(data.fire3,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            image2 = pygame.transform.rotate((pygame.transform.scale(data.fireBarImage,(1200,150)).convert()),180)
            data.screen.blit(image2,(0,550))
            #pygame.draw.rect(data.screen,data.darkRedColor,(0,550,1200,150))
            data.screen.blit(image,(xcord,ycord))
            listOfElementals+=[(xcord,xcord+150,ycord,ycord+100)]
        for coord in xrange(len(listOfElementals)):
            (y,y1,x,x1) = listOfElementals[coord]
            if (y<=data.mouseX<=y1) and (x<=data.mouseY<=x1):#when moving mouse over it gives description
                font = pygame.font.SysFont('arialroundedmtbold', 40)
                description = font.render('%s'%(data.fireElementals[data.fireLevel].name),True,data.redColor)
                data.screen.blit(description,(400,730))#shows at bottom of screen

def callFireElemental(data):
    if (500<=data.mouseClickX<=650) and (560<=data.mouseClickY<=660) and data.fireBar==True and len(data.monstersList)==0\
        and data.ELEMENTAL>0:
        addFireElemental(data)
        data.mouseClickX=None
        data.mouseClickY=None

def addFireElemental(data):
    elemental = (data.fireElementals[data.fireLevel])
    health = elemental.health
    color = elemental.color
    element = elemental.element
    speed = elemental.vectorspeed
    name = elemental.name
    monster = Monster(60,0,health,color,element,speed,name,data)
    data.spritesList.add(monster)
    data.monstersList.add(monster)
    data.ELEMENTAL-=1




def drawlightElementals(data):
    listOfElementals=[]#stores coordinates of towers/elementals
    if data.lightBar == True:
        xcord=500#preset coordinates for bar 2
        ycord=560
        if data.lightLevel<3:
            elemental=data.lightElementals[data.lightLevel]#from list of water elementals
            if elemental.name == 'Light Elemental':
                image = pygame.transform.scale(data.light1,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            elif elemental.name == 'Light Elemental 2':
                image = pygame.transform.scale(data.light2,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            elif elemental.name == 'Light Elemental 3':
                image = pygame.transform.scale(data.light3,(150,100)).convert()
                image.set_colorkey((data.whiteColor))
            image2 = pygame.transform.rotate((pygame.transform.scale(data.lightBarImage,(1200,150)).convert()),180)
            data.screen.blit(image2,(0,550))
            #pygame.draw.rect(data.screen,data.yellowColor,(0,550,1200,150))
            data.screen.blit(image,(xcord,ycord))
            listOfElementals+=[(xcord,xcord+150,ycord,ycord+100)]
        for coord in xrange(len(listOfElementals)):
            (y,y1,x,x1) = listOfElementals[coord]
            if (y<=data.mouseX<=y1) and (x<=data.mouseY<=x1):#when moving mouse over it gives description
                font = pygame.font.SysFont('arialroundedmtbold', 40)
                description = font.render('%s'%(data.lightElementals[data.lightLevel].name),True,data.darkYellowColor)
                data.screen.blit(description,(400,730))#shows at bottom of screen

def calllightElemental(data):
    if (500<=data.mouseClickX<=650) and (560<=data.mouseClickY<=660) and data.lightBar==True and len(data.monstersList)==0\
        and data.ELEMENTAL>0:
        addLightElemental(data)
        data.mouseClickX=None
        data.mouseClickY=None

def addLightElemental(data):
    elemental = (data.lightElementals[data.lightLevel])
    health = elemental.health
    color = elemental.color
    element = elemental.element
    speed = elemental.vectorspeed
    name = elemental.name
    monster = Monster(60,0,health,color,element,speed,name,data)
    data.spritesList.add(monster)
    data.monstersList.add(monster)
    data.ELEMENTAL-=1




#####################################################################
#game over conditions
#####################################################################

def gameOver(data):
    #what the screen will be like depending on win or lose
    data.screen.blit(data.secondintro,(0,0))
    font = pygame.font.SysFont('silom', 200)
    font2 = pygame.font.SysFont('silom', 60)
    font3 = pygame.font.SysFont('silom', 35)
    data.backgroundMusic.stop()
    if data.gameOverWin == True:
        if data.endCounter==1:
            data.gameOverWinSound.play(-1) 
        if data.musicCounter%2!=0:
            pygame.mixer.pause()   
        win = font.render('YOU WIN!!!!',True,data.grayColor)
        data.screen.blit(win,(10,230))
    if data.gameOverLose == True:
        if data.endCounter==1:
            data.gameOverLoseSound.play(-1)
        if data.musicCounter%2!=0:
            pygame.mixer.pause() 
        if data.endCounter%2!=0:
            lose = font.render('YOU LOSE!!',True,data.redColor)
        else:
            lose = font.render('YOU LOSE!!',True,data.yellowColor)
        data.screen.blit(lose,(10,230))
    exit = font2.render('EXIT',True,(0,0,0))
    data.screen.blit(exit,(510,450))
    if (500<=data.mouseX<=650) and (450<=data.mouseY<=510):
        exit = font2.render('EXIT',True,(255,0,0))
        data.screen.blit(exit,(510,450))
    credits = font3.render('Credits to Google Images and to all who tested this game',True,data.greenColor)
    data.screen.blit(credits,(50,550))
    if (500<=data.mouseClickX<=650) and (450<=data.mouseClickY<=510):
        #if you click exit
        data.mode = 'Exit'
    pygame.display.flip()

def casesOver(data):
    #checks for win or lose in the game
    if data.wave ==20 and len(data.monstersList)==0 and data.playerLife>0:
        data.gameOverWin=True
        data.mode='Done'
        data.backgroundMusic.stop()
    if data.playerLife<=0:
        data.gameOverLose =True
        data.mode='Done'
        data.backgroundMusic.stop()

#####################################################################
#init 
#####################################################################
def init(data):
    #2d list of the path
    data.monsterPath=[[0,1,0,0,0,0,0,0,0,0,0,0,42],
    [0,2,0,0,0,0,0,0,0,0,0,0,41],
    [0,3,0,0,0,0,0,0,0,0,0,0,40],
    [0,4,0,0,0,0,0,0,0,0,0,0,39],
    [0,5,6,7,8,9,10,11,12,0,0,0,38],
    [0,0,0,0,0,0,0,0,13,0,0,0,37],
    [0,0,0,0,0,0,0,0,14,0,0,0,36],
    [0,0,0,0,0,0,0,0,15,0,0,0,35],
    [0,0,22,21,20,19,18,17,16,0,0,0,34],
    [0,0,23,24,25,26,27,28,29,30,31,32,33]]

    #set mouse positions to none first
    data.mouseClickX = None
    data.mouseClickY = None
    data.mouseX = None
    data.mouseY = None
    data.mouseClickXUP = None
    data.mouseClickYUP = None
    #####################
    #bar1
    #####################
    data.playerMoney = 30
    data.playerLife = 5
    data.wave = 0
    #element level
    data.waterLevel = 0
    data.fireLevel = 0
    data.lightLevel = 0
    data.darknessLevel = 0
    data.ELEMENTAL = 0 #needed for summoning elementals

    #list of towers per level
    data.pureTowers = [data.FireTowerOne,data.WaterTowerOne,data.LightTowerOne,data.DarknessTowerOne,
    data.FireTowerTwo,data.WaterTowerTwo,data.LightTowerTwo,data.DarknessTowerTwo]
    data.dualTowers = [data.SteamTower,data.MagnifyTower,data.DevilTower,data.RainbowTower,data.PoisonTower,data.TrickeryTower]
    data.tripleTowers = [data.LaserTower,data.HailTower,data.FlameThrowerTower,data.CorrosionTower]

    data.waterElementals = [data.WaterElemental1,data.WaterElemental2,data.WaterElemental3]
    data.fireElementals = [data.FireElemental1,data.FireElemental2,data.FireElemental3]
    data.lightElementals = [data.LightElemental1,data.LightElemental2,data.LightElemental3]
    data.darknessElementals = [data.DarknessElemental1,data.DarknessElemental2,data.DarknessElemental3]


    data.Waves=[data.Wave1,data.Wave2,data.Wave3,data.Wave4,data.Wave5,data.Wave6,data.Wave7,data.Wave8,data.Wave9,\
    data.Wave10,data.Wave11,data.Wave12,data.Wave13,data.Wave14,data.Wave15,data.Wave16,data.Wave17,data.Wave18,data.Wave19,\
    data.Wave20]


    data.towerCounterForDrawing = 0
    data.selectedTowerCounter = 0
    data.cost = 0
    data.pureTowersBar = False
    data.selectedPureTowerToDraw = False
    data.placePureTower = False
    data.towercoord = []
    data.dualTowersBar = False
    data.selectedDualTowerToDraw = False
    data.placeDualTower = False
    data.tripleTowersBar = False
    data.selectedTripleTowerToDraw = False
    data.placeTripleTower = False
    data.waterBar = False
    data.fireBar = False
    data.lightBar = False
    data.darknessBar = False
    data.coordListOfTurrets = []#to check if spot is already filled


    data.sellMode = False#to enter/exit sell mode

    #all the sprite groups needed
    data.spritesList = pygame.sprite.Group()
    data.monstersList = pygame.sprite.Group()
    data.turretsList = pygame.sprite.Group()
    data.bulletsList = pygame.sprite.Group()

    data.gameOverWin = False
    data.gameOverLose =False

    data.timerCounter=0
    data.timerCounter2=0
    data.imageCounter=0

    data.endCounter =0
    data.time = 25

    #to check the range
    data.turretCounter = 1


#####################################################################
#for introduction and main menu and pause and its intits
#####################################################################

def initInitial2(data):
    #this are the values needed for intro/menu page
    data.mode = 'Intro'
    data.x1 = 0
    data.x2 = 600
    data.pause = False
    data.front1 = pygame.image.load('images/frontpage1.png')
    data.front2 = pygame.image.load('images/frontpage2.png')
    image = pygame.image.load('images/secondintro2.jpg')
    data.secondintro = pygame.transform.scale(image,(1200,800)).convert()
    data.musicCounter = 0
    data.playHardMode = False

def initInitial(data):
    #this values are different from initInitial2 
    #since they are called in reset if there is a rest
    data.introCounter=0
    data.mouseClickX = None
    data.mouseClickY = None
    data.mouseX = None
    data.mouseY = None
    data.mouseClickXUP = None
    data.mouseClickYUP = None
    data.instructionMenu = False
    data.instructionMenu2 = False
    (data.dragonXcord,data.dragonYcord)=(350,300)
    data.dragonMoveValue=False
    (data.dragonXcol,data.dragonYcol)=(0,0)
    data.dragonCounter = 0


def introduction(data):
    #blits the opening and closing pictures onto the screen
    if data.x2<1200:
        image = pygame.transform.scale(data.front1,(600,800)).convert()
        data.screen.blit(image,(data.x1,0))
        image2 = pygame.transform.scale(data.front2,(600,800)).convert()
        data.screen.blit(image2,(data.x2,0))

def printMainMenu(data):
    #prints the whole menu
    #including instructions depending on value of data.instructionMenu
    data.screen.blit(data.secondintro,(0,0))
    font = pygame.font.SysFont('silom', 60)
    if data.instructionMenu==False and data.instructionMenu==False:
        instructions = font.render('INSTRUCTIONS',True,(0,0,0))
        data.screen.blit(instructions,(350,250))
        easy = font.render('EASY',True,(0,0,0))
        data.screen.blit(easy,(400,350))
        hard = font.render('HARD',True,(0,0,0))
        data.screen.blit(hard,(600,350))
        exit = font.render('EXIT',True,(0,0,0))
        data.screen.blit(exit,(510,450))
        name = font.render('ELEMENTAL TOWER DEFENSE',True,(127,127,127))
        data.screen.blit(name,(180,150))
        if data.pause==True:
            pause = font.render('GAME PAUSED',True,(data.whiteColor))
            data.screen.blit(pause,(360,550))
    else:#instructionmenu is true
        COLOR = (20,175,20)
        COLOR2 = (255,255,0)
        font2 = pygame.font.SysFont('silom', 35)
        back = font2.render("BACK",True,(255,0,255))
        data.screen.blit(back,(1090,5))
        if data.instructionMenu2==False:
            instruction1 = font2.render('-YOUR OBJECTIVE IS TO SURVIVE 20 WAVES OF MONSTERS',True,COLOR)
            data.screen.blit(instruction1,(10,10))
            instruction2 = font2.render('-YOU MAY BUILD TOWERS ANYWHERE OUTSIDE THE PATH',True,COLOR2)
            data.screen.blit(instruction2,(10,90))
            instruction3 = font2.render('-YOU MAY ONLY BUILD TOWERS BASED ON YOUR ELEMENT LEVEL',True,COLOR)
            data.screen.blit(instruction3,(10,170))
            instruction4 = font2.render('-YOUR ELEMENT LEVEL IS SHOWN ON THE ELEMENT BOXES',True,COLOR2)
            data.screen.blit(instruction4,(10,250))
            instruction5 = font2.render('-YOU MAY INCREASE ELEMENT LEVEL BY SUMMONING ELEMENTALS',True,COLOR)
            data.screen.blit(instruction5,(10,330))
            instruction6 = font2.render('-YOU MAY ONLY SUMMON ELEMENTALS WHEN YOU HAVE A CHARGE',True,COLOR2)
            data.screen.blit(instruction6,(10,410))
            instruction7 = font2.render('-BE WARNED: A TOWER SHOOTING AT A MONSTER OF ITS OWN',True,(255,0,0))
            data.screen.blit(instruction7,(10,490))
            instruction8 = font2.render('                           ELEMENT WILL ONLY MAKE THE MONSTER STRONGER',True,(255,0,0))
            data.screen.blit(instruction8,(10,570))
            instruction9 = font2.render("-YOU MAY SELL TOWERS FOR HALF ITS COST PRICE BY PRESSING 'S'",True,COLOR)
            data.screen.blit(instruction9,(10,650))
            instruction10 = font2.render("-PRESS 'P' TO PAUSE/UNPAUSE GAME AND 'M' TO MUTE SOUND",True,COLOR2)
            data.screen.blit(instruction10,(10,730))
            next = font2.render("NEXT",True,(255,0,255))
            data.screen.blit(next,(1090,745))
        else:
            instruction1 = font2.render("-YOU MAY SUMMON A WAVE BY CLICKING ON 'WAVE'",True,COLOR)
            data.screen.blit(instruction1,(10,10))
            instruction2 = font2.render('-YOU MAY GET INFORMATION ABOUT THE WAVE BY PLACING',True,COLOR2)
            data.screen.blit(instruction2,(10,90))
            instruction3 = font2.render("  CURSOR ON THE 'WAVE'",True,COLOR2)
            data.screen.blit(instruction3,(10,170))
            instruction4 = font2.render('-YOU MAY SUMMON AN ELEMENT BY CLICKING ON THE ELEMENT BOX',True,COLOR)
            data.screen.blit(instruction4,(10,250))
            instruction5 = font2.render('  AND CLICKING ON THE ELEMENTAL SHOWN BELOW',True,COLOR)
            data.screen.blit(instruction5,(10,330))
            instruction6 = font2.render('-YOU MAY ACCESS TOWERS BY CLICKING ON THE TYPES OF TOWER',True,COLOR2)
            data.screen.blit(instruction6,(10,410))
            instruction7 = font2.render('  AND SELECT THE TOWER BY CLICKING ON IT AND PLACE IT ON THE',True,(COLOR2))
            data.screen.blit(instruction7,(10,490))
            instruction8 = font2.render("  MAP BY CLICKING AGAIN, PRESS 'SPACEBAR' TO UNSELECT TOWER",True,(COLOR2))
            data.screen.blit(instruction8,(10,570))
            instruction9 = font2.render("-HINT: RESTART GAME AT ANY TIME BY PRESSING 'R'",True,(255,0,0))
            data.screen.blit(instruction9,(10,650))
            instruction10 = font2.render("-HINT: HARD MODE HAS A TIMER OF 25 SECONDS",True,(255,0,0))
            data.screen.blit(instruction10,(10,730))


def highlightWord(data):
    #certain words are highlighted red or white
    #if the mouse is brought over them
    if data.x2==1200:
        font = pygame.font.SysFont('silom', 60)
        if data.instructionMenu==False:
            if (350<=data.mouseX<=790) and (250<=data.mouseY<=310):
                instructions = font.render('INSTRUCTIONS',True,(255,0,0))
                data.screen.blit(instructions,(350,250))
            if (400<=data.mouseX<=550) and (350<=data.mouseY<=410):
                easy = font.render('EASY',True,(255,0,0))
                data.screen.blit(easy,(400,350))
            if (600<=data.mouseX<=750) and (350<=data.mouseY<=410):
                hard = font.render('HARD',True,(255,0,0))
                data.screen.blit(hard,(600,350))
            if (500<=data.mouseX<=650) and (450<=data.mouseY<=510):
                exit = font.render('EXIT',True,(255,0,0))
                data.screen.blit(exit,(510,450))
        else:
            font2 = pygame.font.SysFont('silom', 35)
            if (1090<=data.mouseX<=1190) and (5<=data.mouseY<=40):
                back = font2.render("BACK",True,(255,255,255))
                data.screen.blit(back,(1090,5))
            if data.instructionMenu2==False:
                if (1090<=data.mouseX<=1190) and (745<=data.mouseY<=780):
                    next = font2.render("NEXT",True,(255,255,255))
                    data.screen.blit(next,(1090,745))


def chooseOption(data):
    #depending on which option is chosen in the menu
    #the next condition occurs
    if data.x2==1200:
        if data.instructionMenu==False and data.instructionMenu2==False:
            if (400<=data.mouseClickX<=550) and (350<=data.mouseClickY<=410):
                data.playHardMode=False
                data.introMusic.stop()
                data.backgroundMusic=pygame.mixer.Sound("music/ObstacleCourse.wav")#play background song
                data.backgroundMusic.play(-1)
                if data.musicCounter%2!=0:
                    pygame.mixer.pause()
                data.mode = 'Running'
                if data.pause==True:
                    data.pause = False
                data.mouseClickX = None
                data.mouseClickY = None
            if (600<=data.mouseClickX<=750) and (350<=data.mouseClickY<=410):
                if data.timerCounter!=0 and data.playHardMode==False:
                    data.time=25
                data.playHardMode=True
                data.introMusic.stop()
                data.backgroundMusic=pygame.mixer.Sound("music/ObstacleCourse.wav")#play background song
                data.backgroundMusic.play(-1)
                if data.musicCounter%2!=0:
                    pygame.mixer.pause()
                data.mode = 'Running'
                if data.pause==True:
                    data.pause = False
                data.mouseClickX = None
                data.mouseClickY = None
            if (350<=data.mouseClickX<=790) and (250<=data.mouseClickY<=310):
                data.instructionMenu=True
            if (500<=data.mouseClickX<=650) and (450<=data.mouseClickY<=510):
                data.mode = 'Exit'
        elif data.instructionMenu==True and data.instructionMenu2==False:
            if (1090<=data.mouseClickX<=1190) and (5<=data.mouseClickY<=40):
                data.instructionMenu=False
            if (1090<=data.mouseClickX<=1190) and (745<=data.mouseClickY<=780):
                data.instructionMenu2=True
            data.mouseClickX = None
            data.mouseClickY = None
        elif data.instructionMenu==True and data.instructionMenu2==True:
            if (1090<=data.mouseClickX<=1190) and (5<=data.mouseClickY<=40):
                data.instructionMenu2=False
            data.mouseClickX = None
            data.mouseClickY = None

def moveIntro(data):
    #gets the two sides of the picture to slide open
    if data.x2<1200:
        if data.introCounter>10 and data.introCounter%5==0:
            data.x1-=100
            data.x2+=100
        data.mouseClickX = None
        data.mouseClickY = None


def redrawAll2(data):
    #is the redraw function for the introduction loop
    printMainMenu(data)
    highlightWord(data)
    introduction(data)
    pygame.display.flip()




def redrawAll3(data): #for paused state
    printMainMenu(data)
    highlightWord(data)
    pygame.display.flip()

def checkPause(data):
    #this checks in all loops if there is a pause while game has started
    if data.pause==True:
        data.mode = 'Paused'
    else:
        data.mode = 'Running'

def exit(data):
    #prints the two images closing
    if data.x2>600:
        image = pygame.transform.scale(data.front1,(600,800)).convert()
        data.screen.blit(image,(data.x1,0))
        image2 = pygame.transform.scale(data.front2,(600,800)).convert()
        data.screen.blit(image2,(data.x2,0))

def moveExit(data):
    #same as move for the intro, but this is the opposite
    #it slides inwards
    if data.mode == 'Exit':
        if data.x2>600:
            if data.endCounter%5==0:
                data.x1+=100
                data.x2-=100

#####################################################################
#for special feature of a flying dragon
#####################################################################

def flyingDragon(data):
    #dragon can fly in any direction from the 4
    directions=[(-50,0),(50,0),(0,-50),(0,50)]
    if (data.waterLevel + data.fireLevel + data.lightLevel + data.darknessLevel)>=5:
        #if this special condition is met
        #it starts to fly and attack
        #it flys in a gif format way
        if 0<=data.timerCounter2%3<1:
            dragon1 = pygame.transform.scale(data.dragon1,(50,50)).convert()
            dragon1.set_colorkey((data.blackColor))
            dragon1.set_alpha(210)
            data.screen.blit(dragon1,(data.dragonXcord,data.dragonYcord))
        elif 1<=data.timerCounter2%3<2:
            dragon2 = pygame.transform.scale(data.dragon2,(50,50)).convert()
            dragon2.set_colorkey((data.blackColor))
            dragon2.set_alpha(210)
            data.screen.blit(dragon2,(data.dragonXcord,data.dragonYcord))
        elif 2<=data.timerCounter2%3<3:
            dragon3 = pygame.transform.scale(data.dragon3,(50,50)).convert()
            dragon3.set_colorkey((data.blackColor))
            dragon3.set_alpha(200)
            data.screen.blit(dragon3,(data.dragonXcord,data.dragonYcord))
        #dragon moves andomly
        #if within map, dragon moves smoothly due to division by 50
        #the magic number 50 is grid pixel 50 X 50
        x=random.choice(range(4))
        if data.dragonCounter==50:
            data.dragonMoveValue=False
            data.dragonCounter=0
        if data.dragonMoveValue==False: 
            (data.dragonXcol,data.dragonYcol)=directions[x]
            if (0<=data.dragonXcord+data.dragonXcol<=650) and (0<=data.dragonYcord+data.dragonYcol<=500):
                data.dragonMoveValue=True
                (data.dragonXcol,data.dragonYcol)=(data.dragonXcol/50,data.dragonYcol/50)
        if data.dragonMoveValue==True:
            (data.dragonXcord,data.dragonYcord)=(data.dragonXcord+data.dragonXcol,data.dragonYcord+data.dragonYcol)
            data.dragonCounter+=1

        #dragon shoots monsters
        #magic numbers for range=200,damge=8,timercounter=1,all elemental
        for monster in data.monstersList:
            if (0<=monster.rect.x<700) and (0<=monster.rect.y<550):
                if ((monster.rect.x - data.dragonXcord)**2 + (monster.rect.y - data.dragonYcord)**2)**0.5<=200:
                    x=max((abs(monster.rect.x - data.dragonXcord)),(abs(monster.rect.y - data.dragonYcord)))
                    xcol=round(((monster.rect.x - data.dragonXcord)/float(x)),2)
                    ycol=round(((monster.rect.y - data.dragonYcord)/float(x)),2)
                    bullet = Bullet(data.dragonXcord+25.0,data.dragonYcord+25.0,xcol,ycol,8,200,1,'fire,water,light,darkness',data)
                    sound=pygame.mixer.Sound("music/laser.wav")
                    if data.musicCounter%2==0:
                        sound.play()
                    data.bulletsList.add(bullet)
                    data.spritesList.add(bullet)
    else:
        #at first it is a statue to get the player interested in it
        #and try to figure it out
        dragon1 = pygame.transform.scale(data.dragon1,(50,50)).convert()
        dragon1.set_colorkey((data.blackColor))
        data.screen.blit(dragon1,(data.dragonXcord,data.dragonYcord))        

    
#main run function
def run():
    pygame.init()
    class Struct: pass
    data = Struct()
    #initialize the screen
    data.screenSize = (1200,800)
    data.screen = pygame.display.set_mode(data.screenSize)
    pygame.display.set_caption("Elemental Tower Defense")
    #initialize clock
    data.clock = pygame.time.Clock()
    #only init the things needed to speed up loading time
    initInitial2(data)
    initInitial(data)
    timerFired(data)
    if data.mode =='Intro':
        data.introMusic=pygame.mixer.Sound("music/dream.wav")#play background song
        data.introMusic.play(-1)
    while data.mode=='Intro':
        moveIntro(data)
        if data.introCounter==10:
            #loads while the pictures slide out to reduce lag
            init2(data)
            init(data)
        chooseOption(data)
        timerFired(data)
    while data.mode !='Exit' and data.mode!='Intro':
        while (data.mode== "Running"):
            if data.playHardMode == True:
                hardMode(data)
            else:
                callWave(data)
            checkPause(data)
            while data.mode=='Paused':
                chooseOption(data)
                if data.mode == 'Exit':
                    break
                checkPause(data)
                timerFired(data)
            #draws everything
            printGrid(data)
            printPath(data)
            drawBar1(data)
            drawBar2(data)
            drawPureTowersBar(data)
            drawTowerOnMouse(data)
            placeTower(data)
            drawDualTowersBar(data)
            drawTowerOnMouseDual(data)
            placeTowerDual(data)
            drawTripleTowersBar(data)
            drawTowerOnMouseTriple(data)
            placeTowerTriple(data)
            #draws and summons elementals
            summonElementals(data)
            drawWaterElementals(data)
            drawFireElementals(data)
            drawlightElementals(data)
            drawDarknessElementals(data)
            #all tower related functions
            turretInfo(data)
            sellTower(data)
            viewWaveMonsters(data)
            #sprite related functions
            drawTowersOnMap(data)
            monstersReachBase(data)
            shootMonsters(data)
            ifMonsterHitOrBulletOB(data)
            #summoning elementals and checking for game over 
            #which send data.mode to 'Done'
            callWaterElemental(data)
            callDarknessElemental(data)
            callFireElemental(data)
            calllightElemental(data)
            casesOver(data)
            timerFired(data)
        while data.mode == 'Done':
            timerFired(data)
    #if someone presses exit at any time
    while data.mode == 'Exit':
        moveExit(data)
        timerFired(data)


run()