import pygame
import Planet
import Ship
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2
 
HEIGHT = 800
WIDTH = 1000
FPS = 60
 
FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Game")

planet1 = Planet.Planet(400, 400)
ship1 = Ship.Ship(100, 100)


running = True
while running:
    screen.fill((35, 35, 35)) 
    planet1.draw(screen)
    ship1.update_position()
    ship1.draw(screen)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            ship1.set_target(*mouse_pos)

    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()