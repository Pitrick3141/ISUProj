"""
#1 Initialization
Import Library & Initialize Pygame
Basic Configurations
"""
#Import library 
from glob import glob
import pygame
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
        [10,13,13,13,13,13,13,13,13,11,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [15,4,4,4,4,4,4,4,4,14],
        [15,4,4,4,4,4,4,4,4,14],
        [15,4,4,4,4,4,4,4,4,14],
        [15,4,4,4,4,4,4,4,4,14],
        [15,4,4,4,4,4,4,4,4,9,13,13,11],
        [15,4,4,4,4,4,4,4,4,4,4,4,14],
        [15,4,4,4,4,4,4,4,4,4,4,4,9,13,13,13,13,11],
        [15,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,14],
        [15,4,4,4,4,4,4,4,4,4,4,4,4,4,4,10,12,8],
        [15,4,4,4,4,4,4,4,4,4,4,4,4,4,4,14],
        [9,12,12,12,12,12,12,12,12,12,12,12,12,12,12,8]
    ],
]
moveable_coor = []
for i in range(16):
  moveable_coor.append([0]*22)

#Define the function to generate monsters randomly
def GenerateMonsters(image,gesture,speed,hp,worth,number):
  for i in range(number):
    x_coor = random.randint(0,21)
    y_coor = random.randint(0,15)
    while moveable_coor[y_coor][x_coor] != 1 or ((x_coor*32 - hero.rect.x) ** 2 + (y_coor*2 - hero.rect.y) ** 2) ** 0.5 < 64:
      x_coor = random.randint(0,21)
      y_coor = random.randint(0,15)
    monster = Monster(image,gesture,speed,x_coor*32,y_coor*32,hp,worth)
    monster_list.add(monster)
    all_sprites_list.add(monster,layer=1)

#Define the function to generate coins randomly
def GenerateCoins(number):
  for i in range(number):
    x_coor = random.randint(0,21)
    y_coor = random.randint(0,15)
    while moveable_coor[y_coor][x_coor] != 1:
      x_coor = random.randint(0,21)
      y_coor = random.randint(0,15)
    coin = Coins(x_coor * 32,y_coor * 32)
    item_list.add(coin)
    all_sprites_list.add(coin,layer=0)

#Define the function to build the map
def MapBuild(screen,room,x,y):
    for row in range(len(presets[room])):
        for column in range(len(presets[room][row])):
          if presets[room][row][column] < len(tiles) and presets[room][row][column] > 0:
            screen.blit(tiles[presets[room][row][column]],[x + column*32,y + row*32])
            if presets[room][row][column] in [0,1,2,3,4]:
                  moveable_coor[row][column] = 1
            elif presets[room][row][column] in [8,9,10,11,12,13,14,15]:
                  moveable_coor[row][column] = 2
    return (x,y,len(presets[room]) * 32,len(presets[room][0]) * 32)

#Define the function to show moveable area
isDebugMove = False
def DebugMove():
  for row in range(len(moveable_coor)):
    for column in range(len(moveable_coor[row])):
      if moveable_coor[row][column] == 1 and row < size[1] and column<size[0]:
        pygame.draw.rect(screen,green,(column*32 + mapsize[0],row*32 + mapsize[1],32,32),width=0)
      elif moveable_coor[row][column] == 2 and row < size[1] and column<size[0]:
        pygame.draw.rect(screen,red,(column*32 + mapsize[0],row*32 + mapsize[1],32,32),width=0)

#Define the function to check if the coordinate is moveable
def CheckMove(x,y,dx,dy,isPlayer=False):
  des_x = x + dx 
  des_y = y + dy 
  coor_des_x = (des_x - mapsize[0]) // 32
  coor_des_y = (des_y - mapsize[1]) // 32
  if isPlayer:
    if moveable_coor[coor_des_y][coor_des_x] == 1:
      return True
    else:
      return False
  else:
    if moveable_coor[coor_des_y][coor_des_x] == 1 or moveable_coor[coor_des_y][coor_des_x] == 2:
      return True
    else:
      return False

