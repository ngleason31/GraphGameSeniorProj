import pygame
import GlobalSettings

class Scoreboard:
    def __init__(self, player1, player2):
        self.player_score = 1000
        self.player1 = player1
        self.player2 = player2
        self.player_sps = 0
        self.opponent_sps = 0
        self.opponent_score = 1000
        self.player1_shipcount = 0
        self.player2_shipcount = 0
        self.font = pygame.font.Font(None, 36)
        
    def update(self):
        self.player_score += self.player_sps
        self.opponent_score += self.opponent_sps
        
    def update_player(self, change):
        self.player_score += change
        
    def update_opponent(self, change):
        self.opponent_score += change
        
    def get_scores(self):
        return [self.player_score, self.opponent_score]
        
    def update_player_sps(self, sps):
        self.player_sps += sps
        
    def update_opponent_sps(self, sps):
        self.opponent_sps += sps
        
    def draw(self, surface):
        player_text = self.font.render(f"Player Score: {self.player_score}", True, GlobalSettings.neutral_color)
        surface.blit(player_text, (50, 5))
        
        shipcount_text1 = self.font.render(f"Ship Count: {self.player1.ship_count}/{GlobalSettings.ship_limit}", True, GlobalSettings.neutral_color)
        surface.blit(shipcount_text1, (50, 50))
            
        opponent_text = self.font.render(f"Opponent Score: {self.opponent_score}", True, GlobalSettings.neutral_color)
        surface.blit(opponent_text, (GlobalSettings.WIDTH - 300, 5))
        
        shipcount_text2 = self.font.render(f"Ship Count: {self.player2.ship_count}/{GlobalSettings.ship_limit}", True, GlobalSettings.neutral_color)
        surface.blit(shipcount_text2, (GlobalSettings.WIDTH - 300, 50))