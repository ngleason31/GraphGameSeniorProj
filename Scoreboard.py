import pygame
import GlobalSettings

class Scoreboard:
    def __init__(self):
        '''
        Initializes the scoreboard with default values (sets initial scores to 1000 to get players started).
        '''
        self.player_score = 1000
        self.player_sps = 0
        self.opponent_sps = 0
        self.opponent_score = 1000
        self.player1_shipcount = 0
        self.player2_shipcount = 0
        self.font = pygame.font.Font(None, 36)
        self.player1_shipcount = 0
        self.player2_shipcount = 0
        
    def update(self):
        '''
        Updates the scores based on the score per second (sps) of each player.
        '''
        
        self.player_score += self.player_sps
        self.opponent_score += self.opponent_sps
        
    def update_player(self, change):
        '''
        Updates the player score by the given change.
        '''
        
        self.player_score += change
        
    def update_opponent(self, change):
        '''
        Updates the opponent score by the given change.
        '''
        
        self.opponent_score += change
        
    def get_scores(self):
        '''
        Returns the current scores of both players.
        '''
        
        return [self.player_score, self.opponent_score]
        
    def update_player_sps(self, sps):
        '''
        Updates the player score per second (sps) by the given value.
        '''
        
        self.player_sps += sps
        
    def update_opponent_sps(self, sps):
        '''
        Updates the opponent score per second (sps) by the given value.
        '''
        
        self.opponent_sps += sps
    
    def update_shipcount(self, player1, player2):
        '''
        Updates the ship count for both players.
        '''
        
        self.player1_shipcount = player1.ship_count
        self.player2_shipcount = player2.ship_count
        
    def draw(self, surface):
        '''
        Draws the scoreboard on the given surface.
        '''
        
        #Draws the player 1 score and ship count.
        player_text = self.font.render(f"Player 1 Score: {self.player_score}", True, GlobalSettings.neutral_color)
        surface.blit(player_text, (50, 5))
        
        shipcount_text1 = self.font.render(f"Ship Count: {self.player1_shipcount}/{GlobalSettings.ship_limit}", True, GlobalSettings.neutral_color)
        surface.blit(shipcount_text1, (50, 50))
        
        #Draws the player 2 score and ship count.
        opponent_text = self.font.render(f"Player 2 Score: {self.opponent_score}", True, GlobalSettings.neutral_color)
        surface.blit(opponent_text, (GlobalSettings.WIDTH - 300, 5))
        
        shipcount_text2 = self.font.render(f"Ship Count: {self.player2_shipcount}/{GlobalSettings.ship_limit}", True, GlobalSettings.neutral_color)
        surface.blit(shipcount_text2, (GlobalSettings.WIDTH - 300, 50))
    
    def serialize(self):
        '''
        Serializes the scoreboard data to a dictionary for sending over the network.
        '''

        return {
            'player_score': self.player_score,
            'opponent_score': self.opponent_score,
            'player1_shipcount': self.player1_shipcount,
            'player2_shipcount': self.player2_shipcount,
        }
        
    @staticmethod
    def deserialize(data):
        '''
        Deserializes the scoreboard data from a dictionary received over the network.
        '''
        
        scoreboard = Scoreboard()
        scoreboard.player_score = data['player_score']
        scoreboard.opponent_score = data['opponent_score']
        scoreboard.player1_shipcount = data['player1_shipcount']
        scoreboard.player2_shipcount = data['player2_shipcount']
        return scoreboard