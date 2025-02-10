import pygame
import Planet
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2
 
HEIGHT = 800
WIDTH = 1000
FPS = 60
 
FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Game")

planet1 = Planet(400, 400)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((35, 35, 35)) 
    planet1.draw(screen)
    
    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()