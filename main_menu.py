import pygame, sys
from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, size): 
        super().__init__()
        self.pos = pos
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), self.size)
        self.rect = self.image.get_rect(center=pos)

class Text():
    def __init__(self, text, pos, size, surface, color):
        self.display_surface = surface
        self.pos = pos
        self.font = pygame.font.Font(pixel_font, size)  # Font creation
        self.text_surface = self.font.render(str(text), False, color) 
        self.text_rect = self.text_surface.get_rect(center=pos)

    def update_text(self):
        self.display_surface.blit(self.text_surface, self.text_rect)  # Rendering the font
        
class MainMenu():
    def __init__(self, surface, current_level, new_max_level, create_overworld):
        # General setup
        self.current_level = current_level
        self.new_max_level = new_max_level
        self.create_overworld = create_overworld
        self.display_surface = surface
        self.midground = pygame.transform.flip(pygame.transform.scale(pygame.image.load(midground_image).convert_alpha(), (screen_width, screen_height)), True, False)
        self.background = pygame.transform.flip(pygame.transform.scale(pygame.image.load(background_image).convert(), (screen_width, screen_height)), True, False)
        self.midground_speed = 1
        self.midground_x = 0

        # Creating instances
        # Buttons
        self.play_button = Button(play_button_non_active_image, (screen_width / 2, screen_height / 2), (400,200))
        self.exit_button = Button(exit_button_non_active_image, (screen_width / 2, screen_height / 1.35), (400,200))
        # Text
        self.text_above = Text('UNDERWATER', (screen_width / 2, screen_height / 7), 110, self.display_surface, GREEN)
        self.text_under = Text('ADVENTURE', (screen_width / 2, screen_height / 3.5), 110, self.display_surface, GREEN)

        # Loading and playing music
        pygame.mixer.music.load(menu_music)
        pygame.mixer.music.play(-1)

    # Handling background movement and drawing
    def update_background(self):
        self.display_surface.blit(self.background, (0,0))
        self.display_surface.blit(self.midground, (self.midground_x, 0))
        self.display_surface.blit(self.midground, (self.midground_x + screen_width, 0))  # Additional display for image boundary coverage
        # Updating background position for horizontal movement
        self.midground_x -= self.midground_speed
        if self.midground_x <= -screen_width:
            self.midground_x = 0
    
    def quit(self):
        pygame.quit()
        sys.exit()

    # Handling button image change when hovered over with the mouse
    def update_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.rect.collidepoint(mouse_pos):
            self.display_surface.blit(pygame.transform.scale(pygame.image.load(play_button_active_image).convert_alpha(), self.play_button.size), self.play_button.rect) 
        else: 
            self.display_surface.blit(self.play_button.image, self.play_button.rect)  # Change image to inactive

        if self.exit_button.rect.collidepoint(mouse_pos):
            self.display_surface.blit(pygame.transform.scale(pygame.image.load(exit_button_active_image).convert_alpha(), self.play_button.size), self.exit_button.rect) 
        else: 
            self.display_surface.blit(self.exit_button.image, self.exit_button.rect)  # Change image to inactive
    
    # Handling external events
    def check_input(self):
        pressed_mousebuttons = pygame.mouse.get_pressed()  # Get pressed mouse buttons
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position
        if pressed_mousebuttons[0]:  # If left mouse button is pressed
            if self.play_button.rect.collidepoint(mouse_pos):
                self.create_overworld(0, 0) 
            elif self.exit_button.rect.collidepoint(mouse_pos):
                self.quit()

    # Starting the main loop
    def run(self):
        self.update_background()
        self.update_buttons()
        self.check_input()
        self.text_above.update_text()
        self.text_under.update_text()
