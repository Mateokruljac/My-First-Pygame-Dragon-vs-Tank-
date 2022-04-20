import math
import random
import pygame
import os 
from pygame import mixer

#access all of the code methods and all in pygame
#initialize pygame
pygame.init()

#create a screen/window
width = 600
height = 600
window = pygame.display.set_mode((width,height))#two bracket becsause we need two parameter coordination
background = pygame.image.load(os.path.join("Background.png"))
background = pygame.transform.scale(background,(height,width))

#background music
mixer.music.load("backgrounds.wav")
mixer.music.play(10)

#create score 
score = 0
font =  pygame.font.Font("freesansbold.ttf",32) #what font do you want

#text position
textX = 7
textY = 7

def scores (x,y):
    show_score = font.render(f"Score: {score}",True,(255,255,255),None)
    window.blit(show_score,(x,y))

#redline
red_line = pygame.image.load("substract.png")
def show_redLine (x,y):
    window.blit(red_line,(x,y))

#title and icon
pygame.display.set_caption("Tank vs Dragon")
icon = pygame.image.load("crown.png")
pygame.display.set_icon(icon)

#Player image
playerIMG = pygame.image.load("tank.png")
#cratiang player (x,y) started position...wherever you want
playerX = 250
playerY = 510
playerX_change = 0
playerY_change =0
life = 3
def player(x,y):
    #blit- means draw
    #new position will be draw on the screen 
    window.blit(playerIMG,(x,y))

def lifes (x,y):
    show_life = font.render(f"life: {life}",True,(255,255,255),None)
    window.blit (show_life,(x,y))
    
def enemy(x,y,i): 
    window.blit(enemyIMG[i],(x,y))

game_over_font =  pygame.font.Font("freesansbold.ttf",512) #what font do you want

def game_over_text(x,y):
    show_game_over_text = font.render(f"GAME OVER",True,(255,255,255),None)
    

    window.blit(show_game_over_text,(100,300))    
#multiple enemy
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 4
#dragon`s fire


for i in range (number_of_enemies):
   #Create enemy
   enemyIMG.append(pygame.image.load("final-boss (1).png"))
   enemyX.append(random.randint(0,536))
   enemyY.append(random.randint(0,100))
   enemyX_change.append(0.18)
   enemyY_change.append(50)

def collisions (fireX,fireY,playerX,playerY):
    distance = math.sqrt(math.pow(playerX-fireX[i],2)) + (math.pow(playerY-fireY[i],2))
    if distance <= 26:
        return True
    else:
        False
   
#create a bullet
bulletIMG =pygame.image.load("bullet.png")
bulletX = 0
bulletY  = 510
bulletX_change = 0
bulletY_change = 0.6
bullet_state = "ready"
def fire_bullet (x,y):
    global bullet_state
    bullet_state = "fire"
    #Why x and y?? Because without 16 and 1+10 bullet doesn`t be in center 
    window.blit(bulletIMG,(x+18,y+20))
    
# colide - calculate Distance 
def collision (bulletX,bulletY,enemyX,enemyY):  
     #formula
     distance = math.sqrt(math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2))
     if distance <= 26:
         return True
     else:
         return False         
#creatig inifite loop
#Game loop
running = True # game == True
while running: #program is inside while True
    #event is anything that is happening inside game (close button,keyboard)
    # create lists of event
    window.fill((255,210,179))
    window.blit(background,(0,0))
    for event in pygame.event.get(): #all event in game wile True
        #Creating while false -> End Game
        # one of the type
        if event.type == pygame.QUIT:
            running = False # Game over
   
        #if keystroke is pressed check wheather its right or left
        if event.type == pygame.KEYDOWN: #keydown menas that keystroke has been pressed
            #any other keystroke 
            if event.key == pygame.K_LEFT:
                playerX_change = -0.40
        if event.type == pygame.KEYDOWN: #keydown menas that keystroke has been pressed
            if event.key == pygame.K_RIGHT:
               playerX_change = 0.40   
            
            if event.key == pygame.K_UP:
               playerY_change -= 0.18
            
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":   
                   bulletX = playerX
                   bulletY = playerY 
                   fire_bullet(bulletX,bulletY)
                   
       
            if event.key ==pygame.K_DOWN:
                playerY_change += 0.18              
        if event.type == pygame.KEYUP : #released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0
            
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0.0
            
   
    #if we want that anything appears in game we have to put that in event...through all game (infinite loop)
    #RGB - red,green,blue...0->250...bright/dark
    #display always must be update!!!
    #player below window...because, window needs to be first
    playerX += playerX_change
    playerY += playerY_change
    #checking for boundaris of Tank so it`t doesn`t go out of the boundaris
    if playerX <= 0:
        playerX = 0
    # 536 because we have to consider a size of a tank
    if playerX >= 536:
        playerX = 536
    
    if playerY >= 536:
        playerY = 536
    if playerY <= 10:
        playerY = 10
     
    for i in range (number_of_enemies):
           
           #game over
        if enemyY[i] >= playerY or enemyY[i] >= 460:
            # because movement of all enemies
            for j in range (number_of_enemies):
                enemyY[j] = 2000 #px
            playerX = 250
            playerY = 510    
            game_over_text(300,300)
            scores(400,300)
            break
       
        #enemy movement [i] for each enemy
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
           enemyX_change[i] = 0.25
           enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 536:
           enemyX_change[i] = - 0.19
           enemyY[i] +=enemyY_change[i]
              
        #collision
        Collision = collision(bulletX,bulletY,enemyX[i],enemyY[i])
        if Collision == True:
           bullet_sound = mixer.Sound("tanks.wav")
           bullet_sound.play()
           bullet_state = "ready"
           bulletY = playerY
           
           score += 1 
           
           enemyX[i] = random.randint(0,536)
           enemyY[i] = random.randint(0,100)
    
        enemy(enemyX[i],enemyY[i],i)
        
    
    #bullet movement 
    if bulletY <=0:
        bulletY = 510
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
 
    
    list_num = [0,50,100,150,200,250,300,350,400,450,500,550,600]
    for i in range (len(list_num)):
       show_redLine(list_num[i],470)
 
    lifes(20,550)
    player(playerX,playerY)
    scores(textX,textY)
    pygame.display.update()