import pygame
import GlobalSettings

class Shop:
    def __init__(self):
        self.rect = pygame.Rect(GlobalSettings.WIDTH / 2 - 25, 30, 50, 50)
        self.color = GlobalSettings.gray
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        triangle_points = [
            (self.rect.centerx, self.rect.y + 20),
            (self.rect.x + 15, self.rect.bottom - 10),
            (self.rect.right - 15, self.rect.bottom - 10)
        ]
        pygame.draw.polygon(screen, GlobalSettings.player_colors[GlobalSettings.curr_player], triangle_points, width=4)
        
        font = pygame.font.Font(None, 25)
        text_surface = font.render("50", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 15))
        screen.blit(text_surface, text_rect)
    
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.color = GlobalSettings.black
        else:
            self.color = GlobalSettings.gray

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
        