class Player:
    def __init__(self, player_num, color, home_planet, settings):
        self.player_num = player_num
        self.color = color
        self.home_planet = home_planet
        self.target_planet = home_planet
        self.settings = settings
        self.ship_count = 0
        self.difficulty = 'Hard'
        self.prev_target = home_planet
        
    def change_target(self, new_planet):
        self.target_planet = new_planet

    def change_difficulty(self, new_difficulty):
        self.difficulty = new_difficulty
        
    def change_setting(self, new_setting):
        self.settings = new_setting
        
    def change_home(self, new_home):
        self.home_planet = new_home
        
    def update_shipcount(self, update):
        self.ship_count += update