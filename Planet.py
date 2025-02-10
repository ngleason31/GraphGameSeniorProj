import pygame

class Planet:
    def __init__(self, x, y, radius=60, color=(50, 50, 50)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)