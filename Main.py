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

# Saves the width and height of the screen
infoObject = pygame.display.Info()
GlobalSettings.WIDTH = infoObject.current_w
GlobalSettings.HEIGHT = infoObject.current_h

# Initialize the screen
screen = pygame.display.set_mode((GlobalSettings.WIDTH, GlobalSettings.HEIGHT))
pygame.display.set_caption("Graph Game")
clock = pygame.time.Clock()

def main(): 
    '''
    Main function to run the game. It initializes the game, displays the welcome screen,
    and handles user input for selecting game modes and settings.
    '''
    
    running = True
    while running:
        pygame.display.set_caption("Graph Game")
        pygame.event.clear()

        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()
            pygame.time.delay(10)
        # Show welcome screen and wait for the user to select an option.
        option = StartScreen.welcomeScreen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
  
        # Checks each option selected by the user and runs the corresponding function.
        if option.lower() == "single player":
            # Initializes the players for single player mode (human and computer).
            player1 = Player(1, GlobalSettings.orange, 0, 'player')
            player2 = Player(2, GlobalSettings.blue, 1, 'computer')
            GlobalSettings.curr_player = 1
            GlobalSettings.opposing_player = 2
            res = selection_screen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT, 'single player', player1, player2)
            if res[0] != "home":
                player1.change_setting(res[1])
                player2.change_setting(res[2])
                # Run the game with the selected settings.
                res = runGame(screen, player1, player2)
                if res == "quit":
                    running = False
        elif option.lower() in "multiplayer":
            # Initializes the players for multiplayer mode (two human players).
            player1 = Player(1, GlobalSettings.orange, 0, 'player')
            player2 = Player(2, GlobalSettings.blue, 1, 'player')
            GlobalSettings.curr_player = 1
            GlobalSettings.opposing_player = 2
            res = selection_screen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT, 'multiplayer', player1, player2)
            # Added for client/server screens
            if res[0] == "multiplayer_menu":
                option = "multiplayer" 
                continue
            # Checks if the user selected the host or join option.
            elif res[0] != "home" and res[0].lower() == "server":
                player1.change_setting(res[1])
                player2.change_setting(res[2])
                # Pass the entered host IP (res[3]) to the server function and hosts the game.
                res_server = server(screen, player1, player2, res[3])
                if res_server == "quit":
                    running = False
            elif res[0] != "home" and res[0].lower() == "client":
                player1.change_setting(res[1])
                player2.change_setting(res[2])
                # Enters client mode and connects to the server using the entered host IP (res[3]).
                res_client = client(screen, player1, player2, res[3])
                if res_client == "quit":
                    running = False
        elif option.lower() in "computer":
            # Initializes the players for computer vs computer mode.
            player1 = Player(1, GlobalSettings.orange, 0, 'player')
            player2 = Player(2, GlobalSettings.blue, 1, 'player')
            GlobalSettings.curr_player = 1
            GlobalSettings.opposing_player = 2
            res = selection_screen(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT, 'computer', player1, player2)
            if res[0] != "home":
                # Grabs the two settings from the selection screen results
                player1.change_setting(res[1])
                player2.change_setting(res[2])
                res = runGame(screen, player1, player2)
                if res == "quit":
                    running = False
        elif option.lower() == "credits":
            # Runs the credits screen.
            res = Credits.runCredits(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            if res == "quit":
                running = False
        elif option.lower() == "settings":
            # Enters the settings menu.
            res = Settings.runSettings(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            # Helper to update the audio settings
            GlobalSettings.update_audio()
            if res == "quit":
                running = False
        elif option.lower() == "quit" or option is None:
            # Quits the game.
            running = False

    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    # Calls the main function to start the game.
    main()