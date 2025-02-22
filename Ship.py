import pygame
import sys
import math
import GlobalSettings


class Ship:
    def __init__(self, x, y, player=0, size=10, speed=5):
        self.x = x
        self.y = y
        self.pos = pygame.Vector2(x, y)
        self.player = player
        self.size = size
        self.speed = speed
        self.curr_target = self.pos
        
    def draw(self, screen):
        triangle_points = [(self.x, self.y - self.size), (self.x - self.size, self.y + self.size), (self.x + self.size, self.y + self.size)]
        pygame.draw.polygon(screen, GlobalSettings.player_colors[self.player], triangle_points, width=6)
    
    def get_position(self):
        return (self.x, self.y)
        
    def set_target(self, x, y):
        self.curr_target = pygame.Vector2(x, y)
    
    def update_position(self):
        if self.pos != self.curr_target:
            direction = (self.curr_target - self.pos).normalize()
            distance = (self.curr_target - self.pos).length()

            if distance > self.speed:
                self.pos += direction * self.speed
            else:
                self.pos = self.curr_target
        
        self.x = self.pos[0]
        self.y = self.pos[1]