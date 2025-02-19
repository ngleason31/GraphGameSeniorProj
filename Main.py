import pygame
import Planet
import Ship
import random
import sys
from Planet import Planet
from Ship import Ship
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
curr_player = 0

def planet_generator():
    planets = []
    num_planets = random.randint(5, 10)
    
    for _ in range(num_planets):
        radius = random.randint(30, 80)
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        planets.append(Planet(x, y, radius))
        
    player_planet = random.randint(0, num_planets - 1)
    planets[player_planet].change_player(curr_player)
        
    return planets

def runGame():
    planets = planet_generator()
    ships = []

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    for ship in ships:
                        x_offset = random.randint(-30, 30)
                        y_offset = random.randint(-30, 30)
                        ship.set_target(mouse_x + x_offset, mouse_y + y_offset)
                if event.button == 3:
                    ships.append(Ship(mouse_x, mouse_y, player=curr_player))
        #Use global background setting for the game.
        if GlobalSettings.dark_background:
            bg_color = GlobalSettings.dark_mode_bg
        else:
            bg_color = GlobalSettings.light_mode_bg

        screen.fill(bg_color) 
        for planet in planets:
            planet.draw(screen)
        for ship in ships:
            ship.update_position()
            ship.draw(screen)
            
        pygame.display.update()
        FramePerSec.tick(FPS)

    return

def main(): 
    running = True
    while running:
        global curr_player
        pygame.display.set_caption("Graph Game")
        pygame.event.clear()

        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()  # Process internal actions.
            pygame.time.delay(10)
        # Show welcome screen and wait for the user to select an option.
        option = StartScreen.welcomeScreen(screen, WIDTH, HEIGHT)
        print("User Selected:", option)
  
        if option.lower() in "player 1":
            curr_player = 1
            res = runGame()
            if res == "quit":
                running = False
        elif option.lower() in "player 2":
            curr_player = 2
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
