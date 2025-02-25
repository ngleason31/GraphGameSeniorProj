import pygame
import math
import GlobalSettings
import random

class Planet:
    def __init__(self, id, x, y, radius=60, player=0):
        self.id = id
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
        
def planet_generator():
    player_planet = Planet(0, 200, 200, 80, GlobalSettings.curr_player)
    opposing_planet = Planet(1, GlobalSettings.WIDTH - 200, GlobalSettings.HEIGHT - 200, 80, GlobalSettings.opposing_player)
    center_planet = Planet(2, GlobalSettings.WIDTH // 2, GlobalSettings.HEIGHT // 2, 80)
    
    planets = [player_planet, opposing_planet, center_planet]
    num_planets = random.randint(4, 8)
    
    for id in range(num_planets):
        radius = random.randint(30, 80)
        planet_found = False
        while not planet_found:
            x = random.randint(200, GlobalSettings.WIDTH - 200)
            y = random.randint(200, GlobalSettings.HEIGHT - 200)
            for planet in planets:
                planet_distance = math.sqrt((planet.x - x) ** 2 + (planet.y - y) ** 2)
                if planet_distance <= 400:
                    planet_found = True
                if planet_distance <= 180:
                    planet_found = False
                    break
            if planet_found:
                planets.append(Planet(id + 3, x, y, radius))
        
        
    return planets