import pygame

# This file contains global settings for the game, including colors, audio settings, and player configurations.

# Settings;
audio_on = False  
dark_background = True 
volume = 1.0

# Screen Settings.
WIDTH = 0
HEIGHT = 0

# Useful colors.
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
light_gray = (200, 200, 200)
orange = (255, 165, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Ship Limit.
ship_limit = 250

# Ship Price.
ship_price = 200

# Dark Mode Colors.
dark_mode_bg = (80, 80, 80)
dark_mode_details = (255, 255, 255)

# Light Mode Colors.
light_mode_bg = (230, 230, 230)
light_mode_details = (0, 0, 0)


# Player Colors.
neutral_color = dark_mode_details if dark_background else light_mode_details
player_colors = (neutral_color, (255, 165, 0), (0, 0, 255))
def reload_player_colors():
    global neutral_color
    global player_colors
    
    neutral_color = dark_mode_details if dark_background else light_mode_details
    player_colors = (neutral_color, (255, 165, 0), (0, 0, 255))

# Updates Audio.
def update_audio():
    if audio_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
