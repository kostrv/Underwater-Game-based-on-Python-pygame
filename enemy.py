import pygame 
from settings import *
from tiles import AnimatedTile
from random import randint
from support import import_folder

class Enemy(AnimatedTile): 
    def __init__(self, size, x, y, path): 
        super().__init__(size, x, y, path)
        self.rect.y += size - self.image.get_size()[1] # Assigning the correct position based on the given image
        self.speed = 1 
        self.is_explodes = False
        self.player_collide = False # Player collision flag

    def enemy_explosion(self): # Explosion after destruction
        self.frames = import_folder(enemy_explosion_images) # Switch animation frames to new ones
        # Animation and destruction after its completion
        self.frame_index += 0.15
        if self.frame_index <= len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

    def move(self):
        self.rect.x -= self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1 
        
    def update(self):
        if not self.is_explodes: # If explosion is not happening
            self.animate()
            self.move()
            self.reverse_image()
        else:
            self.enemy_explosion()
            
# Decoration, no interaction with the player
class DecorationFish(Enemy): 
    def __init__(self, size, x, y, path, minspeed, maxspeed):
        super().__init__(size, x, y, path)
        self.speed = randint(minspeed, maxspeed)
    
    def move(self):
        self.rect.x -= self.speed
