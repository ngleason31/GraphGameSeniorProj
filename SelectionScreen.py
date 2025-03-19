import pygame

def selection_screen(screen, width, height, mode):
    pygame.init()
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    running = True
    dropdown_options = ["Easy", "Medium", "Hard"]
    selected_option = dropdown_options[0]  # Default selection
    dropdown_open = False
    
    while running:
        screen.fill((30, 30, 30))  # Dark background
        
        if mode == "multiplayer":
            # Display Player 1 and Player 2
            player1_text = font.render("Player 1", True, (255, 255, 255))
            player2_text = font.render("Player 2", True, (255, 255, 255))
            screen.blit(player1_text, (width // 4 - player1_text.get_width() // 2, height // 2))
            screen.blit(player2_text, (3 * width // 4 - player2_text.get_width() // 2, height // 2))
        
        elif mode == "computer":
            # Dropdown menu
            menu_x, menu_y = width // 2 - 50, height // 2
            menu_width, menu_height = 100, 30
            pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_width, menu_height))
            option_text = font.render(selected_option, True, (255, 255, 255))
            screen.blit(option_text, (menu_x + 10, menu_y + 5))
            
            if dropdown_open:
                for i, option in enumerate(dropdown_options):
                    pygame.draw.rect(screen, (80, 80, 80), (menu_x, menu_y + (i + 1) * menu_height, menu_width, menu_height))
                    option_text = font.render(option, True, (255, 255, 255))
                    screen.blit(option_text, (menu_x + 10, menu_y + (i + 1) * menu_height + 5))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if mode == "computer" and menu_x <= x <= menu_x + menu_width:
                    if menu_y <= y <= menu_y + menu_height:
                        dropdown_open = not dropdown_open
                    elif dropdown_open:
                        for i, option in enumerate(dropdown_options):
                            if menu_y + (i + 1) * menu_height <= y <= menu_y + (i + 2) * menu_height:
                                selected_option = option
                                dropdown_open = False
        
        pygame.display.flip()
        clock.tick(30)