audio_on = True          
dark_background = True 



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
