import pygame
import GlobalSettings

class Scoreboard:
    def __init__(self):
        self.player_score = 50
        self.opponent_score = 50
        self.font = pygame.font.Font(None, 36)
        
    def update(self):
        self.update_player()
        self.update_opponent()
        
    def update_player(self, change=5):
        self.player_score += change
            
    def update_opponent(self, change=5):
        self.opponent_score += change
        
    def draw(self, surface):
        player_text = self.font.render(f"Player Score: {self.player_score}", True, GlobalSettings.neutral_color)
        surface.blit(player_text, (50, 5))
            
        opponent_text = self.font.render(f"Opponent Score: {self.opponent_score}", True, GlobalSettings.neutral_color)
        surface.blit(opponent_text, (GlobalSettings.WIDTH - 300, 5))