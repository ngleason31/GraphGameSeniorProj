import pygame
import GlobalSettings

class Planet:
    def __init__(self, x, y, radius=60, player=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = GlobalSettings.player_colors[player]
        self.player_num = player
        
    def change_player(self, player_num):
        self.player_num = player_num
        self.color = GlobalSettings.player_colors[player_num]
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, width=6)