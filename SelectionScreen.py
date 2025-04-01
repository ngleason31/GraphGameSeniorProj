import pygame
import GlobalSettings

# A class to handle dropdown menus
class Dropdown:
    def __init__(self, x, y, width, height, options, title, font):
        self.title = title
        self.title_rect = pygame.Rect(x, y, width, height)
        self.rect = pygame.Rect(x, y + height + 5, width, height)
        self.options = options
        self.selected_index = 0
        self.expanded = False
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, GlobalSettings.gray, self.title_rect)
        
        title_surface = self.font.render(self.title, True, GlobalSettings.white)
        title_rect_final = title_surface.get_rect(center=self.title_rect.center)
        screen.blit(title_surface, title_rect_final)
        
        pygame.draw.rect(screen, GlobalSettings.gray, self.rect)
        pygame.draw.rect(screen, GlobalSettings.neutral_color, self.rect, width=4)

        selection_surface = self.font.render(self.options[self.selected_index], True, GlobalSettings.white)
        selection_rect_final = selection_surface.get_rect(center=self.rect.center)
        screen.blit(selection_surface, selection_rect_final)

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                pygame.draw.rect(screen, GlobalSettings.gray, option_rect)
                
                option_surface = self.font.render(option, True, GlobalSettings.white)
                option_rect_final = option_surface.get_rect(center=option_rect.center)
                screen.blit(option_surface, option_rect_final)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
            elif self.expanded:
                for i in range(len(self.options)):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if option_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.expanded = False
                        
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
    
    cpu_options = ['Best Move First', 'Worst Move First', 'Highest Scoring First', 'Lowest Scoring First', 'DFS', 'BFS']
    difficulty_options = ['Easy', 'Medium', 'Hard']
    
    dropdown_menu1 = Dropdown(width // 2 - 600, 350, 400, 50, cpu_options, "Select settings for Computer 1:", font)
    dropdown_menu2 = Dropdown(width // 2 + 200, 350, 400, 50, cpu_options, "Select settings for Computer 2:", font)
    
    difficulty_menu1 = Dropdown(width // 2 - 600, 500, 400, 50, difficulty_options, "Select difficulty", font)
    difficulty_menu2 = Dropdown(width // 2 + 200, 500, 400, 50, difficulty_options, "Select difficulty", font)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return ["home", None, None]
                
            #Handle button presses
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if return_button_rect.collidepoint(mouse):
                        return ['home', None, None]
                
                if continue_button_rect.collidepoint(mouse):
                        if mode.lower() == 'single player':
                            return ['game', None, dropdown_menu2.options[dropdown_menu2.selected_index]]
                        if mode.lower() == 'computer':
                            return ['game', dropdown_menu1.options[dropdown_menu1.selected_index], dropdown_menu2.options[dropdown_menu2.selected_index]]
                        else:
                            return ['game', None, None]
                                    
                    
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
                
                computer_surface = font.render("Computer 2", True, (255, 255, 255))
                computer_rect = computer_surface.get_rect(center=player2_rect.center)
                screen.blit(computer_surface, computer_rect)
                
                dropdown_menu2.handle_event(event)
                dropdown_menu2.draw(screen)
                
                difficulty_menu2.handle_event(event)
                GlobalSettings.computer2_difficulty = difficulty_menu2.options[difficulty_menu2.selected_index]
                difficulty_menu2.draw(screen)
                
            if mode.lower() == 'multiplayer':
                player1_text_surface = font.render("Player 1", True, (255, 255, 255))
                player1_text_rect = player1_text_surface.get_rect(center=player1_rect.center)
                screen.blit(player1_text_surface, player1_text_rect)
                
                player2_text_surface = font.render("Player 2", True, (255, 255, 255))
                player2_text_rect = player1_text_surface.get_rect(center=player2_rect.center)
                screen.blit(player2_text_surface, player2_text_rect)
                
            if mode.lower() == 'computer':
                computer1_surface = font.render("Computer 1", True, (255, 255, 255))
                computer1_rect = computer1_surface.get_rect(center=player1_rect.center)
                screen.blit(computer1_surface, computer1_rect)
                
                computer2_surface = font.render("Computer 2", True, (255, 255, 255))
                computer2_rect = computer2_surface.get_rect(center=player2_rect.center)
                screen.blit(computer2_surface, computer2_rect)
                
                dropdown_menu1.handle_event(event)
                dropdown_menu1.draw(screen)
                
                difficulty_menu1.handle_event(event)
                GlobalSettings.computer1_difficulty = difficulty_menu1.options[difficulty_menu1.selected_index]
                difficulty_menu1.draw(screen)
                
                dropdown_menu2.handle_event(event)
                dropdown_menu2.draw(screen)
                
                difficulty_menu2.handle_event(event)
                GlobalSettings.computer2_difficulty = difficulty_menu2.options[difficulty_menu2.selected_index]
                difficulty_menu2.draw(screen)
                
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