import pygame
import random

p2_action_list = ['up', 'attack1', 'attack2', '', '', '', '', '', '', '', '',  'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none']#'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', ]
p2_choice=[]
class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, screen):
    self.player=player
    self.size=data[0]
    self.image_scale=data[1]
    self.offset=data[2]
    self.flip=flip
    self.animation_list=self.load_images(sprite_sheet, animation_steps)
    self.action=0#0:idle #1:run #2 jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index=0
    self.image=self.animation_list[self.action][self.frame_index]
    self.update_time=pygame.time.get_ticks()
    self.rect=pygame.Rect((x, y, 80, 180))
    self.vel_y=0
    self.running=False
    self.jump=False
    self.attacking=False
    self.attack_type=0
    self.attack_cooldown=0
    self.attack_sound=sound
    self.hit=False
    self.health=100
    self.alive=True
    self.heal=False
    self.healing_potion=0
    self.screen = screen
    


  def load_images(self, sprite_sheet, animation_steps):
    animation_list=[]
    for y, animation in enumerate(animation_steps):
      temp_img_list=[]
      for x in range(animation):
        temp_img=sprite_sheet.subsurface(x*self.size, y*self.size, self.size, self.size)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size*self.image_scale, self.size*self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list
  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED=10
    GRAVITY=1
    dx=0
    dy=0
    self.running=False
    self.attack_type=0
    #ensure player face each other
    if target.rect.centerx>self.rect.centerx:
      self.flip=False
      p2_choice_run=['right']
    else:
      self.flip=True
      p2_choice_run=['left']

    key=pygame.key.get_pressed()
    if self.attacking==False and self.alive==True and round_over==False:
      if self.player==1:
        if key[pygame.K_s] and self.healing_potion!=0:
          self.health+=50
          if self.health>100:
            self.health=100
          self.healing_potion-=2
        if key[pygame.K_a]:
          dx=-SPEED
          self.running=True
        if key[pygame.K_d]:
          dx=SPEED
          self.running=True
        if key[pygame.K_w] and self.jump==False:
          self.vel_y=-30
          self.jump=True
        #attack
        if key[pygame.K_r] or key[pygame.K_t]:
          self.attack(surface, target)
          #determin which attack type was used
          if key[pygame.K_r]:
            self.attack_type=1
          if key[pygame.K_t]:
            self.attack_type=2

      
      if self.player==2:
        p2_choice=random.choices(p2_action_list)
        if self.hit==True:
          if p2_choice_run==['left']:
            p2_choice_run==['right']
          if p2_choice_run==['right']:
            p2_choice_run==['left']
        if self.health<=10 and self.healing_potion!=0:
          self.health+=50
          if self.health>100:
            self.health=100
          self.healing_potion-=2
        if (key[pygame.K_DOWN] or p2_choice==['down']) and self.healing_potion!=0:
          self.health+=50
          if self.health>100:
            self.health=100
          self.healing_potion-=1
        if key[pygame.K_LEFT] or p2_choice_run==['left']:
          dx=-SPEED
          self.running=True
        if key[pygame.K_RIGHT] or p2_choice_run==['right']:
          dx=SPEED
          self.running=True
        if (key[pygame.K_UP] or p2_choice==['up'])and self.jump==False:
          self.vel_y=-30
          self.jump=True
        #attack
        if (key[pygame.K_k] or key[pygame.K_l]) or (p2_choice==['attack1'] or p2_choice==['attack2']) or (pygame.Rect(self.rect.centerx-(2.5*self.rect.width*self.flip), self.rect.y, 2.5*self.rect.width, self.rect.height)):
          self.attack(surface, target)
          self.jump==True
          #determin which attack type was used
          if (key[pygame.K_k] or p2_choice==['attack1'] or pygame.Rect(self.rect.centerx-(2.5*self.rect.width*self.flip), self.rect.y, 2.5*self.rect.width, self.rect.height)):
            self.attack_type=1
          if key[pygame.K_l] or p2_choice==['attack2'] or pygame.Rect(self.rect.centerx-(2.5*self.rect.width*self.flip), self.rect.y, 2.5*self.rect.width, self.rect.height):
            self.attack_type=2

      
    self.vel_y+=GRAVITY
    dy+=self.vel_y
    if self.rect.left+dx<0:
      dx=-self.rect.left
    if self.rect.right+dx> screen_width:
      dx=screen_width-self.rect.right
    if self.rect.bottom+dy>screen_height-110:
      self.vel_y=0
      self.jump=False
      dy=screen_height-110-self.rect.bottom

    


    if self.attack_cooldown>0:
      self.attack_cooldown-=1
    self.rect.x+=dx
    self.rect.y+=dy
  def update(self):
    if self.health<=0:
      self.health=0
      self.alive=False
      self.update_action(6)
    elif self.hit==True:
      self.update_action(5)
    elif self.attacking==True:
        if self.attack_type==1:
          self.update_action(3)
        elif self.attack_type==2:
          self.update_action(4)
    elif self.jump==True:
      self.update_action(2)
    elif self.running==True:
      self.update_action(1)
    else:
      self.update_action(0)
    animation_cooldown=50
    self.image=self.animation_list[self.action][self.frame_index]
    if pygame.time.get_ticks()-self.update_time>animation_cooldown:
      self.frame_index+=1
      self.update_time=pygame.time.get_ticks()
    if self.frame_index>=len(self.animation_list[self.action]):
      if self.alive==False:
        self.frame_index=len(self.animation_list[self.action])-1
      else:
        self.frame_index=0
      if self.action==3 or self.action==4:
        self.attacking=False
        self.attack_cooldown=20
      if self.action==5:
        self.hit=False
        self.attacking=False
        self.attack_cooldown=20

  def attack(self, surface, target):
    if self.attack_cooldown==0:
      self.attacking=True
      self.attack_sound.play()
      attacking_rect= pygame.Rect(self.rect.centerx-(2.5*self.rect.width*self.flip), self.rect.y, 2.5*self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        if p2_choice==['attack1'] or p2_choice==['attack2']:
          target.health-=10
        target.health-=10
        target.hit=True
        target.jump=True
        p2_choice==['up']
        if self.attacking==True:
          print('hit!')
          print('')
          if random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])==[1]:
            critical_hit_img=pygame.image.load('assets/images/icons/critical_hit.png')
            self.screen.blit(critical_hit_img, (250, 600))
            print('crit!')
            print('')
            target.health-=10
          if random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])==[1]:
            print('atuo kill!')
            print('')
            target.health-=100
      #if random.choices([1, 2])==[1] and self.health!=100 and self.alive==True:
        #self.health=self.health+10
      
      #pygame.draw.rect(surface, (0,255, 0), attacking_rect)


  def update_action(self, new_action):
    if new_action!= self.action:
      self.action=new_action
      self.frame_index=0
      self.update_time=pygame.time.get_ticks()
    

  def draw(self, surface):
    img=pygame.transform.flip(self.image, self.flip, False)
    #pygame.draw.rect(surface, (255, 0, 0), self.rect)
    surface.blit(img, (self.rect.x-(self.offset[0]*self.image_scale), self.rect.y-(self.offset[1]*self.image_scale)))