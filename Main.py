import pygame
import random
import sys
from Planet import planet_generator, planet_loc
from Scoreboard import Scoreboard
from Ship import Ship
from pygame.locals import *
import StartScreen
import Credits
import Settings
import GlobalSettings

pygame.init()
vec = pygame.math.Vector2
 
 
infoObject = pygame.display.Info()
GlobalSettings.WIDTH = infoObject.current_w
GlobalSettings.HEIGHT = infoObject.current_h

FPS = 60
FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((GlobalSettings.WIDTH, GlobalSettings.HEIGHT))
pygame.display.set_caption("Graph Game")
clock = pygame.time.Clock()

def runGame():
    planets = planet_generator()
    ships = []
    scoreboard = Scoreboard()
    
    SCORE_UPDATE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SCORE_UPDATE_EVENT, 1000)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                planet = planet_loc(mouse_x, mouse_y, planets)
                if event.button == 1:
                    for ship in ships:
                        if planet != None and planet.id in planets[ship.curr_planet].connections:
                            ship.set_target(planet)                     
                if event.button == 3 and scoreboard.player_score >= 50:
                    if planet != None and planet.player_num == GlobalSettings.curr_player:
                        x_offset = random.randint(planet.radius, planet.radius + 5)
                        y_offset = random.randint(planet.radius, planet.radius + 5)
                        x = mouse_x + x_offset
                        y = mouse_y + y_offset
                        ships.append(Ship(x, y, planet.id, player=GlobalSettings.curr_player))
                        scoreboard.update_player(-50)
            elif event.type == SCORE_UPDATE_EVENT:
                scoreboard.update() 
                
        #Use global background setting for the game.
        if GlobalSettings.dark_background:
            bg_color = GlobalSettings.dark_mode_bg
        else:
            bg_color = GlobalSettings.light_mode_bg

        screen.fill(bg_color) 
        for planet in planets:
            planet.draw(screen, planets)
        for ship in ships:
            ship.update_position()
            ship.draw(screen)
            
        scoreboard.draw(screen)
        
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
        option = StartScreen.welcomeScreen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
        print("User Selected:", option)
  
        if option.lower() in "player 1":
            GlobalSettings.curr_player = 1
            GlobalSettings.opposing_player = 2
            res = runGame()
            if res == "quit":
                running = False
        elif option.lower() in "player 2":
            GlobalSettings.curr_player = 2
            GlobalSettings.opposing_player = 1
            res = runGame()
            if res == "quit":
                running = False
        elif option.lower() == "credits":
            ret = Credits.runCredits(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            if ret == "quit":
                running = False
        elif option.lower() == "settings":
            ret = Settings.runSettings(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            if ret == "quit":
                running = False
        elif option.lower() == "quit" or option is None:
            running = False

    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
