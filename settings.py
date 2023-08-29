import pygame 
import os
try:
    import tkinter as tk
except:
    os.system(f"pip install tkinter")
    import tkinter as tk

def get_screen_resolution():
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

# General settings
tile_size = 64
music_volume = 1
screen_width, screen_height = get_screen_resolution()
FPS = 60
player_sprint_cooldown_time = 300
pixel_font = 'graphics\\ui\\font.ttf'

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (100,100,100)
DARK_GREEN = (13, 26, 32)
DARK_BLUE = (2, 3, 28)
RED = (237, 2, 2)
GOLD = (209, 177, 0)
GREEN = (192, 240, 165)

'-----------------------------------------------IMAGES-----------------------------------------------'
# Buttons
play_button_non_active_image = 'graphics\\main_menu\\button\\non_active\\start_btn.png'
exit_button_non_active_image = 'graphics\\main_menu\\button\\non_active\\exit_btn.png'
play_button_active_image = 'graphics\\main_menu\\button\\active\\start_btn.png'
exit_button_active_image = 'graphics\\main_menu\\button\\active\\exit_btn.png'

# Static objects
terrain_tile_image = 'graphics\\terrain\\terain_tile.png'
plant_1_image = 'graphics\\decorations\\static_decorations\\6.png'
plant_2_image = 'graphics\\decorations\\static_decorations\\7.png'
decorations_image_0 = 'graphics\\decorations\\static_decorations\\1.png'
decorations_image_1 = 'graphics\\decorations\\static_decorations\\2.png'
decorations_image_2 = 'graphics\\decorations\\static_decorations\\3.png'
decorations_image_3 = 'graphics\\decorations\\static_decorations\\4.png'
decorations_image_4 = 'graphics\\decorations\\static_decorations\\5.png'
submarine_image = 'graphics\\character\\submarine.png'

# Animated objects
plant_3_images = 'graphics\\decorations\\plant_3'
gold_coin_images = 'graphics\\coins\\gold'
silver_coin_images = 'graphics\\coins\\silver'
dart_fish_images = 'graphics\\decorations\\decoration_fishes\\dart_fish'
def_fish_images = 'graphics\\decorations\\decoration_fishes\\def_fish'
jelly_fish_images = 'graphics\\decorations\\decoration_fishes\\jelly_fish'

# Enemy
enemy_run_images = 'graphics\\enemies\\big_fish'
enemy_explosion_images = 'graphics\\enemies\\explosions\\enemy'

# Player
player_images_path = 'graphics\\character'

# UI and main menu
ui_health_bar_image = 'graphics\\ui\\health_bar.png'
ui_coin_image = 'graphics\\ui\\coin.png'
pause_image = 'graphics\\ui\\pause.png'
screen_icon_image = 'graphics\\ui\\screen_icon.png'
overworld_icon_image = 'graphics\\overworld\\submarine.png'
loading_image = 'graphics\\ui\\loading.png'

# Background
background_image = 'graphics\\background\\background.png'
midground_image = 'graphics\\background\\midground.png'

'-----------------------------------------------AUDIO-----------------------------------------------'
# Music
menu_music = 'audio\\music\\Watery-Cave.ogg'
overworld_music = 'audio\\music\\23_loop.ogg'
# Sound effects
coin_sound = 'audio\\sounds\\coin.ogg'
damage_sound = 'audio\\sounds\\damage.ogg'
death_sound = 'audio\\sounds\\death.ogg'
enemy_death_sound = 'audio\\sounds\\enemy_death.ogg'
sprint_sound = 'audio\\sounds\\sprint.ogg'
win_sound = 'audio\\sounds\\win.ogg'
