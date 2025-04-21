from collections import deque
class Player:
    def __init__(self, player_num, color, home_planet, settings):
        '''
        Initializes the player object with the parameters.
        '''
        
        self.player_num = player_num
        self.color = color
        self.home_planet = home_planet
        self.target_planet = home_planet
        self.settings = settings
        self.ship_count = 0
        self.prev_target = home_planet
        
        # Initializes to hard, so that players move the fastest.
        self.difficulty = 'Hard'
        
        # Helper deques for the AI.
        self.bfs = deque()
        self.dfs = deque()
        
    def change_target(self, new_planet):
        '''
        Changes the target planet for the player.
        '''
        
        self.target_planet = new_planet

    def change_difficulty(self, new_difficulty):
        '''
        Changes the difficulty of the player.
        '''
        
        self.difficulty = new_difficulty
        
    def change_setting(self, new_setting):
        '''
        Changes the settings of the player.
        '''
        
        self.settings = new_setting
        
    def change_home(self, new_home):
        '''
        Changes the home planet of the player (not currently used, maybe in the future?).
        '''
        
        self.home_planet = new_home
        
    def update_shipcount(self, update):
        '''
        Updates the ship count for the player.
        '''
        
        self.ship_count += update