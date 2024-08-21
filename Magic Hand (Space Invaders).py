import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1000,800))
pygame.display.set_caption('Wizard Defence')

background = pygame.image.load('castle.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

playerimg = pygame.image.load('hand.png')
playerx = 450
playery = 700
xchange = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyxchange = []
enemyychange = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyimg.append(pygame.image.load('orc.png'))
    enemyx.append(random.randint(64,736))
    enemyy.append(random.randint(0,150))
    enemyxchange.append(0.5)
    enemyychange.append(50)

# ready means cant see bullet on screen
# fire means bullet is on screen
bulletimg = pygame.image.load('mana.png')
bulletx = 0
bullety = 700
bulletxchange = 0
bulletychange = 1
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 128)

def game_over_text(x,y):
    over_text = over_font.render('GAME OVER', True, (0,0,0))
    screen.blit(over_text, (100,300))

def show_score(x,y):
    score = font.render('Score: ' + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x+40, y+10))

def iscollision(enemyx,enemyy,bulletx,bullety):
    distance = math.sqrt(math.pow(enemyx-bullety,2)+math.pow(enemyy-bullety,2))
    if distance < 29:
        return True
    else:
        return False

running = True
while running:
    
    screen.fill((0,50,100))

    screen.blit(background, (-500,-700))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xchange = -0.5
            if event.key == pygame.K_RIGHT:
                xchange = 0.5
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # gets current x coordinate of hand
                if bullet_state == 'ready':
                    bulletx = playerx
                    fire_bullet(playerx, bullety)
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                xchange = 0

    playerx += xchange

    # player boundary
    if playerx <= -30:
        playerx = -30
    elif playerx >= 900:
        playerx = 900

    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyy[i] > 300:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text(0,600)
            break

        enemyx[i] += enemyxchange[i]        
        if enemyx[i] <= 0:
            enemyxchange[i] = 0.3
            enemyy[i] += enemyychange[i]
        elif enemyx[i] >= 936:
            enemyxchange[i] = -0.3
            enemyy[i] += enemyychange[i]

        # collisions
        collision = iscollision(enemyx[i],enemyy[i],bulletx,bullety)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 700
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(64,736)
            enemyy[i] = random.randint(0,150)

        enemy(enemyx[i],enemyy[i],i)

    # bullet movement
    if bullety <= 0:
        bullety = 700
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletx, bullety)
        bullety -= bulletychange


    player(playerx,playery)
    show_score(textx,texty)
    pygame.display.update() 