import pygame
import sys
import GlobalSettings

def runSettings(screen, WIDTH, HEIGHT):
    '''
    Runs the settings menu for the game.
    '''
    
    clock = pygame.time.Clock()
    FPS = 60

    # Button definitions.
    audio_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 - 50, 220, 50)
    bg_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 + 20, 220, 50)
    return_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 200, 200, 50)

    # Volume slider.
    volume_slider_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 + 120, 220, 10)
    slider_handle_radius = 10
    dragging_slider = False

    # Hidden easter egg area (e.g., lower-right corner, small invisible area).
    easter_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 50, 50)
    easter_clicks = 0
    easter_triggered = False

    # Preload font.
    font = pygame.font.Font(None, 36)

    running = True
    while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # Toggle Audio: update global variable.
                    if audio_button_rect.collidepoint(mouse):
                        GlobalSettings.audio_on = not GlobalSettings.audio_on
                        GlobalSettings.update_audio()
                    # Toggle Background: update global variable.
                    if bg_button_rect.collidepoint(mouse):
                        GlobalSettings.dark_background = not GlobalSettings.dark_background
                        GlobalSettings.reload_player_colors()
                    # Return to home if return button is clicked.
                    if return_button_rect.collidepoint(mouse):
                        running = False
                    # Hidden Easter Egg click.
                    if easter_rect.collidepoint(mouse):
                        easter_clicks += 1
                        if easter_clicks >= 5:
                            easter_triggered = True

                    # Begin dragging the volume slider if clicked on the slider bar.
                    if volume_slider_rect.collidepoint(mouse):
                        dragging_slider = True

                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_slider = False

                if event.type == pygame.MOUSEMOTION and dragging_slider:
                    mouse_x = event.pos[0]
                    # Calculate new volume based on mouse x-position relative to the slider bar.
                    relative_x = mouse_x - volume_slider_rect.x
                    new_volume = relative_x / volume_slider_rect.width
                    new_volume = max(0, min(new_volume, 1))  # Clamp between 0 and 1.
                    GlobalSettings.volume = new_volume
                    # Update the volume of the music.
                    pygame.mixer.music.set_volume(new_volume)
                    GlobalSettings.update_audio

            # Use the global background setting for the color.
            if GlobalSettings.dark_background:
                bg_color = GlobalSettings.dark_mode_bg
            else:
                bg_color = GlobalSettings.light_mode_bg
            screen.fill(bg_color)

            # Change Color on Hover.
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

            # Draw Audio toggle button.
            audio_text = "Audio: On" if GlobalSettings.audio_on else "Audio: Off"
            audio_surface = font.render(audio_text, True, (255, 255, 255))
            audio_rect = audio_surface.get_rect(center=audio_button_rect.center)
            screen.blit(audio_surface, audio_rect)

            # Draw Background toggle button.
            bg_text = "Background: Dark" if GlobalSettings.dark_background else "Background: Light"
            bg_surface = font.render(bg_text, True, (255, 255, 255))
            bg_rect = bg_surface.get_rect(center=bg_button_rect.center)
            screen.blit(bg_surface, bg_rect)

            # Draw Volume Slider Bar.
            pygame.draw.rect(screen, GlobalSettings.gray, volume_slider_rect)
            
            # Calculate the handle position based on the current volume.
            handle_x = volume_slider_rect.x + int(GlobalSettings.volume * volume_slider_rect.width)
            handle_y = volume_slider_rect.centery
            
            # Draw the slider handle; you can choose a fixed color or add a hover effect here if desired.
            pygame.draw.circle(screen, GlobalSettings.black if volume_slider_rect.collidepoint(mouse) else GlobalSettings.gray, (handle_x, handle_y), slider_handle_radius)
            
            # Display the volume percentage above the slider bar.
            vol_percentage = int(GlobalSettings.volume * 100)
            vol_text = f"Volume: {vol_percentage}%"
            vol_surface = font.render(vol_text, True, (255, 255, 255))
            vol_rect = vol_surface.get_rect(midbottom=(volume_slider_rect.centerx, volume_slider_rect.y - 10))
            screen.blit(vol_surface, vol_rect)

            # Draw Return to Home button.
            return_surface = font.render("Return to Home", True, (255, 255, 255))
            return_rect = return_surface.get_rect(center=return_button_rect.center)
            screen.blit(return_surface, return_rect)

            # If the easter egg has been triggered, display the secret message.
            if easter_triggered:
                # Display secret text.
                secret_text = font.render("Go Gators! :)", True, (0, 0, 0))
                secret_rect = secret_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(secret_text, secret_rect)

            pygame.display.flip()
            clock.tick(FPS)

    return "home"