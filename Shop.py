import pygame
import GlobalSettings

class Shop:
    def __init__(self, triangle_color=GlobalSettings.orange):
        '''
        Initializes the shop with a rectangle and a triangle.
        '''
        
        self.rect = pygame.Rect(GlobalSettings.WIDTH / 2 - 25, 30, 50, 50)
        self.color = GlobalSettings.gray
        self.triangle_color = triangle_color
        
    def draw(self, screen):
        '''
        Draws the shop on the given screen.
        '''
        
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Calculates the triangle points.
        triangle_points = [
            (self.rect.centerx, self.rect.y + 20),
            (self.rect.x + 15, self.rect.bottom - 10),
            (self.rect.right - 15, self.rect.bottom - 10)
        ]
        pygame.draw.polygon(screen, self.triangle_color, triangle_points, width=4)
        
        # Draws the price text.
        font = pygame.font.Font(None, 25)
        text_surface = font.render(f"{GlobalSettings.ship_price}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 15))
        screen.blit(text_surface, text_rect)
    
    def is_hovered(self, pos):
        '''
        Changes the color of the shop when hovered.
        '''
        
        if self.rect.collidepoint(pos):
            self.color = GlobalSettings.black
        else:
            self.color = GlobalSettings.gray

    def is_clicked(self, pos):
        '''
        Returns True if the shop is clicked.
        '''
        
        return self.rect.collidepoint(pos)
        
        