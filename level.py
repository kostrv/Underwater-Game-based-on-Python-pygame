import pygame, sys
from support import import_csv_layout, import_cut_graphics, import_folder
from settings import *
from tiles import Tile, StaticTile, Coin, Decoration, AnimatedTile, AnimatedPlant, Plant, Submarine
from enemy import Enemy, DecorationFish
from player import Player
from game_data import levels 
pygame.init()

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width 
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)  # Applying object's position with respect to camera's position

    def update(self, target, level_width, level_height):
        # Calculate coordinates for centering the camera on the target
        x = -target.x + int(screen_width / 2)
        y = -target.y + int(screen_height / 2) 

        # Restrict camera movement within level boundaries
        x = min(0, x)  # Left edge
        x = max(-level_width + screen_width, x)  # Right edge 
        y = max(-level_height + screen_height, y)  # Bottom edge 
        y = min(0, y)  # Top edge 

        self.camera = pygame.Rect(x, y, self.width, self.height)  # Update camera's position and size

class Level:
    def __init__(self,current_level,surface,create_overworld, change_coins, change_health, check_game_over):
        # General setup
        self.display_surface = surface 
        self.paused = False 
        self.prev_escape_state = False
        self.level_width = 0  
        self.level_height = 0  
        self.camera = Camera(self.level_width, self.level_height)  
        self.midground = pygame.transform.scale(pygame.image.load(midground_image).convert_alpha(), (screen_width, screen_height))
        self.background = pygame.transform.scale(pygame.image.load(background_image).convert(), (screen_width, screen_height))

        # Connect to level menu
        self.create_overworld = create_overworld
        self.current_level = current_level
        self.check_game_over = check_game_over
        self.level_data = levels[self.current_level]
        self.new_max_level = self.level_data['unlock']

        # Load and set up objects based on level_data
        player_layout = import_csv_layout(self.level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # UI
        self.change_coins = change_coins

        # Sound effects
        self.coin_sound = pygame.mixer.Sound(coin_sound)
        self.coin_sound.set_volume(0.2)
        self.enemy_death_sound = pygame.mixer.Sound(enemy_death_sound)
        self.enemy_death_sound.set_volume(0.1)
        self.win_sound = pygame.mixer.Sound(win_sound)
        self.win_sound.set_volume(0.1)
        
        self.generation_done = False
        self.status = 'load'

    def generate_level(self):
        # Load and set up objects based on level_data
        # Terrain
        if not self.generation_done:
            terrain_layout = import_csv_layout(self.level_data['terrain'])
            self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
            # Coins
            coins_layout = import_csv_layout(self.level_data['coins'])
            self.coins_sprites = self.create_tile_group(coins_layout, 'coins')
            # Enemies
            enemy_layout = import_csv_layout(self.level_data['enemies'])
            self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')
            # Constraints
            constraint_layout = import_csv_layout(self.level_data['constrains'])
            self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')
            # Decoration fish
            decoration_fishes_layout = import_csv_layout(self.level_data['decoration_fishes'])
            self.decoration_fishes_sprites = self.create_tile_group(decoration_fishes_layout, 'decoration_fish')
            # Decorations
            decoration_layout = import_csv_layout(self.level_data['decorations'])
            self.decoration_sprites = self.create_tile_group(decoration_layout, 'decoration')
            # Plants
            plants_layout = import_csv_layout(self.level_data['plants'])
            self.plant_sprites = self.create_tile_group(plants_layout, 'plant')
            # Decoration fish movement constraints
            decoration_fishes_constrains_layout = import_csv_layout(self.level_data['decoration_fishes_constrains'])
            self.decoration_fishes_constrains_sprites = self.create_tile_group(decoration_fishes_constrains_layout, 'decoration_fishes_constrain')
            pygame.mixer.music.stop()
            pygame.mixer.music.load(levels[self.current_level]['soundtrack'])
            pygame.mixer.music.play(-1)

            self.generation_done = True
            self.status = 'game'

    # Create level tiles
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        max_x = 0
        max_y = 0
        for row_index, row in enumerate(layout): # Processing data from the csv layer
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
                    # Creating different types of tiles based on the 'type' parameter
                    if type == 'terrain': # Terrain
                        terrain_tile_list = import_cut_graphics(terrain_tile_image)
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'coins': # Coins
                        if val == '0': sprite = Coin(tile_size, x, y, gold_coin_images, 5)
                        if val == '1': sprite = Coin(tile_size, x, y, silver_coin_images, 1)
                    if type == 'enemy': # Enemies
                        sprite = Enemy(tile_size, x, y, enemy_run_images)
                    if type == 'decoration_fish': # Decoration fish
                        if val == '0': sprite = DecorationFish(tile_size, x, y, dart_fish_images, 2, 3)
                        if val == '1': sprite = DecorationFish(tile_size, x, y, def_fish_images, 1, 1)
                        if val == '2': sprite = DecorationFish(tile_size, x, y, jelly_fish_images, 1, 1)
                    if type == 'constraint': # Constraints for enemy movement
                        sprite = Tile(tile_size, x, y)
                    if type == 'decoration_fishes_constrain': # Constraints for decoration fish movement
                        sprite = Tile(tile_size, x, y)
                    if type == 'decoration': # Decorations
                        if val == '0': sprite = Decoration(x, y, decorations_image_0)
                        if val == '1': sprite = Decoration(x, y, decorations_image_1)
                        if val == '2': sprite = Decoration(x, y, decorations_image_2)
                        if val == '3': sprite = Decoration(x, y, decorations_image_3)
                        if val == '4': sprite = Decoration(x, y, decorations_image_4)
                    if type == 'plant': # Plants
                        if val == '0': sprite = Plant(tile_size, x, y, plant_1_image, 1.3)
                        if val == '1': sprite = Plant(tile_size, x, y, plant_2_image, 1.4)
                        if val == '2': sprite = AnimatedPlant(tile_size, x, y, plant_3_images, 1.6)
                    sprite_group.add(sprite)
        self.level_width = max_x + tile_size  # Updating the total level width
        self.level_height = max_y + tile_size  # Updating the total level height
        return sprite_group

    # Creating player objects
    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout): # Processing data from the csv layer
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                # Player
                if val == '0': 
                    sprite = Player((x, y), self.display_surface, change_health)
                    self.player.add(sprite)
                # Submarine
                if val == '1':
                    submarine_surface = pygame.image.load(submarine_image).convert_alpha()
                    sprite = Submarine(tile_size, x, y, submarine_surface)
                    self.goal.add(sprite)

    # Changing enemy direction upon collision with constraints
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    # Changing decoration fish direction upon collision with constraints
    def decoration_fishes_collsion_reverse(self):
        for fish in self.decoration_fishes_sprites.sprites():
            if pygame.sprite.spritecollide(fish, self.decoration_fishes_constrains_sprites, False):
                fish.reverse()

    # Handling horizontal collisions
    def horizontal_movement_colision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed_x # Applying speed for horizontal movement
        colideble_sprites = self.terrain_sprites.sprites() # Sprites to collide with
        for sprite in colideble_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: # Moving left
                    player.rect.left = sprite.rect.right # Colliding with the right edge of the object
                    self.on_left = True
                elif player.direction.x > 0: # Moving right
                    player.rect.right = sprite.rect.left # Colliding with the left edge of the object
                    self.on_right = True

        # Conditions for collision on the right or left side to handle the correct collisions with the current image model
        if player.on_left and player.direction.x >= 0:
            player.on_left = False
        if player.on_right and player.direction.x <= 0:
            player.on_right = False

    # Handling vertical collisions
    def vertical_movement_colision(self):
        player = self.player.sprite
        player.rect.y += player.direction.y * player.speed_y # Applying speed for vertical movement
        colideble_sprites = self.terrain_sprites.sprites() # Sprites with which collision should occur
        for sprite in colideble_sprites: 
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: # If moving downward
                    player.rect.bottom = sprite.rect.top # Colliding with the upper boundary of the object
                    player.direction.y = 0 
                    player.on_ground = True
                elif player.direction.y < 0: # If moving upward
                    player.rect.top = sprite.rect.bottom # Colliding with the lower boundary of the object
                    player.direction.y = 0
                    player.on_ceiling = True
        
        # Conditions for collision on the upper or lower part to handle the correct collisions with the current image model
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    # Checking for victory
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.win_sound.play()
            self.create_overworld(self.current_level, self.new_max_level) # Creating level menu

    # Checking collisions with coins
    def check_coin_collisions(self): 
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value) # Calling function from main.py

    # Checking player collisions with enemies
    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False) 
        if enemy_collisions:
            for enemy in enemy_collisions:
                if not enemy.is_explodes:
                    enemy_left = enemy.rect.left
                    enemy_right = enemy.rect.right
                    player_left = self.player.sprite.rect.left
                    player_right = self.player.sprite.rect.right
                    if self.player.sprite.status == 'fast_swimming': # Destruction only occurs when sprint is active
                        if (self.player.sprite.direction.x == 1 and player_right > enemy_left) or (self.player.sprite.direction.x == -1 and player_left < enemy_right):
                            enemy_collisions.remove(enemy)
                            self.enemy_death_sound.play()
                            if not enemy.player_collide:
                                enemy.frame_index = 0
                                enemy.player_collide = True
                            enemy.is_explodes = True
                    else:
                        if not self.player.sprite.took_damage:
                            self.player.sprite.get_damage(-20)

    # Handling background movement and rendering
    def update_background(self):
        # Calculate horizontal offset based on camera position along the x-axis
        self.display_surface.blit(self.background, (0,0))
        x_offset = self.camera.camera.x // 2  # Adjust value to set desired scroll speed

        # Calculate new position for midground image, making it loop
        self.midground_x = x_offset % self.midground.get_width()

        # Place midground image multiple times to create continuous scrolling effect
        for i in range(-1, screen_width // self.midground.get_width() + 2):
            self.display_surface.blit(self.midground, (self.midground_x + i * self.midground.get_width(), 0))

    # Starting the game
    def run(self):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and not self.prev_escape_state:
            self.paused = not self.paused
        self.prev_escape_state = keys[pygame.K_ESCAPE]

        if keys[pygame.K_TAB]:
            pygame.quit()
            sys.exit()
            
        if self.status == 'load':
            self.generate_level()
        elif not self.paused and self.status == 'game':
            self.camera.update(self.player.sprite.rect, self.level_width, self.level_height)
            self.update_background()
            # Render all sprites using camera coordinates
            all_sprites = (self.decoration_sprites.sprites() + self.plant_sprites.sprites() + self.terrain_sprites.sprites() + self.coins_sprites.sprites() 
            + self.enemy_sprites.sprites() + self.enemy_sprites.sprites() + self.goal.sprites() + self.decoration_fishes_sprites.sprites())
            for sprite in all_sprites:
                self.display_surface.blit(sprite.image, self.camera.apply(sprite))

            # Activate sprite methods
            # Enemies
            self.enemy_sprites.update() 
            self.enemy_collision_reverse()
            # Decoration fish
            self.decoration_fishes_sprites.update()
            self.decoration_fishes_collsion_reverse()
            # Coins
            self.coins_sprites.update()
            # Plants
            self.plant_sprites.update()
            # Player
            self.player.update() 
            self.horizontal_movement_colision()
            self.vertical_movement_colision()
            self.display_surface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite))

            # Check game events
            self.check_coin_collisions()
            self.check_enemy_collisions()
            self.check_win()
            self.check_game_over(self.current_level)
        else:
            self.display_surface.blit(pygame.image.load(pause_image), (screen_width/2-(pygame.image.load(pause_image).get_rect().width/2),screen_height/2-(pygame.image.load(pause_image).get_rect().height/2))) # Display pause

    
        
    
