import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite): # Parent class
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

class StaticTile(Tile): # Static tile used for stationary images
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface.convert_alpha()

class Submarine(StaticTile): # Creating a subclass to modify the rect for different positioning
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y, surface)
        self.rect = self.image.get_rect(center=(x, y))

class AnimatedTile(Tile): # Animated tile used for active objects
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

class Coin(AnimatedTile): # Creating a subclass for a coin to modify the rect for center alignment and handle point values
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value

class Decoration(pygame.sprite.Sprite): # Creating a subclass to modify the drawing point and load the image inside the class
    def __init__(self, x, y, surface):
        super().__init__()
        self.image = pygame.image.load(surface)
        self.rect = self.image.get_rect(bottomleft=(x, y))

class AnimatedPlant(AnimatedTile): # Creating a subclass for a plant to modify the rect for centered alignment with a downward offset
    def __init__(self, size, x, y, path, y_offset_factor):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / y_offset_factor)
        self.rect = self.image.get_rect(center=(center_x, center_y))

class Plant(Decoration): # Creating a subclass to modify the drawing point with an offset
    def __init__(self, size, x, y, surface, y_offset_factor):
        super().__init__(x, y, surface)
        center_x = x + int(size / 2)
        center_y = y + int(size / y_offset_factor)
        self.rect = self.image.get_rect(center=(center_x, center_y))
