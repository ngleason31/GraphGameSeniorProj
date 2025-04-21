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
from Player import Player
import GlobalSettings
from Debug import DebugConsole
from NetworkUtils import recv_msg

FPS = 60
FramePerSec = pygame.time.Clock()

def runGame(screen, player1, player2, server_mode=False, broadcast=None, server=None):
    '''
    Main game loop which handles most of the game logic (Other than the ship logic).
    It handles the game state, player actions, and rendering.
    '''
    
    # Generate planets and initialize game objects.
    planets = planet_generator()
    ships = []
    scoreboard = Scoreboard()
    scoreboard.update_player_sps(planets[0].point_value)
    scoreboard.update_opponent_sps(planets[1].point_value)
    console = DebugConsole()
    shop = Shop()
    clicked_planet = None
    
    # Set a timer to trigger every second (1000 milliseconds).
    SCORE_UPDATE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SCORE_UPDATE_EVENT, 1000)

    # Creates player turn events
    TURN_EVENT1 = pygame.USEREVENT + 2
    TURN_EVENT2 = pygame.USEREVENT + 3
    
    # Adjusts the turn speed based on player difficulty.
    if player1.difficulty.lower() == 'easy':
        pygame.time.set_timer(TURN_EVENT1, 3000)
    elif player1.difficulty.lower() == 'medium':
        pygame.time.set_timer(TURN_EVENT1, 1000)
    elif player1.difficulty.lower() == 'hard':
        pygame.time.set_timer(TURN_EVENT1, 250)
        
    if player2.difficulty.lower() == 'easy':
        pygame.time.set_timer(TURN_EVENT2, 3000)
    elif player2.difficulty.lower() == 'medium':
        pygame.time.set_timer(TURN_EVENT2, 1000)
    elif player2.difficulty.lower() == 'hard':
        pygame.time.set_timer(TURN_EVENT2, 250)


    running = True
    while running:
        
        # Always gets mouse position.
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        
        for event in pygame.event.get():
            # Handles the console input.
            console.handle_typing(event, player1, player2, planets, ships)
            
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Call the pause menu.
                    result = pauseMenu(screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
                    if result == "home":
                        return "home"
                if event.key == pygame.K_LCTRL:
                    # Toggles the debug console.
                    console.toggle()
                    
            # Only activates mouse clickes if a player is playing
            elif event.type == MOUSEBUTTONDOWN and player1.settings.lower() == 'player':
                if event.button == 1:
                    # Logic for buying ships
                    if shop.is_clicked(mouse_pos) and scoreboard.player_score >= GlobalSettings.ship_price and player1.ship_count < GlobalSettings.ship_limit:
                        #Buys a ship at original planet (with an offset).
                        x_offset = random.randint(-planets[0].radius + 15, planets[0].radius - 15)
                        y_offset = random.randint(-planets[0].radius + 15, planets[0].radius - 15)
                        x = planets[0].x + x_offset
                        y = planets[0].y + y_offset
                        ships.append(Ship(x, y, 0, player=GlobalSettings.curr_player))
                        scoreboard.update_player(-GlobalSettings.ship_price)
                        player1.ship_count += 1
                if event.button == 3:
                    # Logic for selecting a planet (Right click).
                    if clicked_planet:
                        clicked_planet.selected = False
                    # Finds the planet ID based on the mouse position.
                    clicked_planet = planet_loc(mouse_x, mouse_y, planets)
                    if clicked_planet:
                        # Sets the target planet to the most recently selected planet.
                        player1.target_planet = clicked_planet.id
                        clicked_planet.selected = True
            
            # Handle Player or CPU turn event according to the difficulty.
            elif event.type == TURN_EVENT1:
                handle_turn(player1.settings, scoreboard, planets, ships, planets[0], player1)
            elif event.type == TURN_EVENT2:
                handle_turn(player2.settings, scoreboard, planets, ships, planets[1], player2)
                        
            # Handle scoreboard update event every second.
            elif event.type == SCORE_UPDATE_EVENT:
                scoreboard.update()
        
        #C hanges color of shop if hovered over.
        if player1.settings.lower() == 'player':
            shop.is_hovered(mouse_pos)
                
        # Use global background setting for the game.
        if GlobalSettings.dark_background:
            bg_color = GlobalSettings.dark_mode_bg
        else:
            bg_color = GlobalSettings.light_mode_bg

        screen.fill(bg_color) 
        
        # Draws planets and ship.
        for planet in planets:
            planet.draw(screen, planets)
        for ship in ships:
            ship.update_position()
            ship.draw(screen)

        # Groups ships by planet.
        planet_ship_map = {}
        for s in ships:
            # Which planet is this ship headed to?
            p = planets[s.curr_planet]
            # Check if ship has actually arrived inside p's radius.
            distance = math.hypot(s.x - p.x, s.y - p.y)
            if distance < p.radius and s.landed:
                # Only then do we consider it "on" this planet.
                planet_ship_map.setdefault(s.curr_planet, []).append(s)

        # Conflict logic.
        for planet_id, ship_list in planet_ship_map.items():
            # How many different owners?
            owners = set(s.player for s in ship_list)
            if len(owners) > 1:
                # conflict => set planet.ship_attacking = True, apply damage multipliers, etc.
                conflict_planet = planets[planet_id]
                conflict_planet.ship_attacking = True
            if len(owners) < 2:
                continue  # no conflict if only one (or zero) owners.

            # There's a conflict => pause capturing on this planet.
            conflict_planet = planets[planet_id]
            conflict_planet.ship_attacking = True

            # Separate the ships by player.
            user_ships = [s for s in ship_list if s.player == GlobalSettings.curr_player]
            cpu_ships = [s for s in ship_list if s.player == GlobalSettings.opposing_player]

            # If both sides exist, apply damage.
            if len(user_ships) > 0 and len(cpu_ships) > 0:
                # Calculate difference.
                # E.g. if 3 CPU ships vs 2 user ships => difference=1 => user ships take 1.1x damage.
                u_count = len(user_ships)
                c_count = len(cpu_ships)
                difference = abs(u_count - c_count)

                # Base damage can be 1.0 each frame, or smaller if you want slower fights.
                base_damage = 0.2

                # Decide who is outnumbered
                # If the CPU has more ships, user is outnumbered => user gets multiplier.
                # If the user has more ships, CPU is outnumbered => CPU gets multiplier.
                # If equal, both do base damage.
                if difference > 0:
                    multiplier = 1.0 + 0.1 * difference
                    if c_count > u_count:
                        # user is outnumbered => user ships get extra damage.
                        for ship in user_ships:
                            ship.health -= base_damage * multiplier
                        # CPU ships just get base damage.
                        for ship in cpu_ships:
                            ship.health -= base_damage
                    elif u_count > c_count:
                        # CPU is outnumbered => CPU ships get extra damage.
                        for ship in cpu_ships:
                            ship.health -= base_damage * multiplier
                        # user ships get base damage.
                        for ship in user_ships:
                            ship.health -= base_damage
                else:
                    # difference == 0 => same # ships on each side => apply base damage to all.
                    for ship in user_ships:
                        ship.health -= base_damage
                    for ship in cpu_ships:
                        ship.health -= base_damage

            # Remove destroyed ships (health <= 0).
            for s in ship_list[:]: 
                if s.health <= 0:
                    ship_list.remove(s)
                    ships.remove(s)
                    if s.player == 1:
                        player1.ship_count -= 1
                    if s.player == 2:
                        player2.ship_count -= 1


        # Capture Logic: Check if any ship has reached its target planet.
        for ship in ships:
            target_planet = planets[ship.curr_planet]
            distance = math.hypot(ship.x - target_planet.x, ship.y - target_planet.y)

            # "Conflict check": if ship_attacking is True, skip capturing.
            if distance < target_planet.radius:
                # Are we in conflict? If so, skip capturing.
                in_conflict = target_planet.ship_attacking
                if not in_conflict and target_planet.player_num != ship.player:
                    # normal capture logic.
                    if target_planet.health >= 0:
                        target_planet.change_health(-3)
                        target_planet.ship_attacking = True
                    else:
                        # Planet changes ownership.
                        if ship.player == player1.player_num:
                            scoreboard.update_player_sps(target_planet.point_value)
                        else:
                            scoreboard.update_opponent_sps(target_planet.point_value)
                        target_planet.change_player(ship.player)
                        target_planet.ship_attacking = False
            
        #Planets heal if not under attack.        
        for planet in planets:
            if not planet.ship_attacking and planet.health < planet.max_health:
                planet.change_health(5)
            has_ship_attacking = False
            for ship in ships:
                if ship.curr_planet == planet.id:
                    has_ship_attacking == True
            
            if not has_ship_attacking:
                planet.ship_attacking = False
                
        # Check for a winner after each frame.
        winner = checkForWinner(planets)
        
        # Handles server logic.
        if server_mode:
            # receives the action from the client.
            action  = recv_msg(server)
            if action != None:
                if action["type"] == "buy_ship":
                    if scoreboard.opponent_score >= GlobalSettings.ship_price and player2.ship_count < GlobalSettings.ship_limit:
                        # Buys a ship at opponenets planet.
                        x_offset = random.randint(-planets[1].radius + 15, planets[1].radius - 15)
                        y_offset = random.randint(-planets[1].radius + 15, planets[1].radius - 15)
                        x = planets[1].x + x_offset
                        y = planets[1].y + y_offset
                        ships.append(Ship(x, y, 1, player=GlobalSettings.opposing_player))
                        scoreboard.update_opponent(-GlobalSettings.ship_price)
                        player2.ship_count += 1
                if action["type"] == "select_planet":
                    # Figures out what was selected by the client.
                    player2.target_planet = action["planet_id"]
            
            # Sends the game state to the client.
            game_state = {
                'planets': [planet.serialize() for planet in planets],
                'ships': [ship.serialize() for ship in ships],
                'scoreboard': scoreboard.serialize(),
                'Winner': winner
            }
            broadcast(game_state)

        # Draws and updates the scoreboard.
        scoreboard.draw(screen)
        scoreboard.update_shipcount(player1, player2)
        
        # Draws the console if it is active.
        console.draw(screen)
        
        # Only draws the shop if a player is playing.
        if player1.settings.lower() == 'player':
            shop.draw(screen)
     
        # Updates the display
        pygame.display.update()
        FramePerSec.tick(FPS)

        if winner is not None:
            # Sends to winner screen
            result = winnerScreen(winner, screen, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            if result == "play_again":
                # Resets game.
                player1 = Player(1, GlobalSettings.orange, 0, player1.settings)
                player2 = Player(2, GlobalSettings.blue, 1, player2.settings)
                return runGame(screen, player1, player2, server_mode, broadcast, server)
            elif result == "home":
                # Returns to menu.
                return "home"

    return

def pauseMenu(screen, WIDTH, HEIGHT):
    '''
    Displays the pause menu with options to resume or quit the game.
    '''
    
    # Initialize fonts and texts.
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
                if event.key == pygame.K_r:  # Resumes game,
                    paused = False
                elif event.key == pygame.K_q:  # Quits game.
                    return "home"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click only,
                    mouse = pygame.mouse.get_pos()
                    # Changes the volume if the slider is clicked.
                    if volume_slider_rect.collidepoint(mouse):
                        dragging_slider = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_slider = False
            elif event.type == pygame.MOUSEMOTION:
                # Logic for dragging the slider when handling mouse motion.
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
    '''
    Checks if there is a winner based on the home planets' ownership.
    '''
    # If player one's home planet (index 0) is owned by player two, player two wins.
    if planets[0].player_num == 2:
        return 2
    # If player two's home planet (index 1) is owned by player one, player one wins.
    elif planets[1].player_num == 1:
        return 1
    else:
    # If no one has won yet, return None.
        return None

def winnerScreen(winner, screen, WIDTH, HEIGHT):
    '''
    Displays the winner screen with options to play again or go home.
    '''
    
    # Initialize fonts, texts, and buttons.
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
                # Checks if the user clicked on the play again or home button.
                mouse = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse):
                    return "play_again"
                if home_button.collidepoint(mouse):
                    return "home"
                    
        # Draws the background and rects
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
        
        # Render button texts.
        play_again_text = font_small.render("Play Again", True, GlobalSettings.neutral_color)
        home_text = font_small.render("Home", True, GlobalSettings.neutral_color)
        
        play_again_rect = play_again_text.get_rect(center=play_again_button.center)
        home_rect = home_text.get_rect(center=home_button.center)
        
        screen.blit(play_again_text, play_again_rect)
        screen.blit(home_text, home_rect)
        
        pygame.display.flip()
        clock.tick(60)