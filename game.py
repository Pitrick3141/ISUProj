#Import library 
from functools import total_ordering
from typing import Literal
import pygame
from sprites import *
import math 
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

#Define special effect for captions
def JumpingCaption(text:str,color:tuple[Literal[0],Literal[0],Literal[0]],x:int,y:int) -> None:
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
def Caption(text:str,color:tuple[Literal[0],Literal[0],Literal[0]],x:int,y:int,size:int = 36) -> None:
  if size != 36:
    font_used = pygame.font.Font(None, size)
  else:
    font_used = font
  cap = font_used.render(text,True,color)
  screen.blit(cap,[x,y])

#screen configurations
size = (700,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("[Yichen Wang] Pygame ISU Project")

#Loop until the user clicks the close button 
done = False

#controllers for instruction pages
display_instructions = True 
instruction_page = 1 

#define user events
NEXT_PAGE = pygame.USEREVENT +1

#Manage how fast the screen updates 
clock = pygame.time.Clock()

#control the animation of texts on instruction pages
cap_x = -50
tutorial_page = -1
tutorial_start_tick = -1
tutorials = ["You can toggle Auto Page Turning By Pressing \"A\"",
"You can also turn the page manually by clicking on the screen",
"The progress of Auto Page Turning is shown on the right lower corner",
"Next Stop: Battle Tutorial",
"Battle1",
"Battle2"]

#auto page turning (APT) controller
isAutoPageEnabled = False
#APT Icons
auto = [pygame.image.load("auto.png"),
pygame.image.load("auto_25.png"),
pygame.image.load("auto_50.png"),
pygame.image.load("auto_75.png"),
pygame.image.load("auto_100.png")]
#How long does APT linger in each page
page_linger_time = [-1,-1,1000,7500,10000]
#The starting point of APT
auto_start_tick = -1

#import images


#Instruction Page Loop 
while not done and display_instructions: 
  for event in pygame.event.get():
    if event.type == pygame.QUIT: 
      done = True 
    if event.type == pygame.KEYDOWN:
      if pygame.K_a:
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
    if cap_x < 10:
      cap_x += 3
    else:
      cap_x = 10
    Caption("Click to Start",white,270,450)
  elif instruction_page == 2: 
    #make the caption blink in red
    if pygame.time.get_ticks() // 120 % 2 == 0:
      Caption("Click to Start",white,270,450)
    else:
      Caption("Click to Start",red,270,450)
    JumpingCaption("Pixel Dungeons",red,10,10)
  elif instruction_page == 3:
    if tutorial_page != instruction_page:
      tutorial_start_tick = pygame.time.get_ticks()
      tutorial_page = instruction_page
    Caption("Welcome to the Pixel Dungeons by Yichen W.",white,10,10)
    Caption("Here are some tutorials for the game",white,10,50)
    tutor_index = (pygame.time.get_ticks()-tutorial_start_tick) // 2000
    if tutor_index < 4:
      Caption(tutorials[tutor_index],info,10,100,30)
  elif instruction_page == 4:
    if tutorial_page != instruction_page:
      tutorial_start_tick = pygame.time.get_ticks()
      tutorial_page = instruction_page
    tutor_index = (pygame.time.get_ticks()-tutorial_start_tick) // 2000
    tutor_index += 4
    if tutor_index < len(tutorials):
      Caption(tutorials[tutor_index],info,10,100,30)

  #update with 60 fps
  clock.tick(60)
  pygame.display.flip()

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
  
  
  #Update the screen 
  pygame.display.flip()

  #Set number of frames per second 
  clock.tick(60)

#Close the window and quit 
pygame.quit()