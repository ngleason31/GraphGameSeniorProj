import pygame
import GlobalSettings

class Shop:
    def __init__(self):
        self.rect = pygame.Rect(GlobalSettings.WIDTH / 2 - 25, 30, 50, 50)
        self.color = (140, 140, 140)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        triangle_points = [
            (self.rect.centerx, self.rect.y + 15),
            (self.rect.x + 15, self.rect.bottom - 15),
            (self.rect.right - 15, self.rect.bottom - 15)
        ]
        pygame.draw.polygon(screen, GlobalSettings.player_colors[GlobalSettings.curr_player], triangle_points, width=4)
        
        font = pygame.font.Font(None, 20)
        text_surface = font.render("50", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery + 15))
        screen.blit(text_surface, text_rect)
        
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.color = (160, 160, 160)
        else:
            self.color = (140, 140, 140)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
        