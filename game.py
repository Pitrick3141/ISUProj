"""
#1 Initialization
Import Library & Initialize Pygame
Basic Configurations
"""
#Import library 
from numpy import inf
import pygame
from pyparsing import Char
import random

#Initialize Pygame
pygame.init()

#Define colours and fonts
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
info = (73, 130, 222)
intro_bg = (195, 209, 232)
font = pygame.font.Font(None, 36)

"""
#2 Functions
Define all the reusable functions
"""
#Define special effect for captions
def JumpingCaption(text,color,x,y) -> None:
    x_shift = 0
    letters = list(text)
    if color == "rand":
        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    for letter in letters:
        if letter == " ":
            continue
        letter_render = font.render(letter,True,color)
        y_shift = 5 * random.random()
        screen.blit(letter_render,[x + x_shift, y + y_shift])
        x_shift += 15

#Define normal captions function
def Caption(text,color,x,y,size = 36) -> None:
  if size != 36:
    font_used = pygame.font.Font(None, size)
  else:
    font_used = font
  cap = font_used.render(text,True,color)
  screen.blit(cap,[x,y])

#Define the mapbuilder and the presets of the maps
presets = [
    [
        [10,13,13,13,13,13,11],
        [15,4,4,4,4,4,14],
        [15,4,4,4,4,4,14],
        [15,4,4,4,4,4,14],
        [15,4,4,4,4,4,14],
        [15,4,4,4,4,4,14],
        [9,12,12,12,12,12,8]
    ],

    [
        [10,13,13,13,13,13,11],
        [15,4,4,4,4,4,14],
        [15,4,4,4,4,4,14],
        [15,4,4,4,4,4,14],
        [15,4,4,4,4,4,14],
        [15,4,4,4,4,4,14],
        [9,12,12,12,12,12,8]
    ],
]

def MapBuild(screen,room,x,y):
    for row in range(len(presets[room])):
        for column in range(len(presets[room][row])):
            screen.blit(tiles[presets[room][row][column]],[x + column*32,y + row*32])
    return (x + 32,y + 32,(len(presets[room]) -2) * 32,(len(presets[room][0]) - 2) * 32)

def BulletMech():
  enemy_hit_list = []
  global score
  for bullet in bullet_list:
    enemy_hit_list = pygame.sprite.spritecollide(bullet,monster_list,False)
    # Remove the bullet if it flies up off the screen
    if bullet.rect.y < mapsize[1] - 32 or bullet.rect.y > mapsize[1] + mapsize[3] + 32 or bullet.rect.x < mapsize[0] - 32 or bullet.rect.x > mapsize[0] + mapsize[2] + 32:
      bullet_list.remove(bullet)
      all_sprites_list.remove(bullet)
  for enemy in enemy_hit_list:
    enemy.hp -= bullet.damage
    bullet_list.remove(bullet)
    all_sprites_list.remove(bullet)
    score += 1
    print(score)

def ShowHUB(screen,x,y):
  global score
  Caption("Score:{}".format(score),info,x,y)
    
def ShowHP(screen,x,y,hp,maxhp):
  ratio = hp/maxhp
  position_g = (x,y - 10,30 * ratio,5)
  position_r = (x + 30 * ratio,y - 10, 30 - 30 * ratio,5)
  pygame.draw.rect(screen, green, position_g, width=0 )
  pygame.draw.rect(screen, red, position_r, width=0)

def Initialize():
  global hero
  global all_sprites_list
  global monster_list
  global bullet_list
  global mapsize
  global score
  hero = Character(hero_img,0,10,20,20,5)
  mapsize = (0,0,0,0)
  all_sprites_list = pygame.sprite.Group()
  monster_list = pygame.sprite.Group()
  bullet_list = pygame.sprite.Group()
  all_sprites_list.add(hero)
  score = 0
  print("Initialize complete!")