#Define the function to calculate bullets mechanism
def BulletMech():
  enemy_hit_list = []
  for bullet in bullet_list:
    enemy_hit_list = pygame.sprite.spritecollide(bullet,monster_list,False)
    # Remove the bullet if it flies up off the screen
    if not moveable_coor[(bullet.rect.y - mapsize[1]) // 32][(bullet.rect.x - mapsize[0]) // 32]:
      bullet_list.remove(bullet)
      all_sprites_list.remove(bullet)
  for enemy in enemy_hit_list:
    enemy.hp -= bullet.damage
    bullet_list.remove(bullet)
    all_sprites_list.remove(bullet)

#Define the function to calculate collision mechanism
def CollideMech():
  enemy_attack_list = []
  enemy_attack_list = pygame.sprite.spritecollide(hero,monster_list,False)
  item_touch_list = []
  item_touch_list = pygame.sprite.spritecollide(hero,item_list,False)
  for enemy in enemy_attack_list:
    if pygame.time.get_ticks() > hero.lastCollideTick + hero.collideProtection:
      hero.hp -= 1
      hero.lastCollideTick = pygame.time.get_ticks()
    if enemy.rect.x > hero.rect.x:
      hero.move_left()
      enemy.move_right()
    else:
      hero.move_right()
      enemy.move_left()
    if enemy.rect.y > hero.rect.y:
      hero.move_front()
      enemy.move_back()
    else:
      hero.move_back()
      enemy.move_front()
  for item in item_touch_list:
    item.touch()

#Define the function to display the HUB
def ShowHUB(screen,x,y):
  global score
  global wave
  Caption("Score: {} Current Wave: {}-{}".format(score,stage,wave),info,x,y)
  Caption("Key: {} Chest Open: {}/3".format(hero.key,hero.chest),info,x,y + 30,24)
  if door.open:
    Caption("Congratulations! You Win!",red,x,y + 50,24)
    Caption("Now you can leave the game or experience the endless challanges!",red,x,y+70,24)
  elif not door.locked:
    Caption("Door is now unlocked! Get close to the door and press E to open it",info,x,y + 50,24)
  if hero.hp <= 0:
    Caption("You Died! Press R to Restart the game!",red,100,200,40)
    if pygame.key.get_pressed()[pygame.K_r]:
      Initialize()
      SceneInit()

#Define the function to display the HP bar
def ShowHP(screen,x,y,hp,maxhp):
  ratio = hp/maxhp
  if ratio < 0:
    ratio = 0
  position_g = (x,y - 10,30 * ratio,5)
  position_r = (x + 30 * ratio,y - 10, 30 - 30 * ratio,5)
  pygame.draw.rect(screen, green, position_g, width=0 )
  pygame.draw.rect(screen, red, position_r, width=0)

#Define the function to initialize the game
def Initialize():
  global hero
  global all_sprites_list
  global monster_list
  global bullet_list
  global item_list
  global mapsize
  global score
  global wave
  global stage
  hero = Character(hero_img,0,5,20,20,10)
  mapsize = (0,0,0,0)
  all_sprites_list.empty()
  monster_list.empty()
  bullet_list.empty()
  item_list.empty()
  all_sprites_list.add(hero,layer=2)
  score = 0
  wave = 0
  stage = 0
  print("Initialize complete!")

#Define the function to reset the map
def SceneInit():
  hero.reset_location(70,70)
  door = Door(550,275)
  item_list.add(door)
  all_sprites_list.add(door,layer=0)

  chests = [Chest(100,40,1),Chest(350,200,2),Chest(150,350,3)]
  for chest in chests:
    item_list.add(chest)
    all_sprites_list.add(chest,layer=0)

"""
#2.5 Sprites
Define all the sprites class for objects in the game
"""

#Define the father class for all objects
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
    def move_left(self,isPlayer = False):
      if CheckMove(self.rect.x,self.rect.y,-self.speed,0,isPlayer):
        self.rect.x -= self.speed
      self.gesture = 2
    def move_right(self,isPlayer = False):
      if CheckMove(self.rect.x + self.rect.width,self.rect.y,self.speed,0,isPlayer):
        self.rect.x += self.speed
      self.gesture = 3
    def move_front(self,isPlayer = False):
      if CheckMove(self.rect.x,self.rect.y + self.rect.height,0,self.speed,isPlayer):
        self.rect.y += self.speed
      self.gesture = 0
    def move_back(self,isPlayer = False):
      if CheckMove(self.rect.x,self.rect.y,0,-self.speed,isPlayer):
        self.rect.y -= self.speed
      self.gesture = 1
    def update(self):
        """ Called each frame. """

#Define the class for all monsters
class Monster(PygameObject):
  def __init__(self, imageset, gesture, speed, x, y, hp,worth) -> None:
        super().__init__(imageset, gesture, speed, x, y)
        self.moveCoolDown = 100
        self.lastMoveTick = 0
        self.maxhp = hp
        self.hp = hp
        self.worth = worth
  def update(self):
    global score
    ShowHP(screen,self.rect.x,self.rect.y,self.hp,self.maxhp)
    if self.hp <= 0:
      all_sprites_list.remove(self)
      monster_list.remove(self)
      for i in range(self.worth):
        coin = Coins(self.rect.x + random.randint(-15,15),self.rect.y + random.randint(-15,15))
        item_list.add(coin)
        all_sprites_list.add(coin,layer=0)
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

#Define the class for player character
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
        self.key = 0
        self.chest = 0
        self.collideProtection = 1000
        self.lastCollideTick = 0
    def update(self):
        ShowHP(screen,self.rect.x,self.rect.y,self.hp,self.maxhp)
        if self.hp <= 0:
          all_sprites_list.remove(self)
        self.image = self.imageset[self.gesture][pygame.time.get_ticks() // 200 % 6]
        key_list = pygame.key.get_pressed()
        if self.isMoveAllowed:
            if key_list[pygame.K_w]:
                self.move_back(True)
            if key_list[pygame.K_a]:
                self.move_left(True)
            if key_list[pygame.K_s]:
                self.move_front(True)
            if key_list[pygame.K_d]:
                self.move_right(True)
        if self.isShootAllowed:
          if key_list[pygame.K_SPACE]:
            if pygame.time.get_ticks() > self.lastBulletTick + self.bulletCoolDown:
              bullet = Bullet(normal_bullet_img,3,self.gesture,1)
              bullet.rect.x = self.rect.x
              bullet.rect.y = self.rect.y
              bullet_list.add(bullet)
              all_sprites_list.add(bullet,layer=1)
              self.lastBulletTick = pygame.time.get_ticks()
        if self.isSkillAllowed:
          if key_list[pygame.K_q]:
            if pygame.time.get_ticks() > self.lastSkillTick + self.skillCoolDown:
              bullet = Bullet(rocket_bullet_img,5,self.gesture,5,False)
              bullet.rect.x = self.rect.x
              bullet.rect.y = self.rect.y
              bullet_list.add(bullet)
              all_sprites_list.add(bullet,layer=1)
              self.lastSkillTick = pygame.time.get_ticks()
        if key_list[pygame.K_SPACE] and pygame.key.get_mods() & pygame.KMOD_SHIFT and pygame.key.get_mods() & pygame.KMOD_CTRL:
          for enemy in monster_list:
            enemy.hp -= enemy.maxhp * 0.2

#Define the class for all bullets
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

#Define the father class for all interactable objects
class Item(PygameObject):
  def __init__(self, imageset, x, y) -> None:
    super().__init__(imageset, 0, 0, x, y)

#Define the class for coins
class Coins(Item):
  def __init__(self, x, y) -> None:
    super().__init__(coins_img, x, y)
  def update(self):
    self.image = self.imageset[self.gesture][pygame.time.get_ticks() // 150 % 4]
    if self.rect.x >= size[0] or self.rect.y >= size[1] or self.rect.x < 0 or self.rect.y < 0:
      self.rect.x = hero.rect.x + random.randint(-20,20)
      self.rect.y = hero.rect.y + random.randint(-20,20)
    if moveable_coor[self.rect.y//32][self.rect.x//32] != 1:
      self.rect.x = hero.rect.x + random.randint(-20,20)
      self.rect.y = hero.rect.y + random.randint(-20,20)
  def touch(self):
    global score
    score += 1
    all_sprites_list.remove(self)
    item_list.remove(self)

#Define the class for keys
class Key(Item):
  def __init__(self, x, y) -> None:
    super().__init__(key_img, x, y)
    self.image = self.imageset[0][0]
  def touch(self):
    hero.key += 1
    all_sprites_list.remove(self)
    item_list.remove(self)

#Define the class for chests
class Chest(Item):
  def __init__(self,x,y,id) -> None:
    super().__init__(chest_img,x,y)
    self.image = chest_img[0][0]
    self.locked = True
    self.id = id
  def touch(self):
    if hero.key > 0 and self.locked == True:
      hero.key -= 1
      self.locked = False
      self.image = chest_img[0][1]
      hero.chest += 1
      for i in range(random.randint(5,10) * self.id):
        coin = Coins(self.rect.x + random.randint(-15,15),self.rect.y + random.randint(-15,15))
        item_list.add(coin)
        all_sprites_list.add(coin,layer=0)

#Define the class for doors
class Door(Item):
  def __init__(self,x,y) -> None:
    super().__init__(door_img,x,y)
    self.image = door_img[0][0]
    self.locked = True
    self.open = False
  def touch(self):
    global door_open_tick
    if hero.chest >= 3 and self.locked:
      self.locked = False
      self.image = door_img[0][1]
    if pygame.key.get_pressed()[pygame.K_e] and not self.locked and not self.open:
      if door_open_tick == -1:
        door_open_tick = pygame.time.get_ticks()
        self.open = True
  def update(self):
    if self.open and self.image != door_img[1][3]:
      self.image = door_img[1][(pygame.time.get_ticks()-door_open_tick)//200%4]
      
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
"If your hp is reduced to zero or below zero, game over.",
"There are 4 waves of enemies in each stage",
"When you defeat a stage, a key appear in the middle of the map",
"You can open chests using the key",
"If all three chests are opened, the door will be unlocked",
"Then get close to the door and open it to win the game"]

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

coins_img = [[pygame.image.load("images/maps/coin_1.png"),
pygame.image.load("images/maps/coin_2.png"),
pygame.image.load("images/maps/coin_3.png"),
pygame.image.load("images/maps/coin_4.png")]]

key_img = [[pygame.image.load("images/maps/key.png")]]
chest_img = [[pygame.image.load("images/maps/chest_closed.png"),pygame.image.load("images/maps/chest_open.png")]]
door_img = [[pygame.image.load("images/maps/door_locked.png"),pygame.image.load("images/maps/door_unlocked.png")],
[pygame.image.load("images/maps/door_1.png"),
pygame.image.load("images/maps/door_2.png"),
pygame.image.load("images/maps/door_3.png"),
pygame.image.load("images/maps/door_4.png")]]

"""
#5 Map and Character
Initialize the map and character in the game
"""

#define the position of the map
mapsize = (0,0,0,0)
#Define the Sprite Groups
all_sprites_list = pygame.sprite.LayeredUpdates()
bullet_list = pygame.sprite.Group()
monster_list = pygame.sprite.Group()
item_list = pygame.sprite.Group()
#define characters
hero = Character(hero_img,0,5,100,100,10)
all_sprites_list.add(hero,layer=2)
#Score of the player
score = 0
#Wave count of monsters
wave = 0
#Monster States of each wave
monster_stat = [(1,3,1,3),(2,5,3,3),(3,5,5,5),(4,20,10,1)]
#Current Game Stage
stage = 0
door_open_tick = -1

#initialize the game
Initialize()
#Instruction Page Loop 
while not done and display_instructions: 
  for event in pygame.event.get():
    if event.type == pygame.QUIT: 
      done = True 
    if event.type == pygame.KEYDOWN:
      key_list = pygame.key.get_pressed()
      if key_list[pygame.K_m]:
        if not isDebugMove:
          isDebugMove = True
          print("Move Debug Enabled")
        else:
          isDebugMove = False
          print("Move Debug Disabled")
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
    tutor_index = (pygame.time.get_ticks()-tutorial_start_tick) // 5000
    tutor_index += 4
    if tutor_index < len(tutorials):
      Caption(tutorials[tutor_index],info,10,100,30)
    else:
      instruction_page += 1
    mapsize = MapBuild(screen,0,20,150)
    if tutor_index == 4:
      hero.reset_location(100,100)
    elif tutor_index == 5:
      hero.isMoveAllowed = True
    elif tutor_index == 6:
      hero.isShootAllowed = True
    elif tutor_index == 7:
      hero.isSkillAllowed = True
    elif tutor_index == 8 and len(monster_list) == 0:
      GenerateMonsters(slime_img,0,1,3,0,1)
    elif tutor_index == 9:
      for enemy in monster_list:
        monster_list.remove(enemy)
        all_sprites_list.remove(enemy)
      hero.hp -= hero.maxhp * 0.03
    all_sprites_list.update()
    BulletMech()
    CollideMech()
    all_sprites_list.draw(screen)
    if isDebugMove:
      DebugMove()
  elif instruction_page == 5:
    Caption("Tutorial Finished, Now enjoy your game!",info,100,200)
    isAutoPageEnabled = False
  else:
    display_instructions = False
    

  #update with 60 fps
  clock.tick(60)
  pygame.display.flip()

#Reset the game
Initialize()
hero.reset_location(70,70)
door = Door(550,275)
item_list.add(door)
all_sprites_list.add(door,layer=0)

chests = [Chest(100,40,1),Chest(350,200,2),Chest(150,350,3)]
for chest in chests:
  item_list.add(chest)
  all_sprites_list.add(chest,layer=0)

#Main Program Loop 
while not done:
  #Main event loop 
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT: 
      done = True 
      #If user clicks close, it will end the main loop. 
    if event.type == pygame.KEYDOWN:
      key_list = pygame.key.get_pressed()
      if key_list[pygame.K_m]:
        if not isDebugMove:
          isDebugMove = True
          print("Move Debug Enabled")
        else:
          isDebugMove = False
          print("Move Debug Disabled")

  #Set the screen
  screen.fill(white)

  #Drawing code here 
  mapsize = MapBuild(screen,1,20,20)
  all_sprites_list.update()
  BulletMech()
  CollideMech()
  all_sprites_list.draw(screen)
  ShowHUB(screen,10,410)
  hero.isMoveAllowed = True
  hero.isShootAllowed = True
  hero.isSkillAllowed = True
  
  if len(monster_list) == 0 and wave < len(monster_stat):
    GenerateMonsters(slime_img,0,monster_stat[wave][0],monster_stat[wave][1],monster_stat[wave][2],monster_stat[wave][3] * (stage + 1))
    wave += 1
  if wave == 4 and len(monster_list) == 0:
    key = Key(200,200)
    item_list.add(key)
    all_sprites_list.add(key,layer=0)
    stage += 1
    wave = 0
  if isDebugMove:
    DebugMove()
  #Update the screen 
  pygame.display.flip()

  #Set number of frames per second 
  clock.tick(60)

#Close the window and quit 
pygame.quit()