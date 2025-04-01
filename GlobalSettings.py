import pygame

#Global Variables
audio_on = False    
dark_background = True 

WIDTH = 0
HEIGHT = 0

#Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
light_gray = (200, 200, 200)
orange = (255, 165, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

computer1_difficulty = 'Medium'
computer2_difficulty = 'Medium'

shipcounts = [0, 0]

curr_player = 0
opposing_player = 0

#Dark Mode Colors
dark_mode_bg = (80, 80, 80)
dark_mode_details = (255, 255, 255)

#Light Mode Colors
light_mode_bg = (230, 230, 230)
light_mode_details = (0, 0, 0)


#Player Colors
neutral_color = dark_mode_details if dark_background else light_mode_details
player_colors = (neutral_color, (255, 165, 0), (0, 0, 255))
def reload_player_colors():
    global neutral_color
    global player_colors
    
    neutral_color = dark_mode_details if dark_background else light_mode_details
    player_colors = (neutral_color, (255, 165, 0), (0, 0, 255))

#Update Audio
def update_audio():
    if audio_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
