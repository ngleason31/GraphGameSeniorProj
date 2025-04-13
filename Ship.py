import pygame
import GlobalSettings
import random


class Ship:
    def __init__(self, x, y, curr_planet, player=0, size=5, speed=5):
        self.x = x
        self.y = y
        self.pos = pygame.Vector2(x, y)
        self.player = player
        self.size = size
        self.speed = speed
        self.curr_planet = curr_planet
        self.next_planet = curr_planet
        self.curr_target = self.pos
        self.max_health = 20
        self.health = 20
        self.landed = True

        
    def draw(self, screen):
        triangle_points = [(self.x, self.y - self.size), (self.x - self.size, self.y + self.size), (self.x + self.size, self.y + self.size)]
        pygame.draw.polygon(screen, GlobalSettings.player_colors[self.player], triangle_points, width=3)

        #if self.health != self.max_health:
            #self.draw_health_bar(screen)
    
    def get_position(self):
        return (self.x, self.y)
        
    def set_target(self, planet):
        self.next_planet = planet.id
        x_offset = random.randint(-planet.radius + 15, planet.radius - 15)
        y_offset = random.randint(-planet.radius + 15, planet.radius - 15)
        x = planet.x + x_offset
        y = planet.y + y_offset
        self.curr_target = pygame.Vector2(x, y)
        self.landed = False

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

        if self.pos == self.curr_target:
            self.landed = True
            self.curr_planet = self.next_planet
        
    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "player": self.player,
            "size": self.size,
            "speed": self.speed,
            "curr_planet": self.curr_planet,
            "next_planet": self.next_planet,
            "curr_target": self.curr_target,
            "max_health": self.max_health,
            "health": self.health,
            "landed": self.landed,
        }

    @staticmethod
    def deserialize(data):
        s = Ship(data["x"], data["y"], data["curr_planet"], data["player"], data["size"], data["speed"])
        s.next_planet = data["next_planet"]
        s.curr_target = data["curr_target"]
        s.health = data["health"]
        s.landed = data["landed"]
        return s