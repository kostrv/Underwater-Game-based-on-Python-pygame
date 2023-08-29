import pygame, sys
from game_data import levels
from support import import_folder
from settings import *

class Node(pygame.sprite.Sprite):
    # Level Node
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()
        self.frames = import_folder(path)  # Import animation images
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)  # Common boundaries
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)  # Central zone boundaries

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            # If the level is unavailable, the image will be tinted black
            tint_surface = self.image.copy()
            tint_surface.fill(BLACK, None, pygame.BLEND_RGBA_MULT)   
            self.image.blit(tint_surface, (0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos 
        self.image = pygame.image.load(overworld_icon_image).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
    
    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        # General setup
        self.display_surface = surface
        self.midground = pygame.transform.flip(pygame.transform.scale(pygame.image.load(midground_image).convert_alpha(), (screen_width, screen_height)), True,False,)
        self.background = pygame.transform.flip(pygame.transform.scale(pygame.image.load(background_image).convert(), (screen_width, screen_height)), True,False,)
        self.midground_speed = 1
        self.midground_x = 0

        # Level attributes
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # Movement attributes
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        # Create objects
        self.setup_nodes()
        self.setup_icon()

        # Timer attributes
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

        self.level_loading = False
        
    def setup_nodes(self):
        # Create level nodes
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            # Apply images based on status
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(node_sprite)
    
    def draw_paths(self):
        # Draw paths
        if self.max_level > 0:
            points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]  # Create points for movement
            pygame.draw.lines(self.display_surface, DARK_GREEN, False, points, 6)

    def setup_icon(self):
        # Create icon
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
    
    def input(self):
        # Handle external events
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')  
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE] or keys[pygame.K_e]:
                self.level_loading = True
                self.create_level(self.current_level)
                
            if keys[pygame.K_TAB]:
                pygame.quit()
                sys.exit()

    def get_movement_data(self, target):
        # Handle icon movement
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next': 
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()
    
    def update_background(self):
        self.display_surface.blit(self.background, (0,0))
        self.display_surface.blit(self.midground, (self.midground_x, 0))
        self.display_surface.blit(self.midground, (self.midground_x + screen_width, 0))  # Additional display for image boundary coverage
        # Update background position for horizontal movement
        self.midground_x -= self.midground_speed
        if self.midground_x <= -screen_width:
            self.midground_x = 0

    def update_icon_pos(self):  
        # Update icon position
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def input_timer(self):
        # Input delay timer
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True
    
    # Start
    def run(self):
        self.input_timer()
        self.update_background()
        self.input()
        self.icon.update()
        self.nodes.update()
        self.update_icon_pos()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)     
        if self.level_loading:
            loading_img = pygame.image.load(loading_image)
            self.display_surface.blit(loading_img, (screen_width/2-(loading_img.get_rect().width/2),screen_height/2.5-(pygame.image.load(pause_image).get_rect().height/2))) # Display loading
