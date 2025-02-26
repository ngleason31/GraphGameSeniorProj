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
from playsound import playsound

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

FPS = 60
FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((GlobalSettings.WIDTH, GlobalSettings.HEIGHT))
pygame.display.set_caption("Graph Game")
clock = pygame.time.Clock()

def pauseMenu(screen, WIDTH, HEIGHT):
    pause_font = pygame.font.Font(None, 72)
    option_font = pygame.font.Font(None, 48)
    pause_text = pause_font.render("Paused", True, GlobalSettings.neutral_color)
    resume_text = option_font.render("Press R to Resume", True, GlobalSettings.neutral_color)
    quit_text = option_font.render("Press Q to Quit", True, GlobalSettings.neutral_color)
    
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume game
                    paused = False
                elif event.key == pygame.K_q:  # Quit game
                    return "home"
        
        # Fill screen with background color based on current settings
        bg_color = GlobalSettings.dark_mode_bg if GlobalSettings.dark_background else GlobalSettings.light_mode_bg
        screen.fill(bg_color)
        
        # Draw pause texts
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(pause_text, pause_rect)
        screen.blit(resume_text, resume_rect)
        screen.blit(quit_text, quit_rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    return "resume"

def how_to_play_menu(screen, WIDTH, HEIGHT):
    instructions = [
        "How to Play:",
        "1. Left-click to move your ship.",
        "2. Right-click (if score >= 50) to spawn a new ship.",
        "3. Press ESC to pause the game.",
        "",
        "Press any key or click to start!"
    ]
    
    clock = pygame.time.Clock()
    waiting = True
    font = pygame.font.Font(None, 36)
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False
        
        # Use global background color based on settings
        bg_color = GlobalSettings.dark_mode_bg if GlobalSettings.dark_background else GlobalSettings.light_mode_bg
        screen.fill(bg_color)
        
        # Draw each line of instructions centered on screen
        y_offset = HEIGHT // 4
        for line in instructions:
            text_surface = font.render(line, True, GlobalSettings.neutral_color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40  # Adjust spacing between lines
        
        pygame.display.flip()
        clock.tick(60)
    
    return "start"

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Call the pause menu
                    result = pauseMenu(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
                    if result == "home":
                        return "home"
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
            how_to_play_menu(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
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
            GlobalSettings.update_audio()
            if ret == "quit":
                running = False
        elif option.lower() == "quit" or option is None:
            running = False

    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()