import pygame
import random
import sys
import math
from Planet import planet_generator, planet_loc
from ShipLogic import handle_turn
from Scoreboard import Scoreboard
from Ship import Ship
from Shop import Shop
from pygame.locals import *
import GlobalSettings

FPS = 60
FramePerSec = pygame.time.Clock()

def runGame(screen, cpu1_setting, cpu2_setting):
    planets = planet_generator()
    ships = []
    selected_ships = []
    scoreboard = Scoreboard()
    scoreboard.update_player_sps(planets[0].point_value)
    scoreboard.update_opponent_sps(planets[1].point_value)
    shop = Shop()
    
    #init for dragging selection
    dragging = False
    dragging_start_pos = (0, 0)
    dragging_current_pos = (0, 0)
    
    # Set a timer to trigger every second (1000 milliseconds)
    SCORE_UPDATE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SCORE_UPDATE_EVENT, 1000)

    TURN_EVENT1 = pygame.USEREVENT + 2
    TURN_EVENT2 = pygame.USEREVENT + 3
    
    if GlobalSettings.computer1_difficulty.lower() == 'easy':
        pygame.time.set_timer(TURN_EVENT1, 3000)
    elif GlobalSettings.computer1_difficulty.lower() == 'medium':
        pygame.time.set_timer(TURN_EVENT1, 1000)
    elif GlobalSettings.computer1_difficulty.lower() == 'hard':
        pygame.time.set_timer(TURN_EVENT1, 250)
        
    if GlobalSettings.computer2_difficulty.lower() == 'easy':
        pygame.time.set_timer(TURN_EVENT2, 3000)
    elif GlobalSettings.computer2_difficulty.lower() == 'medium':
        pygame.time.set_timer(TURN_EVENT2, 1000)
    elif GlobalSettings.computer2_difficulty.lower() == 'hard':
        pygame.time.set_timer(TURN_EVENT2, 250)


    running = True
    while running:
        
        #Gets the currently held down keys
        keys = pygame.key.get_pressed()
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        
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
                clicked_planet = planet_loc(mouse_x, mouse_y, planets)
                if event.button == 1:
                    if shop.is_clicked(mouse_pos) and scoreboard.player_score >= 250 and GlobalSettings.shipcounts[0] < GlobalSettings.ship_limit:
                        #Buys a ship at original planet
                        x_offset = random.randint(-planets[0].radius + 15, planets[0].radius - 15)
                        y_offset = random.randint(-planets[0].radius + 15, planets[0].radius - 15)
                        x = planets[0].x + x_offset
                        y = planets[0].y + y_offset
                        ships.append(Ship(x, y, 0, player=GlobalSettings.curr_player))
                        scoreboard.update_player(-250)
                        GlobalSettings.shipcounts[0] += 1
                    
                    #Selects a single ship in the hitbox randomly (unless shift is being pressed)
                    if (not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]) or shop.is_clicked(mouse_pos):
                        for ship in selected_ships:
                            ship.is_selected = False
                        selected_ships = []
                        
                    for ship in ships:
                        if ship.is_clicked(mouse_pos) and ship.player == GlobalSettings.curr_player:
                            ship.is_selected = True
                            selected_ships.append(ship)
                    
                    #sets up dragging selection 
                    if not shop.is_clicked(mouse_pos):
                        dragging = True
                        dragging_start_pos = event.pos
                if event.button == 3:
                    # Movement Logic: Use the clicked planet to set the ship's target.
                    if clicked_planet is not None:
                        for ship in selected_ships:
                            ship.final_target = clicked_planet.id
            
            # Handle CPU turn event every 3 seconds
            elif event.type == TURN_EVENT1:
                handle_turn(cpu1_setting, scoreboard, planets, ships, planets[0], GlobalSettings.curr_player)
            elif event.type == TURN_EVENT2:
                handle_turn(cpu2_setting, scoreboard, planets, ships, planets[1], GlobalSettings.opposing_player)
                        
            # Handle scoreboard update event every second
            elif event.type == SCORE_UPDATE_EVENT:
                scoreboard.update()

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if dragging:
                        #Check if any ships are included
                        x, y = min(dragging_start_pos[0], dragging_current_pos[0]), min(dragging_start_pos[1], dragging_current_pos[1])
                        width = abs(dragging_current_pos[0] - dragging_start_pos[0])
                        height = abs(dragging_current_pos[1] - dragging_start_pos[1])
                        for ship in ships:
                            if x <= ship.x <= x + width and y <= ship.y <= y + height and ship.player == GlobalSettings.curr_player:
                                selected_ships.append(ship)
                                ship.is_selected = True
                                
                        dragging = False
                
        #Changes color of shop if hovered over
        shop.is_hovered(mouse_pos)
                
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

        #Group ships by planet
        planet_ship_map = {}
        for s in ships:
            # Which planet is this ship headed to?
            p = planets[s.curr_planet]
            # Check if ship has actually arrived inside p's radius
            distance = math.hypot(s.x - p.x, s.y - p.y)
            if distance < p.radius and s.landed:
                # Only then do we consider it "on" this planet
                planet_ship_map.setdefault(s.curr_planet, []).append(s)

        #Conflict logic
        for planet_id, ship_list in planet_ship_map.items():
            # how many different owners?
            owners = set(s.player for s in ship_list)
            if len(owners) > 1:
                # conflict => set planet.ship_attacking = True, apply damage multipliers, etc.
                conflict_planet = planets[planet_id]
                conflict_planet.ship_attacking = True
            if len(owners) < 2:
                continue  # no conflict if only one (or zero) owners

            # There's a conflict => pause capturing on this planet
            conflict_planet = planets[planet_id]
            conflict_planet.ship_attacking = True

            # Separate the ships by player
            user_ships = [s for s in ship_list if s.player == GlobalSettings.curr_player]
            cpu_ships = [s for s in ship_list if s.player == GlobalSettings.opposing_player]

            # If both sides exist, apply damage
            if len(user_ships) > 0 and len(cpu_ships) > 0:
                # Calculate difference
                # E.g. if 3 CPU ships vs 2 user ships => difference=1 => user ships take 1.1x damage
                u_count = len(user_ships)
                c_count = len(cpu_ships)
                difference = abs(u_count - c_count)

                # Base damage can be 1.0 each frame, or smaller if you want slower fights
                base_damage = 0.2

                # Decide who is outnumbered
                # If the CPU has more ships, user is outnumbered => user gets multiplier
                # If the user has more ships, CPU is outnumbered => CPU gets multiplier
                # If equal, both do base damage
                if difference > 0:
                    multiplier = 1.0 + 0.1 * difference
                    if c_count > u_count:
                        # user is outnumbered => user ships get extra damage
                        for ship in user_ships:
                            ship.health -= base_damage * multiplier
                        # CPU ships just get base damage
                        for ship in cpu_ships:
                            ship.health -= base_damage
                    elif u_count > c_count:
                        # CPU is outnumbered => CPU ships get extra damage
                        for ship in cpu_ships:
                            ship.health -= base_damage * multiplier
                        # user ships get base damage
                        for ship in user_ships:
                            ship.health -= base_damage
                else:
                    # difference == 0 => same # ships on each side => apply base damage to all
                    for ship in user_ships:
                        ship.health -= base_damage
                    for ship in cpu_ships:
                        ship.health -= base_damage

            #Remove destroyed ships (health <= 0)
            for s in ship_list[:]: 
                if s.health <= 0:
                    ship_list.remove(s)
                    ships.remove(s)
                    GlobalSettings.shipcounts[s.player - 1] -= 1


        # Capture Logic: Check if any ship has reached its target planet.
        for ship in ships:
            target_planet = planets[ship.curr_planet]
            distance = math.hypot(ship.x - target_planet.x, ship.y - target_planet.y)

            # "Conflict check": if ship_attacking is True, skip capturing
            if distance < target_planet.radius:
                # Are we in conflict? If so, skip capturing
                in_conflict = target_planet.ship_attacking
                if not in_conflict and target_planet.player_num != ship.player:
                    # normal capture logic
                    if target_planet.health >= 0:
                        target_planet.change_health(-3)
                        target_planet.ship_attacking = True
                    else:
                        # Planet changes ownership
                        if ship.player == GlobalSettings.curr_player:
                            scoreboard.update_player_sps(target_planet.point_value)
                        else:
                            scoreboard.update_opponent_sps(target_planet.point_value)
                        target_planet.change_player(ship.player)
                        target_planet.ship_attacking = False
            
        #Planets healing        
        for planet in planets:
            if not planet.ship_attacking and planet.health < planet.max_health:
                planet.change_health(5)
            has_ship_attacking = False
            for ship in ships:
                if ship.curr_planet == planet.id:
                    has_ship_attacking == True
            
            if not has_ship_attacking:
                planet.ship_attacking = False
            
        scoreboard.draw(screen)
        shop.draw(screen)
        
        #Draws and selects the rectangle for selcting ships
        if dragging:
            dragging_current_pos = pygame.mouse.get_pos()
            
            x, y = min(dragging_start_pos[0], dragging_current_pos[0]), min(dragging_start_pos[1], dragging_current_pos[1])
            width = abs(dragging_current_pos[0] - dragging_start_pos[0])
            height = abs(dragging_current_pos[1] - dragging_start_pos[1])

            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((GlobalSettings.neutral_color[0], GlobalSettings.neutral_color[1], GlobalSettings.neutral_color[2], 100))

            screen.blit(overlay, (x, y))

            
        
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

