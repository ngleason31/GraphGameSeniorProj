import socket
import pickle
import pygame
from GameState import GameState
import GlobalSettings

HOST = 'SERVER_IP_HERE'
PORT = 5555

pygame.init()
screen = pygame.display.set_mode((GlobalSettings.WIDTH, GlobalSettings.HEIGHT))
clock = pygame.time.Clock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

running = True

while running:
    pygame.event.pump()
    input_data = {}

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            input_data = {
                "type": "click",
                "button": event.button,
                "pos": pygame.mouse.get_pos()
            }
        elif event.type == pygame.KEYDOWN:
            input_data = {
                "type": "key",
                "key": event.key
            }

    try:
        client.sendall(pickle.dumps(input_data))
        data = b""
        while True:
            part = client.recv(8192)
            data += part
            if len(part) < 8192:
                break
        game_state_dict = pickle.loads(data)
        game_state = GameState.from_dict(game_state_dict)

        # DRAW game_state
        screen.fill(GlobalSettings.light_mode_bg if not GlobalSettings.dark_background else GlobalSettings.dark_mode_bg)

        for planet in game_state.planets:
            planet.draw(screen, game_state.planets)
        for ship in game_state.ships:
            ship.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    except Exception as e:
        print("[CLIENT] Disconnected from server:", e)
        running = False

pygame.quit()
client.close()
