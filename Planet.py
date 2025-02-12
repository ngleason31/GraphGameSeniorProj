import pygame

class Planet:
    def __init__(self, x, y, radius=60, color=(80, 80, 80), background=(35, 35, 35)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.background = background
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, width=6)