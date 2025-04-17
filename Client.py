import socket
import pickle
import pygame
from Shop import Shop
from Planet import planet_loc, Planet
from Ship import Ship
import GlobalSettings

def client(screen, player1, player2, server_ip):
    HOST = server_ip 
    PORT = 5555

    pygame.init()
    clock = pygame.time.Clock()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.connect((HOST, PORT))
    try:
        client_socket.connect((HOST, PORT))
    except Exception as e:
        print("[CLIENT] Unable to connect to server:", e)
        return "quit"
    

    running = True
    shop = Shop(triangle_color=GlobalSettings.blue)
    clicked_planet = None
    draw_planets = []  # Initial empty list for planets (will be updated from game state)

    while running:
        pygame.event.pump()
        input_data = {}
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos

        planets = []
        ships = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if shop.is_clicked(mouse_pos):
                        input_data = {
                            "type": "buy_ship"
                        }
                if event.button == 3:
                    if clicked_planet:
                        clicked_planet.selected = False
                        clicked_planet = planet_loc(mouse_x, mouse_y, planets)
                    if clicked_planet:
                        player2.target_planet = clicked_planet.id
                        clicked_planet.selected = True
                        input_data = {
                            "type": "select_planet",
                            "planet_id": clicked_planet.id
                        }

        try:
            client_socket.sendall(pickle.dumps(input_data))
            data = b""
            while True:
                part = client_socket.recv(8192)
                data += part
                if len(part) < 8192:
                    break
            game_state_dict = pickle.loads(data)
            planets = game_state_dict["planets"]
            ships = game_state_dict["ships"]
            #scoreboard = game_state_dict["scoreboard"]

            # DRAW game_state
            screen.fill(GlobalSettings.light_mode_bg if not GlobalSettings.dark_background else GlobalSettings.dark_mode_bg)

            for planet_dict in planets:
                draw_planets.append(Planet.deserialize(planet_dict))
            for ship_dict in ships:
                ship = Ship.deserialize(ship_dict)
                ship.draw(screen)
                
            for planet in draw_planets:
                planet.draw(screen, draw_planets)
            #scoreboard.draw(screen)
            shop.is_hovered(mouse_pos)
            shop.draw(screen)
            

            pygame.display.flip()
            clock.tick(60)
        except Exception as e:
            print("[CLIENT] Disconnected from server:", e)
            return 'quit'

    pygame.quit()
    client_socket.close()
