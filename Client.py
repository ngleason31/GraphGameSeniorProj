import socket
import pygame
from Shop import Shop
from Planet import planet_loc, Planet
from Player import Player
from Scoreboard import Scoreboard
from Ship import Ship
import GlobalSettings
from NetworkUtils import send_msg, recv_msg
from Game import winnerScreen

def client(screen, player1, player2, server_ip):
    '''
    Handles the client side of the game during multiplayer mode.
    '''
    
    # Initalizes the client socket based on the ip and port.
    HOST = server_ip 
    PORT = 5555
    
    # Result for the client.
    result = None

    pygame.init()
    clock = pygame.time.Clock()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        # Sends a hello message to the server.
        send_msg(client_socket, {"type": "hello", "player": 1})
    except Exception as e:
        # If the connection fails, it quits.
        print("[CLIENT] Unable to connect to server:", e)
        return "quit"
    

    running = True
    # Initializes necessary game features.
    shop = Shop(triangle_color=GlobalSettings.blue)
    clicked_planet = None
    planets = []
    ships = []

    while running:
        # Sets up pygame loop and handles events.
        pygame.event.pump()
        input_data = {}
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # If the shop is clicked, it sends buy_ship to the server.
                    if shop.is_clicked(mouse_pos):
                        input_data = {
                            "type": "buy_ship"
                        }
                if event.button == 3:
                    # Resets the currently clicked planet.
                    if clicked_planet:
                        clicked_planet.selected = False
                    # Finds the clicked planet and sets it as the target planet for player2.
                    clicked_planet = planet_loc(mouse_x, mouse_y, draw_planets)
                    if clicked_planet:
                        player2.target_planet = clicked_planet.id
                        clicked_planet.selected = True
                        # Sends the data to the server.
                        input_data = {
                            "type": "select_planet",
                            "planet_id": clicked_planet.id
                        }

        # Receive exactly one state update.
        game_state_dict = recv_msg(client_socket)
        if game_state_dict is None:
            print("[CLIENT] Server closed connection.")
            break
        
        # Deserialize game state data.
        planets = game_state_dict["planets"]
        ships = game_state_dict["ships"]
        scoreboard = Scoreboard.deserialize(game_state_dict["scoreboard"])
        winner = game_state_dict["winner"]
        
        if winner:
            # If there is a winner, show the winner screen and exit.
            result = winnerScreen(screen, winner, GlobalSettings.WIDTH, GlobalSettings.HEIGHT)
            break
        
        # Tries to send something to the server.
        try:
            send_msg(client_socket, input_data or {"type": "noop"})
        except BrokenPipeError:
            print("[CLIENT] Lost connection to server.")
            break

        # Draws the game.
        screen.fill(GlobalSettings.light_mode_bg if not GlobalSettings.dark_background else GlobalSettings.dark_mode_bg)

        draw_planets = [Planet.deserialize(p) for p in planets]
        for ship_dict in ships:
            ship = Ship.deserialize(ship_dict)
            ship.draw(screen)
                
        for planet in draw_planets:
            planet.draw(screen, draw_planets)
        scoreboard.draw(screen)
        shop.is_hovered(mouse_pos)
        shop.draw(screen)
            

        pygame.display.flip()
        clock.tick(60)


    # Closes the socket and quits pygame.
    client_socket.close()
    pygame.quit()
    
    if result == "play_again":
        player1 = Player(1, GlobalSettings.orange, 0, player1.settings)
        player2 = Player(2, GlobalSettings.blue, 1, player2.settings)
        client(screen, player1, player2, server_ip)
