import pygame
import GlobalSettings

class Scoreboard:
    def __init__(self):
        self.player_score = 50
        self.player_sps = 0
        self.opponent_sps = 50
        self.opponent_score = 0
        self.font = pygame.font.Font(None, 36)
        
    def update(self):
        self.player_score += self.player_sps
        self.opponent_score += self.opponent_sps
        
    def update_player(self, change):
        self.player_score += change
        
    def update_opponent(self, change):
        self.opponent_score += change
        
    def update_player_sps(self, sps):
        self.player_sps += sps
        
    def update_opponent_sps(self, sps):
        self.opponent_sps += sps
        
    def draw(self, surface):
        player_text = self.font.render(f"Player Score: {self.player_score}", True, GlobalSettings.neutral_color)
        surface.blit(player_text, (50, 5))
            
        opponent_text = self.font.render(f"Opponent Score: {self.opponent_score}", True, GlobalSettings.neutral_color)
        surface.blit(opponent_text, (GlobalSettings.WIDTH - 300, 5))