"""
#2.5 Sprites
Define all the sprites class for objects in the game
"""
class PygameObject(pygame.sprite.Sprite):
    """
    This class represents all the objects in the game
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self,imageset,gesture,speed,x,y) -> None:
        super().__init__()
        self.speed = speed
        self.imageset = imageset
        self.image = imageset[gesture][0]
        self.gesture = gesture
        self.rect = self.image.get_rect()
        self.rect.x = x + mapsize[0]
        self.rect.y = y + mapsize[1]
    def reset_location(self,x,y):
        self.rect.x = x + mapsize[0]
        self.rect.y = x + mapsize[1]
    def move_left(self):
        if self.rect.x > mapsize[0] + self.speed:
            self.rect.x -= self.speed
        else:
            self.rect.x = mapsize[0]
        self.gesture = 2
    def move_right(self):
        if self.rect.x < mapsize[0] + mapsize[2] - self.rect.width - self.speed:
            self.rect.x += self.speed
        else:
            self.rect.x = mapsize[0] + mapsize[2] - self.rect.width
        self.gesture = 3
    def move_front(self):
        if self.rect.y < mapsize[1] + mapsize[3] - self.rect.height - self.speed:
            self.rect.y += self.speed
        else:
            self.rect.y = mapsize[1] + mapsize[3] - self.rect.height
        self.gesture = 0
    def move_back(self):
        if self.rect.y > mapsize[1] + self.speed:
            self.rect.y -= self.speed
        else:
            self.rect.y = mapsize[1]
        self.gesture = 1
    def update(self):
        """ Called each frame. """
        
class Monster(PygameObject):
  def __init__(self, imageset, gesture, speed, x, y, hp) -> None:
        super().__init__(imageset, gesture, speed, x, y)
        self.moveCoolDown = 1000
        self.lastMoveTick = 0
        self.maxhp = hp
        self.hp = hp
  def update(self):
    ShowHP(screen,self.rect.x,self.rect.y,self.hp,self.maxhp)
    if self.hp <= 0:
      all_sprites_list.remove(self)
      monster_list.remove(self)
    if pygame.time.get_ticks() > self.lastMoveTick + self.moveCoolDown:
      self.lastMoveTick = pygame.time.get_ticks()
      movx = random.randint(-1,1)
      movy = random.randint(-1,1)
      if movx == -1:
        self.move_left()
      elif movx == 1:
        self.move_right()
      if movy == -1:
        self.move_back()
      elif movy == 1:
        self.move_front()
      self.image = self.imageset[self.gesture][pygame.time.get_ticks() // 150 % 3]

class Character(PygameObject):
    def __init__(self, imageset, gesture, speed, x, y,hp) -> None:
        super().__init__(imageset, gesture, speed, x, y)
        self.isMoveAllowed = False
        self.isShootAllowed = False
        self.isSkillAllowed = False
        self.bulletCoolDown = 250
        self.lastBulletTick = 0
        self.skillCoolDown = 1000
        self.lastSkillTick = 0
        self.maxhp = hp
        self.hp = hp
    
    def update(self):
        ShowHP(screen,self.rect.x,self.rect.y,self.hp,self.maxhp)
        if self.hp <= 0:
          all_sprites_list.remove(self)
        self.image = self.imageset[self.gesture][pygame.time.get_ticks() // 200 % 6]
        key_list = pygame.key.get_pressed()
        if self.isMoveAllowed:
            if key_list[pygame.K_w]:
                self.move_back()
            if key_list[pygame.K_a]:
                self.move_left()
            if key_list[pygame.K_s]:
                self.move_front()
            if key_list[pygame.K_d]:
                self.move_right()
        if self.isShootAllowed:
          if key_list[pygame.K_SPACE]:
            if pygame.time.get_ticks() > self.lastBulletTick + self.bulletCoolDown:
              bullet = Bullet(normal_bullet_img,3,self.gesture,1)
              bullet.rect.x = self.rect.x
              bullet.rect.y = self.rect.y
              bullet_list.add(bullet)
              all_sprites_list.add(bullet)
              self.lastBulletTick = pygame.time.get_ticks()
        if self.isSkillAllowed:
          if key_list[pygame.K_q]:
            if pygame.time.get_ticks() > self.lastSkillTick + self.skillCoolDown:
              bullet = Bullet(rocket_bullet_img,5,self.gesture,5,False)
              bullet.rect.x = self.rect.x
              bullet.rect.y = self.rect.y
              bullet_list.add(bullet)
              all_sprites_list.add(bullet)
              self.lastSkillTick = pygame.time.get_ticks()

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self,image,speed,direction,damage,simple = True):
        # Call the parent class (Sprite) constructor
        super().__init__()
        if not simple:
          self.image = image[direction][0]
        else:
          self.image = image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.direction = direction
        self.simple = simple
        self.imageset = image
        self.damage = damage
    def update(self):
        """ Move the bullet. """
        if self.direction == 0:
          self.rect.y += self.speed
        elif self.direction == 1:
          self.rect.y -= self.speed
        elif self.direction == 2:
          self.rect.x -= self.speed
        elif self.direction == 3:
          self.rect.x += self.speed
        if not self.simple:
          self.image = self.imageset[self.direction][pygame.time.get_ticks() // 50 % 3]

"""
#3 Game Settings
Game configurations & Windows Initialization
"""
#screen configurations
size = (700,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("[Yichen Wang] Pygame ISU Project")

#Loop until the user clicks the close button 
done = False

#controllers for instruction pages & the animation of texts on instruction pages
display_instructions = True 
instruction_page = 1 
cap_x = -50
tutorial_page = -1
tutorial_start_tick = -1
tutorials = ["You can toggle Auto Page Turning By Pressing R key",
"You can also turn the page manually by clicking on the screen",
"The progress of Auto Page Turning is shown on the right lower corner",
"Next Stop: Battle Tutorial",
"You will play as a hero to defeat all monsters in a dungeon",
"You can control your character by WASD keys",
"You can shoot bullets by pressing space key",
"You can use your special ability by pressing Q key",
"Hit by an ememy will reduce your hp, which is displayed on the screen",
"If your hp is reduced to zero or below zero, game over."]

#Manage how fast the screen updates 
clock = pygame.time.Clock()

#auto page turning (APT) controller
isAutoPageEnabled = False

#How long does APT linger in each page
page_linger_time = [-1,-1,1000,7500,65000]

#The starting point of APT
auto_start_tick = -1

"""
#4 Images Import
import all the necessary images for the game
"""

#import images
auto = [pygame.image.load("images/icons/auto.png"),
pygame.image.load("images/icons/auto_25.png"),
pygame.image.load("images/icons/auto_50.png"),
pygame.image.load("images/icons/auto_75.png"),
pygame.image.load("images/icons/auto_100.png")]

tiles = [pygame.image.load("images/maps/brick_1.png"),
pygame.image.load("images/maps/brick_2.png"),
pygame.image.load("images/maps/brick_3.png"),
pygame.image.load("images/maps/brick_4.png"),
pygame.image.load("images/maps/brick_5.png"),
pygame.image.load("images/maps/brick_6.png"),
pygame.image.load("images/maps/brick_7.png"),
pygame.image.load("images/maps/brick_8.png"),
pygame.image.load("images/maps/edge_1.png"),
pygame.image.load("images/maps/edge_2.png"),
pygame.image.load("images/maps/edge_3.png"),
pygame.image.load("images/maps/edge_4.png"),
pygame.image.load("images/maps/edge_5.png"),
pygame.image.load("images/maps/edge_6.png"),
pygame.image.load("images/maps/edge_7.png"),
pygame.image.load("images/maps/edge_8.png")]

hero_img = [
    [pygame.image.load("images/characters/hero_front_1.png"),
    pygame.image.load("images/characters/hero_front_2.png"),
    pygame.image.load("images/characters/hero_front_3.png"),
    pygame.image.load("images/characters/hero_front_4.png"),
    pygame.image.load("images/characters/hero_front_5.png"),
    pygame.image.load("images/characters/hero_front_6.png")
    ],
    [pygame.image.load("images/characters/hero_back_1.png"),
    pygame.image.load("images/characters/hero_back_2.png"),
    pygame.image.load("images/characters/hero_back_3.png"),
    pygame.image.load("images/characters/hero_back_4.png"),
    pygame.image.load("images/characters/hero_back_5.png"),
    pygame.image.load("images/characters/hero_back_6.png"),
    ],
    [pygame.image.load("images/characters/hero_left_1.png"),
    pygame.image.load("images/characters/hero_left_2.png"),
    pygame.image.load("images/characters/hero_left_3.png"),
    pygame.image.load("images/characters/hero_left_4.png"),
    pygame.image.load("images/characters/hero_left_5.png"),
    pygame.image.load("images/characters/hero_left_6.png")
    ],
    [pygame.image.load("images/characters/hero_right_1.png"),
    pygame.image.load("images/characters/hero_right_2.png"),
    pygame.image.load("images/characters/hero_right_3.png"),
    pygame.image.load("images/characters/hero_right_4.png"),
    pygame.image.load("images/characters/hero_right_5.png"),
    pygame.image.load("images/characters/hero_right_6.png")
    ],
    ]

slime_img = [
  [pygame.image.load("images/characters/slime_front_1.png"),
  pygame.image.load("images/characters/slime_front_2.png"),
  pygame.image.load("images/characters/slime_front_3.png"),
  ],
  [pygame.image.load("images/characters/slime_back_1.png"),
  pygame.image.load("images/characters/slime_back_2.png"),
  pygame.image.load("images/characters/slime_back_3.png"),
  ],
  [pygame.image.load("images/characters/slime_left_1.png"),
  pygame.image.load("images/characters/slime_left_2.png"),
  pygame.image.load("images/characters/slime_left_3.png"),
  ],
  [pygame.image.load("images/characters/slime_right_1.png"),
  pygame.image.load("images/characters/slime_right_2.png"),
  pygame.image.load("images/characters/slime_right_3.png"),
  ],
]

normal_bullet_img = pygame.image.load("images/effects/bullet_1.png")

rocket_bullet_img = [
  [pygame.image.load("images/effects/rocket_front_1.png"),
  pygame.image.load("images/effects/rocket_front_2.png"),
  pygame.image.load("images/effects/rocket_front_3.png"),
  ],
  [pygame.image.load("images/effects/rocket_back_1.png"),
  pygame.image.load("images/effects/rocket_back_2.png"),
  pygame.image.load("images/effects/rocket_back_3.png"),
  ],
  [pygame.image.load("images/effects/rocket_left_1.png"),
  pygame.image.load("images/effects/rocket_left_2.png"),
  pygame.image.load("images/effects/rocket_left_3.png"),
  ],
  [pygame.image.load("images/effects/rocket_right_1.png"),
  pygame.image.load("images/effects/rocket_right_2.png"),
  pygame.image.load("images/effects/rocket_right_3.png"),
  ],
]

"""
#5 Map and Character
Initialize the map and character in the game
"""

#define the position of the map
mapsize = (0,0,0,0)
#Define the Sprite Groups
all_sprites_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
monster_list = pygame.sprite.Group()
#define characters
hero = Character(hero_img,0,10,20,20,5)
all_sprites_list.add(hero)
#Score of the player
score = 0

#initialize the game
Initialize()
#Instruction Page Loop 
while not done and display_instructions: 
  for event in pygame.event.get():
    if event.type == pygame.QUIT: 
      done = True 
    if event.type == pygame.KEYDOWN:
      key_list = pygame.key.get_pressed()
      if key_list[pygame.K_r]:
        if isAutoPageEnabled:
          print("auto next page disabled")
          isAutoPageEnabled = False
        else:
          print("auto next page enabled")
          auto_start_tick = pygame.time.get_ticks()
          isAutoPageEnabled = True
    if event.type == pygame.MOUSEBUTTONDOWN: 
      instruction_page += 1
      if instruction_page == 2:
        auto_start_tick = pygame.time.get_ticks()
        isAutoPageEnabled = True
  screen.fill(intro_bg)

  #automatic page turning controller
  if isAutoPageEnabled and instruction_page < len(page_linger_time) and page_linger_time[instruction_page] != -1:
    prog = (pygame.time.get_ticks() - auto_start_tick) / page_linger_time[instruction_page]
    if pygame.time.get_ticks() - auto_start_tick >= page_linger_time[instruction_page]:
      instruction_page += 1
      auto_start_tick = pygame.time.get_ticks()
    if prog < 0.2:
      screen.blit(auto[0],[600,400])
    elif prog < 0.4:
      screen.blit(auto[1],[600,400])
    elif prog < 0.6:
      screen.blit(auto[2],[600,400])
    elif prog < 0.8:
      screen.blit(auto[3],[600,400])
    else:
      screen.blit(auto[4],[600,400])
    Caption("Automatic Page",info,550,450,24)
    Caption("Turning Enabled",info,550,470,24)

  if instruction_page == 1: 
    Caption("Pixel Dungeons",white,cap_x,10)
    Caption("Designed and Programmed by Yichen Wang",info,cap_x * 5 - 40,50,24)
    if cap_x < 10:
      cap_x += 2
    else:
      cap_x = 10
    Caption("Click to Start",white,270,450 - cap_x * 2)
  elif instruction_page == 2: 
    #make the caption blink in red
    if pygame.time.get_ticks() // 120 % 2 == 0:
      Caption("Click to Start",white,270,430)
    else:
      Caption("Click to Start",red,270,430)
    JumpingCaption("Pixel Dungeons",red,10,10)
  elif instruction_page == 3:
    if tutorial_page != instruction_page:
      tutorial_start_tick = pygame.time.get_ticks()
      tutorial_page = instruction_page
    Caption("Welcome to the Pixel Dungeons by Yichen W.",white,10,10)
    Caption("Here are some general tutorials",white,10,50)
    tutor_index = (pygame.time.get_ticks()-tutorial_start_tick) // 2000
    if tutor_index < 4:
      Caption(tutorials[tutor_index],info,10,100,30)
    else:
      instruction_page += 1
  elif instruction_page == 4:
    if tutorial_page != instruction_page:
      tutorial_start_tick = pygame.time.get_ticks()
      tutorial_page = instruction_page
    Caption("Welcome to the Pixel Dungeons by Yichen W.",white,10,10)
    Caption("Here are some battle tutorials",white,10,50)
    tutor_index = (pygame.time.get_ticks()-tutorial_start_tick) // 10000
    tutor_index += 4
    if tutor_index < len(tutorials):
      Caption(tutorials[tutor_index],info,10,100,30)
    else:
      instruction_page += 1
    mapsize = MapBuild(screen,0,20,150)
    if tutor_index == 4:
      hero.reset_location(10,10)
    elif tutor_index == 5:
      hero.isMoveAllowed = True
    elif tutor_index == 6:
      hero.isShootAllowed = True
    elif tutor_index == 7:
      hero.isSkillAllowed = True
    elif tutor_index == 8 and len(monster_list) < 2:
      monster = Monster(slime_img,0,5,random.randint(0,mapsize[2]),random.randint(0,mapsize[3]),2)
      monster_list.add(monster)
      all_sprites_list.add(monster)
    elif tutor_index == 9:
      for enemy in monster_list:
        monster_list.remove(enemy)
        all_sprites_list.remove(enemy)
      hero.hp -= 0.02
    elif tutor_index >= 10:
      instruction_page += 1
    all_sprites_list.update()
    BulletMech()
    all_sprites_list.draw(screen)
    ShowHUB(screen,20,400)
  elif instruction_page == 5:
    Caption("Tutorial Finished, Now enjoy your game!",info,100,200)
  else:
    display_instructions = False
    

  #update with 60 fps
  clock.tick(60)
  pygame.display.flip()

Initialize()
#Main Program Loop 
while not done:
  #Main event loop 
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT: 
      done = True 
      #If user clicks close, it will end the main loop. 

  #Set the screen
  screen.fill(white)

  #Drawing code here 
  MapBuild(screen,0,20,20)
  
  #Update the screen 
  pygame.display.flip()

  #Set number of frames per second 
  clock.tick(60)

#Close the window and quit 
pygame.quit()