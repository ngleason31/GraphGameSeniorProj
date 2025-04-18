import pygame
import GlobalSettings
import random


class Ship:
    def __init__(self, x, y, curr_planet, player=0, size=5, speed=5, health=20):
        '''
        Initializes the ship with the given parameters.
        '''
        self.x = x
        self.y = y
        self.pos = pygame.Vector2(x, y)
        self.player = player
        self.size = size
        self.speed = speed
        self.curr_planet = curr_planet
        self.next_planet = curr_planet
        self.curr_target = self.pos
        self.max_health = health
        self.health = health
        self.landed = True

        
    def draw(self, screen):
        '''
        Draws the ship on the screen.
        '''
        
        # Gets the triangle points for the ship, and then draws the ship
        triangle_points = [(self.x, self.y - self.size), (self.x - self.size, self.y + self.size), (self.x + self.size, self.y + self.size)]
        pygame.draw.polygon(screen, GlobalSettings.player_colors[self.player], triangle_points, width=3)
    
    def get_position(self):
        '''
        Returns the current position of the ship.
        '''
        
        return (self.x, self.y)
        
    def set_target(self, planet):
        '''
        Sets the target planet for the ship to move towards.
        '''
        
        self.next_planet = planet.id
        
        # Randomly selects a point on the planet to land on.
        x_offset = random.randint(-planet.radius + 15, planet.radius - 15)
        y_offset = random.randint(-planet.radius + 15, planet.radius - 15)
        x = planet.x + x_offset
        y = planet.y + y_offset
        
        #Starts moving towards the target.
        self.curr_target = pygame.Vector2(x, y)
        self.landed = False

    def update_position(self):
        '''
        Updates the position of the ship based on its speed and target.
        '''
        
        # If the ship is not landed, it moves towards the target.
        if self.pos != self.curr_target:
            direction = (self.curr_target - self.pos).normalize()
            distance = (self.curr_target - self.pos).length()

            if distance > self.speed:
                self.pos += direction * self.speed
            else:
                self.pos = self.curr_target
        
        self.x = self.pos[0]
        self.y = self.pos[1]

        # If the ship is at the target, it lands on the planet, and movement ceases.
        if self.pos == self.curr_target:
            self.landed = True
            self.curr_planet = self.next_planet
        
    def serialize(self):
        '''
        Serializes the ship object into a dictionary for sending over the network.
        '''
        
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
        '''
        Deserializes the ship object from a dictionary for receiving over the network.
        '''
        
        s = Ship(data["x"], data["y"], data["curr_planet"], data["player"], data["size"], data["speed"])
        s.next_planet = data["next_planet"]
        s.curr_target = data["curr_target"]
        s.health = data["health"]
        s.landed = data["landed"]
        return s