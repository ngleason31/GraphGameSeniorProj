import socket
from NetworkUtils import send_msg
from Game import runGame

def server(screen, player1, player2, host_ip):
    '''
    Handles the server side of the game during multiplayer mode.
    '''

    PORT = 5555
    client = None
    
    def broadcast_game_state(game_state):
        '''
        Helper function to broadcast the game state to the connected client
        '''
        
        try:
            send_msg(client, game_state)
        except Exception as e:
            print(f"[ERROR] Failed to broadcast: {e}")

    # Initalizes the server socket based on the ip and port.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host_ip, PORT))
    except Exception as e:
        print(f"[ERROR] Failed to bind to {host_ip}:{PORT} - {e}")
        return
    
    # Waits for a client to connect.
    server_socket.listen(1)
    print("[SERVER] Waiting for clients to connect...")
    try:
        conn, addr = server_socket.accept()
        print(f"[SERVER] Player 2 connected from {addr}")
        client = conn
    except Exception as e:
        print(f"[ERROR] Error accepting connection for Player 2: {e}")

    # Runs the game with the server mode and the broadcast function.
    runGame(
        screen=screen,
        player1=player1,
        player2=player2,
        server_mode=True,
        broadcast=broadcast_game_state,
        server=conn
    )

    # Closes the connection and server socket.
    conn.close()
    server_socket.close()
    print("[SERVER] Server socket closed.")
