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
        # Assign a random point value between 0 and 75 to the planet.
        self.point_value = random.randint(1, 75)
        
    def change_player(self, player_num):
        self.player_num = player_num
        self.color = GlobalSettings.player_colors[player_num]
        
    def draw(self, screen, planets):
        #Drawing the planet itself
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, width=6)
        # Draw the point value on the planet
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.point_value), True, GlobalSettings.neutral_color)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        for connection in self.connections:
            #Calculating start points on edge of circle
            connecting_planet = planets[connection]
            dx = self.x - connecting_planet.x
            dy = self.y - connecting_planet.y
            d = math.sqrt((self.x - connecting_planet.x) ** 2 + (self.y - connecting_planet.y) ** 2)
            x_1 = self.x - self.radius * (dx / d)
            y_1 = self.y - self.radius * (dy / d)
            x_2 = connecting_planet.x + connecting_planet.radius * (dx / d)
            y_2 = connecting_planet.y + connecting_planet.radius * (dy / d)
            
            #Drawing the line
            pygame.draw.line(screen, GlobalSettings.neutral_color, (x_1, y_1), (x_2, y_2), 4)
            
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
            
    for first_planet_id in range(num_planets):
        for second_planet_id in range(first_planet_id + 1, num_planets):
            first_planet = planets[first_planet_id]
            second_planet = planets[second_planet_id]
            distance = math.sqrt((first_planet.x - second_planet.x) ** 2 + (first_planet.y - second_planet.y) ** 2)
            if distance <= 400:
                first_planet.add_connection(second_planet_id)
                second_planet.add_connection(first_planet_id)
                
                
    #Checks if there are any connections for the center planet
    has_close_planet = False
    for id in range(3, num_planets):
        planet = planets[id]
        distance = math.sqrt((planet.x - center_planet.x) ** 2 + (planet.y - center_planet.y) ** 2)
        if distance <= 400:
            has_close_planet = True
            center_planet.add_connection(id)
            planets[id].add_connection(2)
        
    #If no close planets, adds a connection to both top left and bottom right planets
    if not has_close_planet:
        center_planet.add_connection(0)
        center_planet.add_connection(1)
        player_planet.add_connection(2)
        opposing_planet.add_connection(2)
    
    #Makes sure the entire graph is connected
    if not planet_BFS(player_planet, center_planet, planets):
        player_planet.add_connection(2)
        center_planet.add_connection(0)
        
    if not planet_BFS(opposing_planet, center_planet, planets):
        opposing_planet.add_connection(2)
        center_planet.add_connection(1)
        
    return planets


#Helper planet BFS function
def planet_BFS(start, goal, planets):
    stack = [start]
    visited = []
    
    while stack:
        planet = stack.pop(0)
        visited.append(planet.id)
        for connection in planet.connections:
            if planet == goal:
                return True
            if connection not in visited:
                stack.append(planets[connection])
                
    return False

#Function to check if a certain x, y is in a planet (square hitbox for simplicity)
def planet_loc(x, y, planets):
    for planet in planets:
        if (x <= planet.x + planet.radius and x >= planet.x - planet.radius
        and y <= planet.y + planet.radius and y >= planet.y - planet.radius):
            return planet
    
    return None
        
    
