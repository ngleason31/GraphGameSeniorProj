import pygame
import sys
from Planet import Planet
from pygame.locals import *
import StartScreen

pygame.init()
vec = pygame.math.Vector2
 
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
FPS = 60
FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Game")
clock = pygame.time.Clock()

def runGame():
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
    sys.exit()


def main():
    option = StartScreen.welcomeScreen()
    print("User Selected: ", option)
    runGame()
    if option in ["player1", "player2"]:
        runGame()
    else:
        print("Other option selected. Exiting for now.")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
