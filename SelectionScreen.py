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