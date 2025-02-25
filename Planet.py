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
        self.connections = []
        
    def change_player(self, player_num):
        self.player_num = player_num
        self.color = GlobalSettings.player_colors[player_num]
        
    def draw(self, screen, planets):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, width=6)
        for connection in self.connections:
            pygame.draw.line(screen, GlobalSettings.neutral_color, (self.x, self.y), (planets[connection].x, planets[connection].y), 6)
            
    def add_connection(self, id):
        self.connections.append(id)
        
def planet_generator():
    #Start with a top left, center, and bottom left planet
    player_planet = Planet(0, 200, 200, 80, GlobalSettings.curr_player)
    opposing_planet = Planet(1, GlobalSettings.WIDTH - 200, GlobalSettings.HEIGHT - 200, 80, GlobalSettings.opposing_player)
    center_planet = Planet(2, GlobalSettings.WIDTH // 2, GlobalSettings.HEIGHT // 2, 80)
    
    planets = [player_planet, opposing_planet, center_planet]
    num_planets = random.randint(4, 8) + 3
    
    #Generates planets that are at least close to another planet, but far enough from all planets not to overlap
    for id in range(num_planets - 3):
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
                
    #Checks if there are any connections for the top left planet
    has_close_planet = False
    for id in range(3, num_planets):
        planet = planets[id]
        distance = math.sqrt((planet.x - player_planet.x) ** 2 + (planet.y - player_planet.y) ** 2)
        if distance <= 400:
            has_close_planet = True
            player_planet.add_connection(id)
            planet.add_connection(0)
        
    #If no close planets, adds a connection to the center planet
    if not has_close_planet:
        player_planet.add_connection(2)
        center_planet.add_connection(0)
            
    #Checks if there are any connections for the bottom right planet
    has_close_planet = False
    for id in range(3, num_planets):
        planet = planets[id]
        distance = math.sqrt((planet.x - opposing_planet.x) ** 2 + (planet.y - opposing_planet.y) ** 2)
        if distance <= 400:
            has_close_planet = True
            opposing_planet.add_connection(id)
            planets[id].add_connection(1)
        
    #If no close planets, adds a connection to the center planet
    if not has_close_planet:
        opposing_planet.add_connection(2)
        center_planet.add_connection(1)
            
    #Checks if there are any connections for the center planet
    has_close_planet = False
    for id in range(3, num_planets):
        planet = planets[id]
        distance = math.sqrt((planet.x - center_planet.x) ** 2 + (planet.y - center_planet.y) ** 2)
        if distance <= 400:
            has_close_planet = True
            opposing_planet.add_connection(id)
            planets[id].add_connection(2)
        
    #If no close planets, adds a connection to both top left and bottom right planets
    if not has_close_planet:
        center_planet.add_connection(0)
        center_planet.add_connection(1)
        player_planet.add_connection(2)
        opposing_planet.add_connection(2)
            
    for first_planet_id in range(3, num_planets):
        for second_planet_id in range(first_planet_id, num_planets):
            first_planet = planets[first_planet_id]
            second_planet = planets[second_planet_id]
            distance = math.sqrt((first_planet.x - second_planet.x) ** 2 + (first_planet.y - second_planet.y) ** 2)
        if distance <= 400:
            first_planet.add_connection(second_planet_id)
            second_planet.add_connection(first_planet_id)
        
    return planets
