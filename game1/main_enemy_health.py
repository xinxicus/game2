from time import sleep
import pygame
import random
import math
from pygame import mixer
pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((800,600))
#fire=2
#ready=1

background=pygame.image.load('background.png')


mixer.music.load('background.wav')
mixer.music.play(-1)

random_pick_list = []
random_health_list=[]
for i in range(1001):
  random_health_list.append(i)

for i in range(1):
  random_pick_list.append(i)

pygame.display.set_caption('Space invaders')
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
playerImg=pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0
playerY_change=0
player_lose='false'
player_health=100
healing_potion=2
harming_potion=2
health=0
#healing_potionimg=pygame.image.load('Healing_potion.png')
print(player_health)

explosion=pygame.image.load('explosion.png')

enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
enemy_health=[]
max_health=5

bombImg=[]
bombY_change=[]
bomb_state=[]
bombY=[]
bombX=[]

lose = False

num_of_enemies=10 
for i in range(num_of_enemies):
  enemyImg.append(pygame.image.load('enemy.png'))
  enemyX.append(random.randint(0, 736))
  enemyY.append(random.randint(50, 150))
  enemyX_change.append(2)
  enemyY_change.append(80)
  enemy_health.append(max_health)

  bombImg.append(pygame.image.load('bomb.png'))
  bombY_change.append(2)
  bomb_state.append('ready')
  bombY.append(enemyY[i])
  bombX.append(enemyX[i])

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
  screen.blit(health, (500, 0))
  

over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text(x, y):
  lose_music=mixer.Sound('lose.mp3')
  lose_music.play(-1)
  over_text=over_font.render("GAME OVER", True, (255, 255, 255))
  screen.blit(over_text, (200, 250))
  lose_img=pygame.image.load('lose.png')
  screen.blit(lose_img, (350, 180))
  screen.blit(health, (500, 0))
  

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

def enemy_bomb(x, y, i):
  screen.blit(bombImg[i], (x, y))

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

def isLose(playerX, playerY, bombX, bombY):
  global player_health
  distance=math.sqrt(math.pow(playerX-bombX,2)+math.pow(playerY-bombY,2))
  if distance<27:
    player_health=player_health-1
    print(player_health)
    if player_health==0:
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
      if (event.key==pygame.K_UP or event.key==pygame.K_w) and player_lose=='false' and healing_potion!=0:
        for i in range(50):
          player_health=player_health+1
        if player_health>100:
          player_health=100
        healing_potion=healing_potion-1
      if (event.key==pygame.K_DOWN or event.key==pygame.K_s) and player_lose=='false' and harming_potion!=0:
        for i in range(num_of_enemies):
          if enemyY[i]<=400:
            score_value=score_value+1
            enemyX[i]=random.randint(0, 736)
            enemyY[i]=random.randint(50, 150)
        harming_potion=harming_potion-1
      if (event.key==pygame.K_LEFT or event.key==pygame.K_a) and player_lose=='false': 
        playerX_change = -5
      if (event.key==pygame.K_RIGHT or event.key==pygame.K_d) and player_lose=='false':
        playerX_change = 5
      if event.key==pygame.K_SPACE and player_lose=='false':
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
      if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_a or event.key==pygame.K_d:
        playerX_change=0

  playerX+=playerX_change
  if playerX<=0:
    playerX=0
  elif playerX>=736:
    playerX=736




  if player_health<=50:
    playerImg=pygame.image.load('eight_bit_player.png')
  if player_health>50:
    playerImg=pygame.image.load('player.png')
  for i in range(num_of_enemies):
    if enemyY[i]>440:
      playerY=200000
      player_lose='true'
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

    if bullets_state[i] == 'fire':
      fire_bullet(bullets_x[i], bullets_y[i], i)
      bullets_y[i]-=bulletY_change


    if bomb_state[i]== 'fire':
      bombX[i] = enemyX[i]
      bombY[i] = enemyY[i]
      bomb_state[i] = 'fly'


    if bomb_state[i] == 'fly':
      bombY[i]+=bombY_change[i]
      enemy_bomb(bombX[i],bombY[i], i)

    if bombY[i]>480:
      bombY[i]=enemyY[i]
      bombX[i] = enemyX[i]
      bomb_state[i] = 'ready'

    if (random.choices(random_health_list))[0]==0 and player_lose=='false' and player_health<100:
      player_health=player_health+1
    if bomb_state[i] == 'ready':
      if (random.choices(random_pick_list))[0]==0 and player_lose=='false' and enemyY[i]<350:
        bomb_state[i]='fire'

    #collision=isCollision(enemyX[i],enemyY[i], bulletX, bulletY)
    #if collision:
    #  explosion_Sound=mixer.Sound('explosion.wav')
    #  explosion_Sound.play()
    #  bulletY=480
    #  bullet_state='ready'
    #  score_value+=1
    #  enemyX[i]=random.randint(0, 736)
    #  enemyY[i]=random.randint(50, 150)
    health=font.render('Health: '+ str(player_health),True, (255, 255, 255))
    screen.blit(health, (500, 0))
    if not lose:
      lose=isLose(playerX, playerY, bombX[i], bombY[i])
      
    if lose and player_health<=0:
      screen.blit(explosion, (playerX, 480))

      game_over_text(200, 500)

      playerY=200000
      player_lose='true'
      # for b in range(num_of_enemies):
      #  enemyY[b]=2000

      break

    for a in range(num_of_bullets):
      collision=isCollision(enemyX[i],enemyY[i], bullets_x[a], bullets_y[a])
      if collision:
        enemy_health[i]=enemy_health[i]-1
        if enemy_health[i]==0:
          explosion_Sound=mixer.Sound('explosion.wav')
          explosion_Sound.play()
          enemyX[i]=random.randint(0, 736)
          enemyY[i]=random.randint(50, 150)
          score_value+=1
          enemy_health[i]=max_health
        else:
          hit=mixer.Sound('hit.wav')
          hit.play()
        bullets_y[a] = 480
        bullets_state[a] = 'ready'
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
    

  player(playerX, playerY)
  show_score(textX, textY)
  pygame.display.update()