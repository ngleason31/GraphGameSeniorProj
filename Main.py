import pygame
import sys
from pygame.locals import *
import StartScreen
import Credits
import Settings
import GlobalSettings
from SelectionScreen import selection_screen
from Game import runGame
from Player import Player
from Server import server
from Client import client
pygame.init()
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load("Audio/gameMusic.mp3")
pygame.mixer.music.play(-1)
GlobalSettings.update_audio()

vec = pygame.math.Vector2

infoObject = pygame.display.Info()
GlobalSettings.WIDTH = infoObject.current_w
GlobalSettings.HEIGHT = infoObject.current_h

screen = pygame.display.set_mode((GlobalSettings.WIDTH, GlobalSettings.HEIGHT))
pygame.display.set_caption("Graph Game")
clock = pygame.time.Clock()

player1 = Player(1, GlobalSettings.orange, 0, 'player')
player2 = Player(2, GlobalSettings.blue, 1, 'player')

def main(): 
    running = True
    while running:
        pygame.display.set_caption("Graph Game")
        pygame.event.clear()

        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()
            pygame.time.delay(10)
        # Show welcome screen and wait for the user to select an option.
        option = StartScreen.welcomeScreen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
  
        if option.lower() == "single player":
            GlobalSettings.curr_player = 1
            GlobalSettings.opposing_player = 2
            res = selection_screen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT, 'single player', player1, player2)
            if res[0] != "home":
                player1.change_setting(res[1])
                player2.change_setting(res[2])
                res = runGame(screen, player1, player2)
                if res == "quit":
                    running = False
        elif option.lower() in "multiplayer":   
            GlobalSettings.curr_player = 2
            GlobalSettings.opposing_player = 1
            res = selection_screen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT, 'multiplayer', player1, player2)
            if res[0] != "home" and res[0].lower() == "server":
                player1.change_setting(res[1])
                player2.change_setting(res[2])
                res = server(screen, player1, player2)
                if res == "quit":
                    running = False
            if res[0] != "home" and res[0].lower() == "client":
                player1.change_setting(res[1])
                player2.change_setting(res[2])
                res = client(screen, player1, player2)
                if res == "quit":
                    running = False
        elif option.lower() in "computer":
            GlobalSettings.curr_player = 1
            GlobalSettings.opposing_player = 2
            res = selection_screen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT, 'computer', player1, player2)
            if res[0] != "home":
                player1.change_setting(res[1])
                player2.change_setting(res[2])
                res = runGame(screen, player1, player2)
                if res == "quit":
                    running = False
        elif option.lower() == "credits":
            res = Credits.runCredits(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            if res == "quit":
                running = False
        elif option.lower() == "settings":
            res = Settings.runSettings(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            GlobalSettings.update_audio()
            if res == "quit":
                running = False
        elif option.lower() == "quit" or option is None:
            running = False

    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()