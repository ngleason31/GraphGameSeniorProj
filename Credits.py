import pygame
import sys
import GlobalSettings

def runCredits(screen, WIDTH, HEIGHT):
    # Set up a screen for the credits. Adjust WIDTH/HEIGHT as needed.
    pygame.display.set_caption("Credits")
    
    clock = pygame.time.Clock()
    FPS = 60

    # Define the credits text lines.
    credits = [
        "   DEVELOPERS:",
        "   Caleb Everett",
        "   Nico Gleason",
        "",
        "ADVISOR:",
        "   Peter Dobbins",
        "",
        "SPECIAL THANKS:",
        "   University of Florida for a great last 4 years!",
        "",
        "GO GATORS!"
    ]

    # Start drawing credits below the screen.
    y_offset = HEIGHT
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" 

        if GlobalSettings.dark_background:
            bg_color = GlobalSettings.dark_mode_bg
            text_color = GlobalSettings.dark_mode_details
        else:
            bg_color = GlobalSettings.light_mode_bg
            text_color = GlobalSettings.light_mode_details
        screen.fill(bg_color)

        # Render and draw each line of the credits.
        for index, line in enumerate(credits):
            font = pygame.font.Font(None, 36)
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset + index * 40))
            screen.blit(text_surface, text_rect)

        # Scroll the credits upward.
        y_offset -= 0.5  
        pygame.display.flip()
        clock.tick(FPS)

        # End credits when all text has scrolled off the top.
        if y_offset + len(credits) * 40 < 0:
            running = False

    button_rect = pygame.Rect(WIDTH // 2 - 110 , HEIGHT // 2 - 50, 230, 50)
    button_font = pygame.font.Font(None, 36)
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        
        if GlobalSettings.dark_background:
            bg_color = GlobalSettings.dark_mode_bg
        else:
            bg_color = GlobalSettings.light_mode_bg
        screen.fill(bg_color)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, (100, 100, 100), button_rect)
            if click[0] == 1:
                waiting = False 
        else:
            pygame.draw.rect(screen, (150, 150, 150), button_rect)
        
        button_text = button_font.render("Return to Home", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return "home"

if __name__ == "__main__":
    runCredits()