def pauseMenu(screen, WIDTH, HEIGHT):
    pause_font = pygame.font.Font(None, 72)
    option_font = pygame.font.Font(None, 48)
    pause_text = pause_font.render("Paused", True, GlobalSettings.neutral_color)
    resume_text = option_font.render("Press R to Resume", True, GlobalSettings.neutral_color)
    quit_text = option_font.render("Press Q to Quit", True, GlobalSettings.neutral_color)
    
    # Define volume slider variables.
    volume_slider_rect = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 150, 220, 10)
    slider_handle_radius = 10
    dragging_slider = False
    
    paused = True
    clock = pygame.time.Clock()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume game
                    paused = False
                elif event.key == pygame.K_q:  # Quit game
                    return "home"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click only
                    mouse = pygame.mouse.get_pos()
                    if volume_slider_rect.collidepoint(mouse):
                        dragging_slider = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_slider = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging_slider:
                    mouse_x = event.pos[0]
                    relative_x = mouse_x - volume_slider_rect.x
                    new_volume = relative_x / volume_slider_rect.width
                    new_volume = max(0, min(new_volume, 1))  # Clamp between 0 and 1
                    GlobalSettings.volume = new_volume
                    pygame.mixer.music.set_volume(new_volume)

        # Fill screen with background color based on current settings.
        bg_color = GlobalSettings.dark_mode_bg if GlobalSettings.dark_background else GlobalSettings.light_mode_bg
        screen.fill(bg_color)
        
        # Draw pause texts.
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(pause_text, pause_rect)
        screen.blit(resume_text, resume_rect)
        screen.blit(quit_text, quit_rect)
        
        # Draw volume slider bar.
        pygame.draw.rect(screen, GlobalSettings.gray, volume_slider_rect)
        # Calculate the handle's position based on the current volume.
        handle_x = volume_slider_rect.x + int(GlobalSettings.volume * volume_slider_rect.width)
        handle_y = volume_slider_rect.centery
        mouse = pygame.mouse.get_pos()
        handle_color = GlobalSettings.black if volume_slider_rect.collidepoint(mouse) else GlobalSettings.gray
        pygame.draw.circle(screen, handle_color, (handle_x, handle_y), slider_handle_radius)
        # Render the volume percentage above the slider bar.
        vol_percentage = int(GlobalSettings.volume * 100)
        vol_text = option_font.render(f"Volume: {vol_percentage}%", True, GlobalSettings.neutral_color)
        vol_rect = vol_text.get_rect(midbottom=(volume_slider_rect.centerx, volume_slider_rect.y - 10))
        screen.blit(vol_text, vol_rect)
        
        pygame.display.flip()
        clock.tick(30)
    
    return "resume"


def checkForWinner(planets):
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