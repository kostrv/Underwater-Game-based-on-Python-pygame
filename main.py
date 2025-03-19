import os
try: 
    import pygame
except ModuleNotFoundError: 
    os.system('pip install pygame')	
    import pygame
    
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI
from main_menu import MainMenu
from game_data import levels

class Game:
    def __init__(self):
        # Game attributes
        self.max_level = 0
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # Main menu instance
        self.main_menu = MainMenu(screen, 0, self.max_level, self.create_overworld)
        self.status = 'main_menu'
        # UI instance
        self.ui = UI(screen)

        # Sound effects
        self.death_sound = pygame.mixer.Sound(death_sound)
        self.death_sound.set_volume(0.1)

    def create_level(self, current_level):
        self.cur_health = 100
        self.status = 'level'
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health, self.check_game_over)      

    def create_main_menu(self, current_level, new_max_level):
        self.main_menu = MainMenu(screen, current_level, new_max_level)
        self.status = 'main_menu'

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level: # Update maximum level
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        # Stop music and switch to level menu music
        pygame.mixer.music.stop()
        pygame.mixer.music.load(overworld_music)
        pygame.mixer.music.play(-1)
    
    def check_game_over(self, current_level):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.overworld = Overworld(current_level, self.max_level, screen, self.create_level) 
            self.status = 'overworld'
            self.death_sound.play()
            # Stop music and switch to level menu music
            pygame.mixer.music.stop()
            pygame.mixer.music.load(overworld_music)
            pygame.mixer.music.play(-1)
    
    # Start
    def run(self):
        if self.status == 'main_menu':
            self.main_menu.run()
        elif self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health) 
            self.ui.show_coins(self.coins)

# General setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)  # Create a full-screen window
pygame.display.set_caption("UNDERWATER ADVENTURE")
pygame.display.set_icon(pygame.image.load(screen_icon_image))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game.run()
    pygame.display.update()
    clock.tick(60)
