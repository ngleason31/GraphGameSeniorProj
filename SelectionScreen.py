import pygame
import GlobalSettings

def selection_screen(screen, width, height, mode):
    clock = pygame.time.Clock()
    FPS = 60


    # Preload font
    font = pygame.font.Font(None, 36)
    
    #Button definitions
    return_button_rect = pygame.Rect(width // 2 - 300, height - 200, 200, 50)
    continue_button_rect = pygame.Rect(width // 2 + 100, height - 200, 200, 50)
    
    #Selection definitions
    player1_rect = pygame.Rect(width // 2 - 600, 200, 400, 100)
    player1_box = pygame.Rect(width // 2 - 560, 215, 70, 70)
    player2_rect = pygame.Rect(width // 2 + 200, 200, 400, 100)
    player2_box = pygame.Rect(width // 2 + 490, 215, 70, 70)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return "home"
                
            #Handle button presses
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if return_button_rect.collidepoint(mouse):
                        return 'home'
                
                if continue_button_rect.collidepoint(mouse):
                        return 'game'
                    
            # Use the global background setting for the color.
            if GlobalSettings.dark_background:
                bg_color = GlobalSettings.dark_mode_bg
            else:
                bg_color = GlobalSettings.light_mode_bg
            screen.fill(bg_color)
            
            #Draws the buttons
            mouse = pygame.mouse.get_pos()
            if return_button_rect.collidepoint(mouse):
                pygame.draw.rect(screen, GlobalSettings.black, return_button_rect)
            else:
                pygame.draw.rect(screen, GlobalSettings.gray, return_button_rect)

            if continue_button_rect.collidepoint(mouse):
                pygame.draw.rect(screen, GlobalSettings.black, continue_button_rect)
            else:
                pygame.draw.rect(screen, GlobalSettings.gray, continue_button_rect)
                
            #Draw selction sides
            pygame.draw.rect(screen, GlobalSettings.gray, player1_rect)
            pygame.draw.rect(screen, bg_color, player1_box)
            triangle_points = [
                (player1_box.centerx, player1_box.y + 15),
                (player1_box.x + 15, player1_box.bottom - 15),
                (player1_box.right - 15, player1_box.bottom - 15)
            ]
            pygame.draw.polygon(screen, GlobalSettings.player_colors[1], triangle_points, width=4)
            
            pygame.draw.rect(screen, GlobalSettings.gray, player2_rect)
            pygame.draw.rect(screen, bg_color, player2_box)
            triangle_points = [
                (player2_box.centerx, player2_box.y + 15),
                (player2_box.x + 15, player2_box.bottom - 15),
                (player2_box.right - 15, player2_box.bottom - 15)
            ]
            pygame.draw.polygon(screen, GlobalSettings.player_colors[2], triangle_points, width=4)
            
            if mode.lower() == 'single player':
                player_surface = font.render("Player 1", True, (255, 255, 255))
                player_rect = player_surface.get_rect(center=player1_rect.center)
                screen.blit(player_surface, player_rect)
                
                computer_surface = font.render("Computer", True, (255, 255, 255))
                computer_rect = computer_surface.get_rect(center=player2_rect.center)
                screen.blit(computer_surface, computer_rect)
                
            if mode.lower() == 'multiplayer':
                player1_text_surface = font.render("Player 1", True, (255, 255, 255))
                player1_text_rect = player1_text_surface.get_rect(center=player1_rect.center)
                screen.blit(player1_text_surface, player1_text_rect)
                
                player2_text_surface = font.render("Player 2", True, (255, 255, 255))
                player2_text_rect = player1_text_surface.get_rect(center=player2_rect.center)
                screen.blit(player2_text_surface, player2_text_rect)
                
            if mode.lower() == 'computer':
                computer1_surface = font.render("Computer", True, (255, 255, 255))
                computer1_rect = computer1_surface.get_rect(center=player1_rect.center)
                screen.blit(computer1_surface, computer1_rect)
                
                computer2_surface = font.render("Computer", True, (255, 255, 255))
                computer2_rect = computer2_surface.get_rect(center=player2_rect.center)
                screen.blit(computer2_surface, computer2_rect)
                
                
            # Draw Return to Home button
            return_surface = font.render("Return to Home", True, (255, 255, 255))
            return_rect = return_surface.get_rect(center=return_button_rect.center)
            screen.blit(return_surface, return_rect)
            
            # Draw Return to Home button
            continue_surface = font.render("Play Game", True, (255, 255, 255))
            continue_rect = continue_surface.get_rect(center=continue_button_rect.center)
            screen.blit(continue_surface, continue_rect)

            pygame.display.flip()
            clock.tick(FPS)

    return "game"