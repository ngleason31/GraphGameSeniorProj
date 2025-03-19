import pygame
import sys
import GlobalSettings

def runSettings(screen, WIDTH, HEIGHT):
    # Get display dimensions
    pygame.display.set_caption("Settings")
    clock = pygame.time.Clock()
    FPS = 60

    # Initial settings state
    # darkBackground = True

    # Button definitions
    audio_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 - 50, 220, 50)
    bg_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 + 20, 220, 50)
    return_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 200, 200, 50)

    # Hidden easter egg area (e.g., lower-right corner, small invisible area)
    easter_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 50, 50)
    easter_clicks = 0
    easter_triggered = False

    # Preload font
    font = pygame.font.Font(None, 36)

    running = True
    while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # Toggle Audio: update global variable
                    if audio_button_rect.collidepoint(mouse):
                        GlobalSettings.audio_on = not GlobalSettings.audio_on
                        GlobalSettings.update_audio()
                    # Toggle Background: update global variable
                    if bg_button_rect.collidepoint(mouse):
                        GlobalSettings.dark_background = not GlobalSettings.dark_background
                        GlobalSettings.reload_player_colors()
                    # Return to home if return button is clicked
                    if return_button_rect.collidepoint(mouse):
                        running = False
                    # Hidden Easter Egg click
                    if easter_rect.collidepoint(mouse):
                        easter_clicks += 1
                        if easter_clicks >= 5:
                            easter_triggered = True

            # Use the global background setting for the color.
            if GlobalSettings.dark_background:
                bg_color = GlobalSettings.dark_mode_bg
            else:
                bg_color = GlobalSettings.light_mode_bg
            screen.fill(bg_color)

            #Change Color on Hover
            mouse = pygame.mouse.get_pos()
            if audio_button_rect.collidepoint(mouse):
                pygame.draw.rect(screen, GlobalSettings.black, audio_button_rect)
            else:
                pygame.draw.rect(screen, GlobalSettings.gray, audio_button_rect)

            if bg_button_rect.collidepoint(mouse):
                pygame.draw.rect(screen, GlobalSettings.black, bg_button_rect)
            else:
                pygame.draw.rect(screen, GlobalSettings.gray, bg_button_rect)

            if return_button_rect.collidepoint(mouse):
                pygame.draw.rect(screen, GlobalSettings.black, return_button_rect)
            else:
                pygame.draw.rect(screen, GlobalSettings.gray, return_button_rect)

            # Draw Audio toggle button
            audio_text = "Audio: On" if GlobalSettings.audio_on else "Audio: Off"
            audio_surface = font.render(audio_text, True, (255, 255, 255))
            audio_rect = audio_surface.get_rect(center=audio_button_rect.center)
            screen.blit(audio_surface, audio_rect)

            # Draw Background toggle button
            bg_text = "Background: Dark" if GlobalSettings.dark_background else "Background: Light"
            bg_surface = font.render(bg_text, True, (255, 255, 255))
            bg_rect = bg_surface.get_rect(center=bg_button_rect.center)
            screen.blit(bg_surface, bg_rect)

            # Draw Return to Home button
            return_surface = font.render("Return to Home", True, (255, 255, 255))
            return_rect = return_surface.get_rect(center=return_button_rect.center)
            screen.blit(return_surface, return_rect)

            #pygame.draw.rect(screen, (0, 255, 0), easter_rect, 1)

            # If the easter egg has been triggered, display the secret message
            if easter_triggered:
                # Display secret text
                secret_text = font.render("Go Gators! :)", True, (0, 0, 0))
                secret_rect = secret_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(secret_text, secret_rect)

            pygame.display.flip()
            clock.tick(FPS)

    return "home"