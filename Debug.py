import pygame
from Ship import Ship
import GlobalSettings
import random

class DebugConsole:
    def __init__(self):
        '''
        A console for debug commands.
        '''
        
        self.rect = pygame.Rect(0, GlobalSettings.HEIGHT - 200, GlobalSettings.WIDTH, 50)
        self.font = pygame.font.SysFont(None, 48)
        self.input_text = ""
        self.active = False

    def toggle(self):
        '''
        Toggles the console on and off.
        '''
        
        self.active = not self.active

    def handle_typing(self, event, player1, player2, planets, ships):
        '''
        Handles typing in the console.
        '''
        
        if not self.active:
            return None

        # Handle key events and executes the command.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                cmd = self.input_text.strip()
                self.input_text = ""
                if cmd:
                    cmd = cmd.split()
                    self.execute(cmd, player1, player2, planets, ships)
            else:
                # Adds the character to the input text.
                if event.unicode.isprintable():
                    self.input_text += event.unicode

    def execute(self, cmd, player1, player2, planets, ships):
        '''
        Executes the command based on the input.
        '''
        
        # Command to add ships.
        if cmd[0].lower() == 'addships':
            # Adds ships to player 1.
            if cmd[1].lower() == '1':
                n = int(cmd[2])
                if n + player1.ship_count > GlobalSettings.ship_limit:
                    n = GlobalSettings.ship_limit - player1.ship_count
                player1.ship_count += n
                for _ in range(n):
                    x_offset = random.randint(-planets[0].radius + 15, planets[0].radius - 15)
                    y_offset = random.randint(-planets[0].radius + 15, planets[0].radius - 15)
                    x = planets[0].x + x_offset
                    y = planets[0].y + y_offset
                    ships.append(Ship(x, y, 0, player=1))
            if cmd[1].lower() == '2':
                # Adds ships to player 2.
                n = int(cmd[2])
                if n + player1.ship_count > GlobalSettings.ship_limit:
                    n = GlobalSettings.ship_limit - player2.ship_count
                player2.ship_count += n
                for _ in range(n):
                    x_offset = random.randint(-planets[1].radius + 15, planets[1].radius - 15)
                    y_offset = random.randint(-planets[1].radius + 15, planets[1].radius - 15)
                    x = planets[1].x + x_offset
                    y = planets[1].y + y_offset
                    ships.append(Ship(x, y, 1, player=2))
                  
        # Command to force wins.  
        elif cmd[0].lower() == 'forcewin':
            if cmd[1].lower() == '1':
                planets[1].player_num = 1
            elif cmd[1].lower() == '2':
                planets[0].player_num = 2
                
    def draw(self, surface):
        '''
        Draws the console on the given surface.
        '''
        
        if not self.active:
            return

        # Semi Transparent background.
        bg = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        bg.fill((0, 0, 0, 180))
        surface.blit(bg, self.rect.topleft)

        # Draw input prompt.
        prompt = "> " + self.input_text
        txt_surf = self.font.render(prompt, True, (255, 255, 255))
        surface.blit(txt_surf, (self.rect.left + 5, self.rect.bottom - self.font.get_linesize() - 5))