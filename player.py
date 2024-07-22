import pygame
from settings import *
from support import import_folder
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, change_health):
        super().__init__()
        # General setup
        self.import_character_assets()  # Import player animation
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]  # Current player image
        self.rect = self.image.get_rect(topleft=pos)
        self.display_surface = surface

        # Player movement control variables
        self.direction = pygame.math.Vector2(0, 0)  # Player movement direction vector
        self.speed_x = 5
        self.speed_y = 5
        self.base_speed = self.speed_x  # Player base speed (used during sprint)
        self.sprinting_timer = 0
        self.initial_sprint_timer = 0  # Sprint initialization timer
        self.sprint_cooldown_timer = 0  # Sprint cooldown timer
        self.sprint_active = False  # Sprint activation flag
        self.rush_animation_played = False  # Flag indicating if rush animation has been played

        # Player state variables
        self.player_status = 'idle'  # Current player state
        self.racing_right = True  # Player movement direction flag (True - right, False - left)
        self.on_ground = False  # Ground collision flag
        self.on_ceiling = False  # Ceiling collision flag
        self.on_left = False  # Left wall collision flag
        self.on_right = False  # Right wall collision flag
        self.took_damage = False
        self.prev_space_state = False  # "Space" key release flag
        
        # Health control
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 800
        self.hurt_time = 0

        # Sound effects
        self.sprint_sound = pygame.mixer.Sound(sprint_sound)
        self.sprint_sound.set_volume(0.5)
        self.damage_sound = pygame.mixer.Sound(damage_sound)
        self.damage_sound.set_volume(0.7)

        # Timer attributes
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 5000

    # Import animation assets
    def import_character_assets(self):
        character_path = 'graphics\\character'  # Path to player animation folder
        self.animations = {'idle': [], 'default_swimming': [], 'fast_swimming': [], 'hurt': [], 'rush_for_bonus_start': []}  # Animation flags (corresponding to player state names)
        for animation in self.animations.keys(): 
            full_path = character_path + '\\' + animation  # Get path
            self.animations[animation] = import_folder(full_path)  # Load animation from corresponding folder

    def animate(self):
        animation = self.animations[self.status]  # Choose current animation based on player state
        self.frame_index += self.animation_speed 

        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)].convert_alpha()
        if self.racing_right:
            self.image = image  # If player is moving right, use current frame
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image  # If player is moving left, flip the frame horizontally

        # Set player position based on its state and relative position to level objects for proper collision handling of the current image model
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
     
    # Sprint
    def sprint(self):
        # Handle sprint cooldown timer
        if self.sprint_cooldown_timer > 0:
            self.sprint_cooldown_timer -= 1
        # Apply sprint effects for a set duration
        if self.sprinting_timer > 0:
            self.sprinting_timer -= 1
            self.speed_x = self.base_speed * 2
            if self.racing_right:
                self.direction.x = 1
            else:
                self.direction.x = -1
        else:  # Reset flags to default values
            self.speed_x = self.base_speed
            self.sprint_active = False
            self.sprint_cooldown_timer = player_sprint_cooldown_time

    # Handle input events
    def get_input(self):
        if self.allow_input:
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not self.invincible:
                self.direction.x = min(1, self.direction.x + 0.1)  # Move right
                self.racing_right = True
            elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not self.invincible:
                self.direction.x = max(-1, self.direction.x - 0.1)  # Move left
                self.racing_right = False
            else:
                # Stop with inertia
                if self.direction.x > 0:
                    self.direction.x = max(0, self.direction.x - 0.03)
                if self.direction.x < 0:
                    self.direction.x = min(0, self.direction.x + 0.03)
            
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and not self.invincible:  # Move up
                self.direction.y = -1
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not self.invincible:  # Move down
                self.direction.y = 1
            else:
                # Stop with inertia
                if self.direction.y < 0:
                    self.direction.y = min(0, self.direction.y + 0.03)
                if self.direction.y > 0:
                    self.direction.y = max(0, self.direction.y - 0.03)
            
            if keys[pygame.K_SPACE] and not self.invincible:
                if not self.prev_space_state and not self.sprint_active:
                    self.sprint_sound.play()
                    self.space_released = False  # Prevent sprint activation until the next "space" key release
                    self.sprint_active = True
                    self.initial_sprint_timer = 20
                    self.sprinting_timer = 2 * FPS
                    self.rush_animation_played = False
            self.prev_space_state = keys[pygame.K_SPACE]

    # Handling status
    def get_status(self):
        if self.took_damage:
            self.status = 'hurt'
        elif self.direction.y < 0 and self.direction.x == 0:
            self.status = 'idle'
        elif self.direction.y > 1 or self.direction.x == 0:
            self.status = 'idle'
        else:
            if self.initial_sprint_timer > 0:
                self.status = 'rush_for_bonus_start'
                self.initial_sprint_timer -= 1
                if not self.rush_animation_played:
                    self.rush_animation_played = True
            elif self.initial_sprint_timer <= 0 and self.sprint_active:
                self.status = 'fast_swimming'
            else:
                self.status = 'default_swimming'
    
    # Handling damage reception
    def get_damage(self, damage_val):
        if not self.invincible:
            self.damage_sound.play()
            self.direction.x, self.direction.y = 0, 0
            self.took_damage = True
            self.change_health(damage_val)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
    
    def if_death(self):  
        self.death_animation_end = True
    
    # Invincibility timer
    def invincibility_timer(self):       
        if self.invincible:
            current_time = pygame.time.get_ticks()
            self.direction.x, self.direction.y = 0, 0
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False 
                self.took_damage = False

    def input_timer(self):
        # Input delay timer
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    # Execution
    def update(self):
        self.input_timer()
        self.get_input()
        self.get_status()
        self.animate()
        self.sprint()
        self.invincibility_timer()
        self.if_death()