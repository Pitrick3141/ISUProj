import pygame
#define gamesprite class for easy creating & updating spirits
class GameSprite(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y, speed=1):
        
        super().__init__()
        
        # load images
        self.image = pygame.image.load(image)
        self.rect = (x,y,self.image.get_rect().width,self.image.get_rect().height)
        self.speed = speed
        self.speedx = 0
        self.speedy = 0
 
    def update(self, *args):
        # update the position of the spirit
        self.rect.y += self.speedy
        self.rect.x += self.speedx