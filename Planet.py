import pygame
import math
import GlobalSettings
import random

class Planet:
    def __init__(self, id, x, y, radius=60, player=0, health=1200):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.ship_attacking = False
        self.color = GlobalSettings.player_colors[player]
        self.player_num = player
        self.connections = []
        self.point_value = radius // 5
        self.max_health = health
        self.health = health
        self.selected = False
        
    def change_player(self, player_num):
        self.player_num = player_num
        self.color = GlobalSettings.player_colors[player_num]
        
    def change_health(self, health):
        self.health += health
        
        if self.health > self.max_health:
            self.health = self.max_health
        
    def draw(self, screen, planets):
        #Show if it is selected or not
        if self.selected:
            pygame.draw.circle(screen, GlobalSettings.green, (int(self.x), int(self.y)), self.radius + 3, width=6)
        #Drawing the planet itself
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, width=4)
        # Draw the point value on the planet
        font = pygame.font.Font(None, 18)
        text = font.render(str(self.point_value), True, GlobalSettings.neutral_color)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        
        #Drawing the healthbar for the planet
        if self.health != self.max_health:
            self.draw_health_bar(screen)
            
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
            pygame.draw.line(screen, GlobalSettings.neutral_color, (x_1, y_1), (x_2, y_2), 3)
            
    def add_connection(self, id):
        self.connections.append(id)
        
    def draw_health_bar(self, screen):
        #Draws a small health bar above the ship.
        bar_width = 50
        bar_height = 10
        offset_y = -15  

        # position the bar above the ship
        bar_x = self.x - bar_width // 2
        bar_y = self.y - offset_y

        # outline
        pygame.draw.rect(screen, GlobalSettings.neutral_color, (bar_x, bar_y, bar_width, bar_height), 1)
        # fill
        fill_width = (self.health / self.max_health) * (bar_width - 2)
        pygame.draw.rect(screen, GlobalSettings.red, (bar_x+1, bar_y+1, fill_width, bar_height-2))
        
    def serialize(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "radius": self.radius,
            "ship_attacking": self.ship_attacking,
            "color": self.color,
            "player_num": self.player_num,
            "connections": self.connections,
            "point_value": self.point_value,
            "max_health": self.max_health,
            "health": self.health,
        }

    @staticmethod
    def deserialize(data):
        p = Planet(data["id"], data["x"], data["y"], data["radius"], data["player_num"], data["max_health"])
        p.ship_attacking = data["ship_attacking"]
        p.color = data["color"]
        p.connections = data["connections"]
        p.point_value = data["point_value"]
        p.health = data["health"]
        return p
            
def planet_generator():
    #Start with a top left, center, and bottom left planet
    player_planet = Planet(0, 150, 150, 30, GlobalSettings.curr_player, health=10000)
    opposing_planet = Planet(1, GlobalSettings.WIDTH - 150, GlobalSettings.HEIGHT - 150, 30, GlobalSettings.opposing_player, health=10000)
    
    planets = [player_planet, opposing_planet]
    num_planets = random.randint(80, 90) + 2
    
    #Generates planets that are at least close to another planet, but far enough from all planets not to overlap
    for id in range(num_planets - 2):
        radius = random.randint(15, 30)
        attempts = 0
        planet_found = False
        while not planet_found and attempts < 1000:
            attempts += 1
            x = random.randint(150, GlobalSettings.WIDTH - 150)
            y = random.randint(150, GlobalSettings.HEIGHT - 150)
            for planet in planets:
                planet_distance = math.sqrt((planet.x - x) ** 2 + (planet.y - y) ** 2)
                if planet_distance <= 110:
                    planet_found = True
                if planet_distance <= 80:
                    planet_found = False
                    break
            if planet_found:
                planets.append(Planet(id + 2, x, y, radius))
    
    #Creates connections between planets
    num_actual_planets = len(planets)
    for first_planet_id in range(num_actual_planets):
        for second_planet_id in range(first_planet_id + 1, num_actual_planets):
            first_planet = planets[first_planet_id]
            second_planet = planets[second_planet_id]
            distance = math.sqrt((first_planet.x - second_planet.x) ** 2 + (first_planet.y - second_planet.y) ** 2)
            if distance <= 130:
                first_planet.add_connection(second_planet_id)
                second_planet.add_connection(first_planet_id)
                
                
    
    #Makes sure the entire graph is connected
    if not planet_BFS(player_planet, opposing_planet, planets):
        #Regenerates if not connected
        return planet_generator()
        
    return planets


#Helper planet BFS function
# def planet_BFS(start, goal, planets):
#     stack = [start]
#     visited = []
    
#     while stack:
#         planet = stack.pop(0)
#         visited.append(planet.id)
#         for connection in planet.connections:
#             if planet == goal:
#                 return True
#             if connection not in visited:
#                 stack.append(planets[connection])
                
#     return False

def planet_BFS(start, goal, planets):
    queue = [start]
    visited = set()
    while queue:
        current = queue.pop(0)
        if current == goal:
            return True
        visited.add(current.id)
        for connection in current.connections:
            neighbor = planets[connection]
            if neighbor.id not in visited:
                queue.append(neighbor)
    return False

#Function to check if a certain x, y is in a planet (square hitbox for simplicity)
def planet_loc(x, y, planets):
    for planet in planets:
        if (x <= planet.x + planet.radius and x >= planet.x - planet.radius
        and y <= planet.y + planet.radius and y >= planet.y - planet.radius):
            return planet
    
    return None
        
    
