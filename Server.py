import socket
from NetworkUtils import send_msg
import pickle
from Game import runGame

def server(screen, player1, player2, host_ip):
    #HOST = '0.0.0.0'
    PORT = 5555
    clients = []


    def broadcast_game_state(game_state):
        try:
            for client in clients:
                send_msg(client, game_state)
        except Exception as e:
            print(f"[ERROR] Failed to broadcast: {e}")


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host_ip, PORT))
    except Exception as e:
        print(f"[ERROR] Failed to bind to {host_ip}:{PORT} - {e}")
        return
    #server.bind((host_ip, PORT))
    server_socket.listen(1)
    print("[SERVER] Waiting for clients to connect...")
    try:
        conn, addr = server_socket.accept()
        print(f"[SERVER] Player 2 connected from {addr}")
        clients.append(conn)
    except Exception as e:
        print(f"[ERROR] Error accepting connection for Player 2: {e}")


    runGame(
        screen=screen,
        player1=player1,
        player2=player2,
        server_mode=True,
        broadcast=broadcast_game_state,
        server=conn
    )

    conn.close()
    server_socket.close()
    print("[SERVER] Server socket closed.")
