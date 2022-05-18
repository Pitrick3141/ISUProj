#Import library 
import pygame
import math 
import random

#Define colours 
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)

#Define Jumping effect for captions
def JumpingCaption(text,color,x,y):
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

#Initialize Pygame
pygame.init()

#Set the width and height of the screen
size = (700,500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("[Yichen Wang] Pygame ISU Project")

#Loop until the user clicks the close button 
done = False

font = pygame.font.Font(None, 36)

display_instructions = True 
instruction_page = 1 

#Manage how fast the screen updates 
clock = pygame.time.Clock()

#Instruction Page Loop 
while not done and display_instructions: 
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT: 
      done = True 
    if event.type == pygame.MOUSEBUTTONDOWN: 
      instruction_page += 1 
      if instruction_page == 3: 
        display_instructions = False 
  screen.fill(black)

  if instruction_page == 1: 
    text = font.render("Pixel Dungeons",True,white)
    screen.blit(text,[10,10])

  if instruction_page == 2: 
    JumpingCaption("Pixel Dungeons",red,10,10)
    NEXT_PAGE = pygame.USEREVENT +1
    pygame.time.set_timer(NEXT_PAGE,1000)
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