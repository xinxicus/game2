import pygame
import random
import math
from pygame import mixer
pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

background=pygame.image.load('background.png')


mixer.music.load('background.wav')
mixer.music.play(-1)


pygame.display.set_caption('Space invaders')
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
playerImg=pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0
playerY_change=0

enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=10 
for i in range(num_of_enemies):
  enemyImg.append(pygame.image.load('enemy.png'))
  enemyX.append(random.randint(0, 736))
  enemyY.append(random.randint(50, 150))
  enemyX_change.append(2)
  enemyY_change.append(80)


bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=5
bullet_state='ready'
#bullet_state = 'fire'

num_of_bullets=100
bullets_img= []
bullets_x = []
bullets_y = []
bullets_x_change = []
bullets_y_change = []
bullets_state= []


for i in range(num_of_bullets):
  bullets_img.append(pygame.image.load('missile.png'))
  bullets_x.append(0)
  bullets_y.append(480)
  bullets_state.append('ready')


score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

win_font=pygame.font.Font('freesansbold.ttf',64)
def you_win_text(x, y):
  win_music=mixer.Sound('win.mp3')
  win_music.play(-1)
  win_text=win_font.render("YOU WON!", True, (255, 255, 255))
  screen.blit(win_text, (200, 250))
  fireworks=pygame.image.load('fireworks.png')
  screen.blit(fireworks, (350, 180))
  

over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text(x, y):
  lose_music=mixer.Sound('lose.mp3')
  lose_music.play(-1)
  over_text=over_font.render("GAME OVER", True, (255, 255, 255))
  screen.blit(over_text, (200, 250))
  

def show_score(x,y):
  score=font.render('Score: '+ str(score_value),True, (255, 255, 255))
  screen.blit(score, (x, y))


#def fire_bullet(x, y):
#  global bullet_state
#  bullet_state="fire"
#  screen.blit(bulletImg,(x+16, y+10))
#  screen.blit(bulletImg, (x-10, y+10))
#  screen.blit(bulletImg, (x+40, y+10))

def fire_bullet(x, y, i):
  bullets_state[i] = 'fire'
  screen.blit(bullets_img[i],(x+2, y+10))
  screen.blit(bullets_img[i], (x-25, y+10))
  screen.blit(bullets_img[i], (x+26, y+10))

def player(x,y):
  screen.blit(playerImg, (x, y))


def enemy(x, y, i):
  screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
  distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
  if distance<54:
    return True
  else:
    return False


running = True
while running:



  screen.fill((0, 0, 0))
  screen.blit(background,(0, 0))
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      running=False
  
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_LEFT: 
        playerX_change = -5
      if event.key==pygame.K_RIGHT:
        playerX_change = 5
      if event.key==pygame.K_SPACE:
        #if bullet_state=='ready':
        #if bullet_state=='fire':
        #  bullet_Sound=mixer.Sound('laser.wav')
        #  bullet_Sound.play()
        #  bulletX=playerX
        #  fire_bullet(bulletX, bulletY)

        for i in range(num_of_bullets):
          if bullets_state[i] == 'ready':
            bullet_Sound=mixer.Sound('laser.wav')
            bullet_Sound.play()
            bullets_x[i]=playerX
            fire_bullet(bullets_x[i], bullets_y[i], i)
            break


    if event.type==pygame.KEYUP:
      if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
        playerX_change=0

  playerX+=playerX_change
  if playerX<=0:
    playerX=0
  elif playerX>=736:
    playerX=736

  for i in range(num_of_enemies):
    if enemyY[i]>440:
      for j in range(num_of_enemies):
        enemyY[j]=2000
      game_over_text(200, 250)
      break
    if score_value==100:
      for j in range(num_of_enemies):
        enemyY[i]=-20000
      you_win_text(200, 250)
      break
    
    
    enemyX[i]+=enemyX_change[i]
    if enemyX[i]<=0:
      enemyX_change[i]=2
      enemyY[i]+=enemyY_change[i]
    elif enemyX[i]>=736:
      enemyX_change[i]=-2
      enemyY[i]+=enemyY_change[i]

    #collision=isCollision(enemyX[i],enemyY[i], bulletX, bulletY)
    #if collision:
    #  explosion_Sound=mixer.Sound('explosion.wav')
    #  explosion_Sound.play()
    #  bulletY=480
    #  bullet_state='ready'
    #  score_value+=1
    #  enemyX[i]=random.randint(0, 736)
    #  enemyY[i]=random.randint(50, 150)

    for a in range(num_of_bullets):
      collision=isCollision(enemyX[i],enemyY[i], bullets_x[a], bullets_y[a])
      if collision:
        explosion_Sound=mixer.Sound('explosion.wav')
        explosion_Sound.play()
        bullets_y[a] = 480
        bullets_state[a] = 'ready'
        score_value+=1
        enemyX[i]=random.randint(0, 736)
        enemyY[i]=random.randint(50, 150)
        break


    enemy(enemyX[i], enemyY[i], i)
  
  
  
  
  #if bulletY <=0:
  #  bulletY=480
  #  bullet_state='ready'

  #if bullet_state == 'fire':
  #  fire_bullet(bulletX, bulletY)
  #  bulletY-=bulletY_change
    
  for i in range(num_of_bullets):
    if bullets_y[i] <= 0:
      bullets_y[i] = 480
      bullets_state[i] = 'ready'

    #print('i = ' + str(i))
    if bullets_state[i] == 'fire':
      fire_bullet(bullets_x[i], bullets_y[i], i)
      bullets_y[i]-=bulletY_change

  player(playerX, playerY)
  show_score(textX, textY)
  pygame.display.update()