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
import math

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

def checkForWinner(planets):
    # Assume that a planet with player_num 0 is neutral.
    # If all planets are owned by the same non-zero player, that player wins.
    first_owner = planets[0].player_num
    if first_owner == 0:
        return None
    for planet in planets:
        if planet.player_num != first_owner:
            return None
    return first_owner

def winnerScreen(winner, screen, WIDTH, HEIGHT):
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 48)
    
    congrats_text = font_large.render(f"Congratulations, Player {winner} Wins!", True, GlobalSettings.neutral_color)
    
    play_again_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50)
    home_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 120, 300, 50)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse):
                    return "play_again"
                if home_button.collidepoint(mouse):
                    return "home"
                    
        bg_color = GlobalSettings.dark_mode_bg if GlobalSettings.dark_background else GlobalSettings.light_mode_bg
        screen.fill(bg_color)
        
        congrats_rect = congrats_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(congrats_text, congrats_rect)

        mouse = pygame.mouse.get_pos()

        # Draw Play Again button with hover effect.
        if play_again_button.collidepoint(mouse):
            pygame.draw.rect(screen, GlobalSettings.black, play_again_button)
        else:
            pygame.draw.rect(screen, GlobalSettings.gray, play_again_button)

        # Draw Home button with hover effect.
        if home_button.collidepoint(mouse):
            pygame.draw.rect(screen, GlobalSettings.black, home_button)
        else:
            pygame.draw.rect(screen, GlobalSettings.gray, home_button)
        
        play_again_text = font_small.render("Play Again", True, GlobalSettings.neutral_color)
        home_text = font_small.render("Home", True, GlobalSettings.neutral_color)
        
        play_again_rect = play_again_text.get_rect(center=play_again_button.center)
        home_rect = home_text.get_rect(center=home_button.center)
        
        screen.blit(play_again_text, play_again_rect)
        screen.blit(home_text, home_rect)
        
        pygame.display.flip()
        clock.tick(60)

def runGame():
    planets = planet_generator()
    ships = []
    scoreboard = Scoreboard()

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
                clicked_planet = planet_loc(mouse_x, mouse_y, planets)
                if event.button == 1:
                    for ship in ships:
                        for p in planets:
                            distance = math.sqrt((ship.x - p.x) ** 2 + (ship.y - p.y) ** 2)
                            # Check if the ship is close enough to capture the planet and if the planet has a nonzero point value.
                            if distance < p.radius and p.point_value > 0 and p.player_num != ship.player:
                                # Capture: update the score according to the ship's owner.
                                if ship.player == GlobalSettings.curr_player:
                                    scoreboard.update_player(p.point_value)
                                else:
                                    scoreboard.update_opponent(p.point_value)
                                # Change planet ownership and set its point value to 0 so that it can't be captured repeatedly.
                                p.change_player(ship.player)
                                p.point_value = 0
                    # Movement Logic: Use the clicked planet to set the ship's target.
                    if clicked_planet is not None:
                        for ship in ships:
                            current_planet = planets[ship.curr_planet]
                            # Check if the clicked planet is connected to the ship's current planet.
                            if clicked_planet.id in current_planet.connections:
                                ship.set_target(clicked_planet)
                                break                 
                if event.button == 3 and scoreboard.player_score >= 50:
                    if clicked_planet != None and clicked_planet.player_num == GlobalSettings.curr_player:
                        # x_offset = random.randint(clicked_planet.radius, clicked_planet.radius)
                        # y_offset = random.randint(clicked_planet.radius, clicked_planet.radius)
                        # x = mouse_x + x_offset
                        # y = mouse_y + y_offset
                        x = clicked_planet.x
                        y = clicked_planet.y
                        ships.append(Ship(x, y, clicked_planet.id, player=GlobalSettings.curr_player))
                        scoreboard.update_player(-50)
                
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

        # Capture Logic: Check if any ship has reached its target planet.
        for ship in ships:
            target_planet = planets[ship.curr_planet]
            distance = math.hypot(ship.x - target_planet.x, ship.y - target_planet.y)
            if distance < target_planet.radius and target_planet.point_value > 0 and target_planet.player_num != ship.player:
                if ship.player == GlobalSettings.curr_player:
                    scoreboard.update_player(target_planet.point_value)
                else:
                    scoreboard.update_opponent(target_planet.point_value)
                target_planet.change_player(ship.player)
                target_planet.point_value = 0
            
        scoreboard.draw(screen)
        
        pygame.display.update()
        FramePerSec.tick(FPS)

        # Check for a winner after each frame.
        winner = checkForWinner(planets)
        if winner is not None:
            result = winnerScreen(winner, screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            if result == "play_again":
                return runGame()
            elif result == "home":
                return "home"

    return

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
            how_to_play_menu(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
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