import pygame
import sys
from Planet import Planet
from pygame.locals import *
import StartScreen
import Credits
import Settings
import GlobalSettings

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
                return "quit"
        # Use global background setting for the game.
        if GlobalSettings.dark_background:
            bg_color = (35, 35, 35)
        else:
            bg_color = (220, 220, 220)
        screen.fill((35, 35, 35)) 
        planet1.draw(screen)  
        pygame.display.update()
        FramePerSec.tick(FPS)

    return

def main(): 
    running = True
    while running:
        pygame.display.set_caption("Graph Game")
        pygame.event.clear()

        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()  # Process internal actions.
            pygame.time.delay(10)
        # Show welcome screen and wait for the user to select an option.
        option = StartScreen.welcomeScreen(screen, WIDTH, HEIGHT)
        print("User Selected:", option)
  
        if option in ["player 1", "player 2"]:
            res = runGame()
            if res == "quit":
                running = False
        elif option.lower() == "credits":
            ret = Credits.runCredits(screen, WIDTH, HEIGHT)
            if ret == "quit":
                running = False
        elif option.lower() == "settings":
            ret = Settings.runSettings(screen, WIDTH, HEIGHT)
            if ret == "quit":
                running = False
        elif option.lower() == "quit" or option is None:
            running = False

    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
