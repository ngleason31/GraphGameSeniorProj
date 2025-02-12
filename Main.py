import pygame
import sys
from Planet import Planet
from pygame.locals import *
import StartScreen
import Credits

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

    return

def main():
    while True:
        option = StartScreen.welcomeScreen()
        print("User Selected: ", option)

        if option in ["player1", "player2"]:
            runGame()
        elif option == "credits":
            print("Credits selected. ")
            ret = Credits.runCredits()
        
        elif option == "settings":
            # Show the settings screen, etc.
            pass

        elif option == "quit" or option is None:
            print("Quitting game. ")
            pygame.quit()
            sys.exit()
    

if __name__ == "__main__":
    main()
